"""
TRANSFORM — Limpieza y preparación para Q3 de Dalila.

Pregunta: ¿Las tareas de alta prioridad se completan antes, en promedio,
          que las de prioridad media y baja?

Columna clave derivada: completion_days = completed_date - assignment_date
"""

import pandas as pd
import numpy as np

PRIORITY_ORDER = {"high": 1, "medium": 2, "low": 3,
                  "critical": 0, "unknown": 4}


def transform(df_tasks: pd.DataFrame, df_users: pd.DataFrame):
    print("=" * 55)
    print("  TRANSFORM PHASE")
    print("=" * 55)

    # ── 0. Limpieza de la 2da fuente: usuarios/equipo ─────────────────────────
    df_u = df_users.copy()
    df_u.columns = (df_u.columns.str.strip().str.lower()
                                 .str.replace(" ", "_").str.replace("-", "_"))
    before_u = len(df_u)
    df_u = df_u.drop_duplicates()
    if "email" in df_u.columns:
        df_u["email"] = df_u["email"].str.strip().str.lower()
    if "role" in df_u.columns:
        df_u["role"] = df_u["role"].fillna("unknown").str.strip().str.lower()
    if "full_name" in df_u.columns:
        df_u["full_name"] = df_u["full_name"].str.strip()
    print(f"[TRANSFORM] Usuarios: {before_u} filas → {len(df_u)} tras limpieza "
          f"(columnas: {df_u.columns.tolist()})")

    df = df_tasks.copy()

    # ── 1. Normalizar columnas ────────────────────────────────────────────────
    df.columns = (df.columns.str.strip().str.lower()
                             .str.replace(" ", "_").str.replace("-", "_"))
    print(f"[TRANSFORM] Columnas: {df.columns.tolist()}")

    # ── 2. Duplicados ─────────────────────────────────────────────────────────
    before = len(df)
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Duplicados eliminados: {before - len(df)} | Filas: {len(df)}")

    # ── 3. Parsear fechas ─────────────────────────────────────────────────────
    for col in ["assignment_date", "start_date", "due_date", "completed_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    print("[TRANSFORM] Fechas parseadas.")

    # ── 4. Nulos en categóricos ───────────────────────────────────────────────
    if "priority"   in df.columns: df["priority"]   = df["priority"].fillna("unknown").str.lower().str.strip()
    if "status"     in df.columns: df["status"]     = df["status"].fillna("unknown").str.lower().str.strip()
    if "difficulty" in df.columns: df["difficulty"] = df["difficulty"].fillna("unknown").str.lower().str.strip()

    # ── 5. Columna derivada clave: completion_days ───────────────────────────
    # Solo para tareas completadas
    df["completion_days"] = None
    mask_done = (df["status"] == "done") & df["completed_date"].notna() & df["assignment_date"].notna()
    df.loc[mask_done, "completion_days"] = (
        (df.loc[mask_done, "completed_date"] - df.loc[mask_done, "assignment_date"]).dt.days
    )
    df["completion_days"] = pd.to_numeric(df["completion_days"], errors="coerce")

    # Días hasta el deadline
    if "due_date" in df.columns and "assignment_date" in df.columns:
        df["days_to_deadline"] = (df["due_date"] - df["assignment_date"]).dt.days

    # Entregada a tiempo
    if "completed_date" in df.columns and "due_date" in df.columns:
        df["on_time"] = (
            (df["status"] == "done") &
            df["completed_date"].notna() &
            (df["completed_date"] <= df["due_date"])
        ).astype(int)

    print(f"[TRANSFORM] Columnas derivadas: completion_days, days_to_deadline, on_time")

    # ── 6. Resumen por prioridad (indicador Q3) ───────────────────────────────
    df_done = df[df["status"] == "done"].copy()
    priority_summary = (
        df_done.groupby("priority")
        .agg(
            task_count        = ("id", "count"),
            avg_completion_days = ("completion_days", "mean"),
            min_completion_days = ("completion_days", "min"),
            max_completion_days = ("completion_days", "max"),
            on_time_count     = ("on_time", "sum"),
        )
        .reset_index()
    )
    priority_summary["avg_completion_days"] = priority_summary["avg_completion_days"].round(2)
    priority_summary["on_time_rate"] = (
        priority_summary["on_time_count"] / priority_summary["task_count"]
    ).round(4)
    priority_summary["priority_order"] = priority_summary["priority"].map(PRIORITY_ORDER).fillna(9)
    priority_summary = priority_summary.sort_values("priority_order").drop(columns="priority_order")

    print(f"\n[TRANSFORM] Resumen por prioridad:")
    print(priority_summary.to_string(index=False))
    print()

    return df, priority_summary, df_u
