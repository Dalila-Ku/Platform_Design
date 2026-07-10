"""
utils/indicators.py
---------------------
Etapa CALCULATE INDICATORS: calcula las metricas necesarias para responder
la pregunta de investigacion:

    Is there a relationship between the number of assignment status updates
    and the likelihood of submitting an assignment before the deadline?
"""

import logging

import pandas as pd

logger = logging.getLogger("ETL")


def _bucket(n):
    if n <= 2:
        return "1) Baja (0-2)"
    elif n <= 4:
        return "2) Media (3-4)"
    else:
        return "3) Alta (5+)"


def calculate_indicators(df: pd.DataFrame):
    """
    Devuelve:
        indicators (dict)       -> resumen general para research_summary/indicators.json
        evaluated_df (DataFrame)-> tareas con desenlace evaluable + columnas auxiliares
        student_summary (DataFrame) -> agregado por usuario asignado
    """
    logger.info("[INDICATORS] Calculando indicadores sobre %d tareas.", len(df))

    evaluated = df.dropna(subset=["submitted_on_time"]).copy()
    evaluated["submitted_on_time"] = evaluated["submitted_on_time"].astype(bool)
    logger.info("[INDICATORS] %d tareas con desenlace evaluable (status='done').", len(evaluated))

    # Correlacion (status_update_count vs on_time como 0/1)
    correlation = None
    has_variation = (
        evaluated["status_update_count"].nunique() > 1
        and evaluated["submitted_on_time"].nunique() > 1
    )
    if len(evaluated) >= 2 and has_variation:
        correlation = evaluated["status_update_count"].corr(evaluated["submitted_on_time"].astype(int))
    logger.info("[INDICATORS] Correlacion (status_update_count vs on_time): %s",
                round(correlation, 3) if correlation is not None else "N/A (datos insuficientes)")

    # Tasa de entrega a tiempo por rango de actualizaciones
    evaluated["update_bucket"] = evaluated["status_update_count"].apply(_bucket)
    rate_by_bucket = (
        evaluated.groupby("update_bucket")["submitted_on_time"]
        .agg(on_time_rate="mean", n_tasks="count")
        .reset_index()
    )
    rate_by_bucket["on_time_rate"] = (rate_by_bucket["on_time_rate"] * 100).round(1)
    logger.info("[INDICATORS] Tasa de entrega a tiempo calculada por %d rangos de actualizacion.", len(rate_by_bucket))

    overall_on_time_rate = round(evaluated["submitted_on_time"].mean() * 100, 1) if len(evaluated) else None
    avg_updates_on_time = (
        round(evaluated.loc[evaluated["submitted_on_time"], "status_update_count"].mean(), 2)
        if evaluated["submitted_on_time"].any() else None
    )
    avg_updates_late = (
        round(evaluated.loc[~evaluated["submitted_on_time"], "status_update_count"].mean(), 2)
        if (~evaluated["submitted_on_time"]).any() else None
    )

    logger.info("[INDICATORS] Tasa global de entrega a tiempo: %s%%", overall_on_time_rate)
    logger.info("[INDICATORS] Promedio de actualizaciones (a tiempo): %s | (tarde): %s",
                avg_updates_on_time, avg_updates_late)

    # Resumen por estudiante (usuario asignado)
    student_summary = (
        df.groupby("assigned_user_name")
        .agg(
            total_tasks=("task_id", "count"),
            avg_status_updates=("status_update_count", "mean"),
            done_tasks=("status", lambda s: (s == "done").sum()),
        )
        .reset_index()
    )
    on_time_by_user = (
        evaluated.groupby("assigned_user_name")["submitted_on_time"].mean().mul(100).round(1)
    )
    student_summary = student_summary.merge(
        on_time_by_user.rename("on_time_rate_pct"), on="assigned_user_name", how="left"
    )
    student_summary["avg_status_updates"] = student_summary["avg_status_updates"].round(2)
    logger.info("[INDICATORS] Resumen por estudiante generado para %d usuarios.", len(student_summary))

    indicators = {
        "n_tasks_total": len(df),
        "n_tasks_evaluated": len(evaluated),
        "overall_on_time_rate_pct": overall_on_time_rate,
        "correlation_updates_vs_on_time": round(correlation, 3) if correlation is not None else None,
        "avg_updates_on_time": avg_updates_on_time,
        "avg_updates_late": avg_updates_late,
        "rate_by_update_bucket": rate_by_bucket.to_dict(orient="records"),
    }
    return indicators, evaluated, student_summary