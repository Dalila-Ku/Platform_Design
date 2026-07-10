"""
main.py
--------
Pipeline ETL — Platform_Design
Autora: Ingrid Castillo

Pregunta de investigacion:
    Is there a relationship between the number of assignment status updates
    and the likelihood of submitting an assignment before the deadline?

Fuentes de datos (2, de la plataforma compartida):
    1) platform.db  -> tabla `tasks` (SQLite, base de datos oficial del equipo)
    2) status_activity_log.json -> log de actividad de cambios de estado
       (ver utils/extract.py para la justificacion de esta fuente)

Ejecutar:
    python main.py
"""

import logging
import os
from datetime import datetime

from utils.extraact import extract_tasks_source, extract_status_log_source
from utils.traansform import transform_and_clean
from utils.indiicators import calculate_indicators
from utils.loaad import load_output

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "etl_run.log"), mode="w", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("ETL")


def run_pipeline():
    start = datetime.now()
    logger.info("========== INICIO DEL PIPELINE ETL ==========")

    tasks_df = extract_tasks_source()
    log_df = extract_status_log_source()
    clean_df = transform_and_clean(tasks_df, log_df)
    indicators, evaluated_df, student_summary = calculate_indicators(clean_df)
    load_output(clean_df, indicators, student_summary)

    elapsed = (datetime.now() - start).total_seconds()
    logger.info("========== PIPELINE COMPLETADO en %.2fs ==========", elapsed)
    return indicators


if __name__ == "__main__":
    run_pipeline()