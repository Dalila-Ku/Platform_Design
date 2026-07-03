"""
TRANSFORM — Limpieza y preparación de datos para la pregunta P4.

Pregunta: ¿Existe relación entre el número de tareas activas de un
          estudiante en un momento dado y su porcentaje de entregas a tiempo?
"""

import pandas as pd
import numpy as np

# Fecha de referencia para contar tareas "activas" simultáneas
REFERENCE_DATE = pd.Timestamp("2026-06-10")

def transform(df_tasks: pd.DataFrame, df_users: pd.DataFrame):
    print("=" * 55)
    print("  TRANSFORM PHASE")
    print("=" * 55)

    df = df_tasks.copy()

    # ── 1. Normalizar nombres de columnas ─────────────────────────────────────
    df.columns = (df.columns.str.strip().str.lower()
                             .str.replace(" ", "_").str.replace("-", "_"))
    print(f"[TRANSFORM] Columnas normalizadas: {df.columns.tolist()}")

    # ── 2. Eliminar duplicados ────────────────────────────────────────────────
    before = len(df)
    df = df.drop_duplicates()
    print(f"[TRANSFORM] Duplicados eliminados: {before - len(df)} | Filas restantes: {len(df)}")

    # ── 3. Parsear fechas ─────────────────────────────────────────────────────
    date_cols = ["assignment_date", "start_date", "due_date", "completed_date"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    print(f"[TRANSFORM] Fechas parseadas: {date_cols}")

    # ── 4. Rellenar nulos en campos categóricos ───────────────────────────────
    if "status"     in df.columns: df["status"]     = df["status"].fillna("unknown")
    if "priority"   in df.columns: df["priority"]   = df["priority"].fillna("medium")
    if "difficulty" in df.columns: df["difficulty"] = df["difficulty"].fillna("medium")
    print(f"[TRANSFORM] Nulos en categóricos rellenados.")

    # ── 5. student_id ─────────────────────────────────────────────────────────
    if "student_id" not in df.columns:
        if "created_by" in df.columns:
            df["student_id"] = pd.to_numeric(df["created_by"], errors="coerce")
        else:
            user_ids = list(df_users["id"]) if df_users is not None else list(range(1, 6))
            df["student_id"] = [user_ids[i % len(user_ids)] for i in range(len(df))]
        print("[TRANSFORM] student_id creado.")

    # ── 6. Columnas derivadas para P4 ─────────────────────────────────────────

    # ¿La tarea estaba activa en la fecha de referencia?
    df["is_active_at_ref"] = (
        (df["assignment_date"] <= REFERENCE_DATE) &
        (df["due_date"] >= REFERENCE_DATE) &
        (~df["status"].isin(["done", "cancelled"]))
    ).astype(int)

    # ¿Se entregó a tiempo?
    df["on_time"] = (
        (df["status"] == "done") &
        df["completed_date"].notna() &
        df["due_date"].notna() &
        (df["completed_date"] <= df["due_date"])
    ).astype(int)

    # Días para iniciar desde asignación
    df["days_to_start"] = (df["start_date"] - df["assignment_date"]).dt.days

    # Días vs deadline (negativo = antes, positivo = tarde)
    df["days_vs_deadline"] = (df["completed_date"] - df["due_date"]).dt.days

    print(f"[TRANSFORM] Columnas derivadas creadas: is_active_at_ref, on_time, days_to_start, days_vs_deadline")

    # ── 7. Resumen por estudiante ─────────────────────────────────────────────
    student_summary = (
        df.groupby("student_id")
        .agg(
            total_tasks       = ("id", "count"),
            active_at_ref     = ("is_active_at_ref", "sum"),
            completed_tasks   = ("on_time", lambda x: (df.loc[x.index, "status"] == "done").sum()),
            on_time_count     = ("on_time", "sum"),
        )
        .reset_index()
    )
    student_summary["on_time_rate"] = (
        student_summary["on_time_count"] / student_summary["completed_tasks"].replace(0, np.nan)
    ).round(4).fillna(0)

    # Merge con nombres de usuarios
    if df_users is not None and "full_name" in df_users.columns:
        df_users_clean = df_users[["id","full_name"]].rename(columns={"id":"student_id","full_name":"student_name"})
        student_summary = student_summary.merge(df_users_clean, on="student_id", how="left")

    print(f"\n[TRANSFORM] Resumen por estudiante ({len(student_summary)} estudiantes):")
    print(student_summary.to_string(index=False))
    print()

    return df, student_summary
