"""
EXTRACT — Fuentes de datos para la pregunta Q3 de Dalila.

Pregunta: ¿Las tareas de alta prioridad se completan antes, en promedio,
          que las de prioridad media y baja?

Fuente 1: CSV de tareas desde GitHub (tasks_sample.csv)
Fuente 2: CSV de usuarios desde GitHub (users_sample.csv)
"""

import pandas as pd
import requests
import io

GITHUB_BASE = "https://raw.githubusercontent.com/Dalila-Ku/Platform_Design/main"

SOURCE_CANDIDATES = {
    "tasks": [
        f"{GITHUB_BASE}/db_files/dalila/data/tasks_sample.csv",
    ],
    "users": [
        # Fuente real compartida del equipo (antes apuntaba a un archivo
        # inexistente: db_files/dalila/data/users_sample.csv -> 404)
        f"{GITHUB_BASE}/db_files/esau/data/users.csv",
    ],
}

# ── Fallback data ─────────────────────────────────────────────────────────────

FALLBACK_TASKS = pd.DataFrame({
    "id":              list(range(1, 21)),
    "title":           [f"Task {i}" for i in range(1, 21)],
    "status":          (["done", "in_progress", "todo", "done", "done"] * 4),
    "priority":        (["high", "high", "medium", "medium", "low"] * 4),
    "difficulty":      (["hard", "medium", "easy", "hard", "medium"] * 4),
    "assignment_date": pd.date_range("2026-05-01", periods=20, freq="3D").astype(str).tolist(),
    "start_date":      pd.date_range("2026-05-02", periods=20, freq="3D").astype(str).tolist(),
    "due_date":        pd.date_range("2026-05-20", periods=20, freq="3D").astype(str).tolist(),
    "completed_date":  (pd.date_range("2026-05-10", periods=12, freq="3D").astype(str).tolist() + [None] * 8),
    "estimated_hours": ([8, 12, 4, 16, 6, 10, 20, 3, 14, 5] * 2),
    "actual_hours":    ([7, 11, None, 15, 5, 9, 18, None, 13, 4] * 2),
})

FALLBACK_USERS = pd.DataFrame({
    "id":        [1, 2, 3, 4, 5, 6, 7, 8],
    "full_name": ["Dalila Ku", "Esaú Palomo", "Yeimi Piste", "Gael Pérez",
                  "Ingrid Castillo", "Ana Torres", "Luis Méndez", "Sofía Ramírez"],
    "email":     [f"user{i}@upy.edu.mx" for i in range(1, 9)],
    "role":      (["student"] * 8),
})


def _fetch_csv(urls: list, label: str):
    for url in urls:
        try:
            print(f"[EXTRACT]   Intentando {label}: {url}")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            df = pd.read_csv(io.StringIO(resp.text))
            print(f"[EXTRACT] {label} OK — {len(df)} filas")
            return df, url
        except Exception as e:
            print(f"[EXTRACT]   FAILED: {type(e).__name__}: {e}")
    return None, "fallback"


def extract_all():
    print("=" * 55)
    print("  EXTRACT PHASE")
    print("=" * 55)

    df_tasks, tasks_url = _fetch_csv(SOURCE_CANDIDATES["tasks"], "tasks")
    df_users, users_url = _fetch_csv(SOURCE_CANDIDATES["users"], "users")

    if df_tasks is None:
        print("[EXTRACT] WARNING: Usando fallback de tasks.")
        df_tasks = FALLBACK_TASKS.copy()
        tasks_url = "local_fallback"

    if df_users is None:
        print("[EXTRACT] WARNING: Usando fallback de users.")
        df_users = FALLBACK_USERS.copy()
        users_url = "local_fallback"

    print(f"\n[EXTRACT] Resumen:")
    print(f"  tasks : {len(df_tasks)} filas | {tasks_url}")
    print(f"  users : {len(df_users)} filas | {users_url}\n")
    return df_tasks, df_users
