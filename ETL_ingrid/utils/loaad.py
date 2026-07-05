"""
utils/load.py
---------------
Etapa LOAD: escribe los archivos finales en outputs/.
"""

import json
import logging
import os

import pandas as pd

logger = logging.getLogger("ETL")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")


def load_output(clean_df: pd.DataFrame, indicators: dict, student_summary: pd.DataFrame):
    """Escribe tasks_clean.csv, student_summary.csv, indicators.json e indicators_report.xlsx."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tasks_path = os.path.join(OUTPUT_DIR, "tasks_clean.csv")
    clean_df.to_csv(tasks_path, index=False)
    logger.info("[LOAD] %d filas escritas en %s", len(clean_df), tasks_path)

    summary_path = os.path.join(OUTPUT_DIR, "student_summary.csv")
    student_summary.to_csv(summary_path, index=False)
    logger.info("[LOAD] %d filas escritas en %s", len(student_summary), summary_path)

    json_path = os.path.join(OUTPUT_DIR, "indicators.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(indicators, f, ensure_ascii=False, indent=2, default=str)
    logger.info("[LOAD] Indicadores escritos en %s", json_path)

    xlsx_path = os.path.join(OUTPUT_DIR, "indicators_report.xlsx")
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        clean_df.to_excel(writer, sheet_name="tasks_clean", index=False)
        student_summary.to_excel(writer, sheet_name="student_summary", index=False)
        pd.DataFrame(indicators["rate_by_update_bucket"]).to_excel(
            writer, sheet_name="rate_by_bucket", index=False
        )
        overview = pd.DataFrame([{
            "n_tasks_total": indicators["n_tasks_total"],
            "n_tasks_evaluated": indicators["n_tasks_evaluated"],
            "overall_on_time_rate_pct": indicators["overall_on_time_rate_pct"],
            "correlation_updates_vs_on_time": indicators["correlation_updates_vs_on_time"],
            "avg_updates_on_time": indicators["avg_updates_on_time"],
            "avg_updates_late": indicators["avg_updates_late"],
        }])
        overview.to_excel(writer, sheet_name="overview", index=False)
    logger.info("[LOAD] Reporte Excel escrito en %s", xlsx_path)