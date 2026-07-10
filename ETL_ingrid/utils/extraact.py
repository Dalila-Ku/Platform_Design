"""
utils/extract.py
------------------
Etapa EXTRACT del pipeline.

Fuente 1: tabla `tasks` en platform.db (base de datos oficial de la plataforma)
Fuente 2: status_activity_log.json (log de actividad de cambios de estado)

La plataforma todavia no registra un historial de estados (la tabla
`comments` esta vacia y no existe `status_history`), asi que la fuente 2
se genera de forma sintetica pero realista, simulando lo que emitiria un
microservicio de auditoria. Ver generate_status_log() para el detalle.
"""

import json
import logging
import os
import random
import sqlite3
from datetime import datetime, timedelta

import pandas as pd

logger = logging.getLogger("ETL")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "platform.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
SEED_DATA_PATH = os.path.join(BASE_DIR, "generated_data.sql")
STATUS_LOG_PATH = os.path.join(BASE_DIR, "status_activity_log.json")

STATUS_FLOW = ["todo", "in_progress", "in_review", "done"]
random.seed(42)


# ── Preparacion (solo corre si los archivos no existen aun) ────────────────

def ensure_database():
    """Construye platform.db desde schema.sql + generated_data.sql si no existe."""
    if os.path.exists(DB_PATH):
        logger.info("[EXTRACT-1] platform.db ya existe, se usa el actual.")
        return
    logger.info("[EXTRACT-1] platform.db no existe. Construyendo desde schema.sql + generated_data.sql ...")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    with open(SEED_DATA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    logger.info("[EXTRACT-1] platform.db construido correctamente.")


def _parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d") if s else None


def _build_event_sequence(task):
    assignment_date = _parse_date(task["assignment_date"]) or datetime(2026, 1, 1)
    due_date = _parse_date(task["due_date"])
    completed_date = _parse_date(task["completed_date"])
    final_status = task["status"]

    on_time = None
    if final_status == "done" and completed_date and due_date:
        on_time = completed_date <= due_date

    if on_time is True:
        base_updates = random.randint(2, 4)
    elif on_time is False:
        base_updates = random.randint(4, 8)
    else:
        base_updates = random.randint(1, 5)

    n_updates = max(1, base_updates + random.choice([-1, 0, 0, 1]))

    events = []
    window_end = completed_date or due_date or (assignment_date + timedelta(days=14))
    span_days = max((window_end - assignment_date).days, 1)

    prev_status = "todo"
    for i in range(n_updates):
        offset = int(span_days * (i + 1) / (n_updates + 1))
        changed_at = assignment_date + timedelta(days=offset)
        new_status = random.choice(STATUS_FLOW)
        events.append({
            "task_id": task["id"],
            "previous_status": prev_status,
            "new_status": new_status,
            "changed_at": changed_at.strftime("%Y-%m-%d"),
            "changed_by": random.randint(1, 15),
        })
        prev_status = new_status
    return events


def generate_status_log():
    """Genera status_activity_log.json (fuente 2) si no existe todavia."""
    if os.path.exists(STATUS_LOG_PATH):
        logger.info("[EXTRACT-2] status_activity_log.json ya existe, se usa el actual.")
        return
    logger.info("[EXTRACT-2] status_activity_log.json no existe. Generando log de actividad ...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    tasks = [dict(r) for r in conn.execute(
        "SELECT id, status, assignment_date, start_date, due_date, completed_date FROM tasks"
    ).fetchall()]
    conn.close()

    all_events = []
    for task in tasks:
        all_events.extend(_build_event_sequence(task))

    with open(STATUS_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)
    logger.info("[EXTRACT-2] %d eventos generados para %d tareas.", len(all_events), len(tasks))


# ── Extract real ─────────────────────────────────────────────────────────

def extract_tasks_source() -> pd.DataFrame:
    """Extrae la tabla `tasks` (con usuario asignado) desde platform.db."""
    ensure_database()
    logger.info("[EXTRACT-1] Conectando a la base de datos: %s", DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT t.id AS task_id, t.project_id, t.title, t.status, t.priority, t.difficulty,
               t.assignment_date, t.start_date, t.due_date, t.completed_date,
               t.estimated_hours, t.actual_hours, t.created_by,
               u.id AS assigned_user_id, u.full_name AS assigned_user_name
        FROM tasks t
        LEFT JOIN task_assignments ta ON ta.task_id = t.id
        LEFT JOIN users u ON u.id = ta.user_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    logger.info("[EXTRACT-1] %d filas extraidas de la tabla 'tasks' (con join a usuarios asignados).", len(df))
    return df


def extract_status_log_source() -> pd.DataFrame:
    """Extrae el log de actividad de cambios de estado (fuente 2)."""
    generate_status_log()
    logger.info("[EXTRACT-2] Leyendo log de actividad: %s", STATUS_LOG_PATH)
    with open(STATUS_LOG_PATH, "r", encoding="utf-8") as f:
        events = json.load(f)
    df = pd.DataFrame(events)
    logger.info("[EXTRACT-2] %d eventos de actualizacion de estado extraidos, correspondientes a %d tareas distintas.",
                len(df), df["task_id"].nunique())
    return df