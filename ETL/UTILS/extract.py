"""
EXTRACT — Conexión a las 2 fuentes de la plataforma compartida.

Fuente 1: Base de datos SQLite (platform.db local)
Fuente 2: CSV de tareas desde GitHub (tasks_sample.csv)
"""

import sqlite3
import pandas as pd
import requests
import io
import os

# ── Configuración ─────────────────────────────────────────────────────────────

GITHUB_BASE = "https://raw.githubusercontent.com/Dalila-Ku/Platform_Design/main"
CSV_URLS = [
    f"{GITHUB_BASE}/db_files/dalila/data/tasks_sample.csv",
]

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "platform.db")

# ── Fallback data (si GitHub no está disponible) ──────────────────────────────

FALLBACK_TASKS = pd.DataFrame({
    "id":              list(range(1, 21)),
    "title":           [f"Task {i}" for i in range(1, 21)],
    "status":          (["done","in_progress","todo","done","in_review"] * 4),
    "priority":        (["critical","high","medium","low","high"] * 4),
    "difficulty":      (["very_hard","hard","medium","easy","hard"] * 4),
    "assignment_date": pd.date_range("2026-05-01", periods=20, freq="3D").astype(str).tolist(),
    "start_date":      pd.date_range("2026-05-02", periods=20, freq="3D").astype(str).tolist(),
    "due_date":        pd.date_range("2026-05-15", periods=20, freq="3D").astype(str).tolist(),
    "completed_date":  (pd.date_range("2026-05-12", periods=10, freq="3D").astype(str).tolist() + [None]*10),
    "created_by":      ([1,2,3,4,5,1,2,3,4,5]*2),
    "estimated_hours": ([8,12,4,16,6,10,20,3,14,5]*2),
    "actual_hours":    ([7,11,None,15,5,9,18,None,13,4]*2),
})

# ── Source 1: SQLite ──────────────────────────────────────────────────────────

def extract_sqlite():
    """Extrae tareas y usuarios desde la base de datos SQLite local."""
    print("[EXTRACT] Fuente 1: Conectando a SQLite (platform.db) ...")
    try:
        conn = sqlite3.connect(DB_PATH)
        df_tasks = pd.read_sql("""
            SELECT t.id, t.title, t.status, t.priority, t.difficulty,
                   t.assignment_date, t.start_date, t.due_date, t.completed_date,
                   t.estimated_hours, t.actual_hours,
                   u.full_name as assigned_to, u.id as student_id
            FROM tasks t
            LEFT JOIN task_assignments ta ON ta.task_id = t.id
            LEFT JOIN users u ON u.id = ta.user_id
            ORDER BY t.id
        """, conn)
        df_users = pd.read_sql("SELECT id, full_name, email, role FROM users", conn)
        conn.close()
        print(f"[EXTRACT] SQLite OK — tasks: {len(df_tasks)} | users: {len(df_users)}")
        return df_tasks, df_users
    except Exception as e:
        print(f"[EXTRACT] SQLite FAILED: {e}")
        return None, None

# ── Source 2: CSV desde GitHub ────────────────────────────────────────────────

def extract_csv():
    """Extrae el CSV de tareas desde el repositorio GitHub."""
    print("[EXTRACT] Fuente 2: Conectando a CSV en GitHub ...")
    for url in CSV_URLS:
        try:
            print(f"[EXTRACT]   Intentando: {url}")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            df = pd.read_csv(io.StringIO(resp.text))
            print(f"[EXTRACT] CSV OK — {len(df)} filas, columnas: {df.columns.tolist()}")
            return df, url
        except Exception as e:
            print(f"[EXTRACT]   FAILED: {type(e).__name__}: {e}")
    print("[EXTRACT] WARNING: Usando datos de fallback local para CSV.")
    return FALLBACK_TASKS.copy(), "local_fallback"

# ── Orquestador ───────────────────────────────────────────────────────────────

def extract_all():
    """Ejecuta la extracción de ambas fuentes y retorna los DataFrames."""
    print("=" * 55)
    print("  EXTRACT PHASE")
    print("=" * 55)
    df_sqlite, df_users = extract_sqlite()
    df_csv, csv_source  = extract_csv()

    # Si SQLite falló, usar CSV como fuente principal
    if df_sqlite is None:
        print("[EXTRACT] Usando CSV como fuente principal (SQLite no disponible).")
        df_sqlite = df_csv.copy()
        df_users  = pd.DataFrame({"id": range(1,6),
                                  "full_name": ["Dalila Ku","Esaú Palomo","Yeimi Piste","Gael Pérez","Ingrid Castillo"]})

    print(f"\n[EXTRACT] Resumen:")
    print(f"  Fuente 1 (SQLite) : {len(df_sqlite)} tareas")
    print(f"  Fuente 2 (CSV)    : {len(df_csv)} tareas | URL: {csv_source}")
    print(f"  Usuarios          : {len(df_users)}\n")
    return df_sqlite, df_csv, df_users
