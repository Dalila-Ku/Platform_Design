"""
utils/transform.py
--------------------
Etapa TRANSFORM del pipeline: limpieza, union de las 2 fuentes y calculo
de las columnas base necesarias para los indicadores.
"""

import logging

import pandas as pd

logger = logging.getLogger("ETL")


def transform_and_clean(tasks_df: pd.DataFrame, log_df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia ambas fuentes y las combina en un solo dataframe a nivel tarea.

    Operaciones aplicadas:
        - Conversion de fechas a datetime
        - Eliminacion de duplicados (por task_id y en el log)
        - Conteo de actualizaciones de estado por tarea (agregado de la fuente 2)
        - Calculo de la bandera submitted_on_time
    """
    logger.info("[TRANSFORM] Iniciando limpieza. Filas de entrada -> tasks: %d, log: %d",
                len(tasks_df), len(log_df))

    df = tasks_df.copy()

    # -- Fechas --
    date_cols = ["assignment_date", "start_date", "due_date", "completed_date"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    logger.info("[TRANSFORM] Columnas de fecha convertidas a datetime: %s", date_cols)

    # -- Duplicados en tasks --
    before = len(df)
    df = df.drop_duplicates(subset="task_id")
    logger.info("[TRANSFORM] Duplicados eliminados en tasks: %d", before - len(df))

    # -- Limpieza del log de actividad --
    log_clean = log_df.drop_duplicates().copy()
    log_clean["changed_at"] = pd.to_datetime(log_clean["changed_at"], errors="coerce")
    logger.info("[TRANSFORM] Duplicados eliminados en log de actividad: %d",
                len(log_df) - len(log_clean))

    # -- Agregacion: numero de actualizaciones de estado por tarea --
    updates_per_task = (
        log_clean.groupby("task_id").size().reset_index(name="status_update_count")
    )
    df = df.merge(updates_per_task, on="task_id", how="left")
    df["status_update_count"] = df["status_update_count"].fillna(0).astype(int)
    logger.info("[TRANSFORM] Conteo de actualizaciones de estado calculado y unido a %d tareas.", len(df))

    missing_due = df["due_date"].isna().sum()
    if missing_due:
        logger.info("[TRANSFORM] %d tareas sin due_date; se excluyen del calculo de entrega a tiempo.", missing_due)

    # -- Bandera de entrega a tiempo (solo aplica a tareas 'done') --
    df["submitted_on_time"] = pd.NA
    done_mask = df["status"] == "done"
    df.loc[done_mask, "submitted_on_time"] = (
        df.loc[done_mask, "completed_date"] <= df.loc[done_mask, "due_date"]
    )
    logger.info("[TRANSFORM] Bandera 'submitted_on_time' calculada para %d tareas con status='done'.",
                done_mask.sum())

    logger.info("[TRANSFORM] Filas de salida tras limpieza y union: %d", len(df))
    return df