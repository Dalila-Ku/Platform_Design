"""
LOAD — Guarda los resultados del ETL en la carpeta outputs/.

Archivos generados:
  outputs/tasks_clean.csv          — tareas limpias con columnas derivadas
  outputs/student_summary.csv      — resumen por estudiante
  outputs/indicators_report.xlsx   — reporte completo en Excel (2 hojas)
"""

import os
import json
import pandas as pd
from datetime import datetime

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")


def _ensure_dir():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)


def load_all(df_tasks: pd.DataFrame, student_summary: pd.DataFrame, indicators: dict):
    """Persiste todos los artefactos del pipeline ETL."""
    print("=" * 55)
    print("  LOAD PHASE")
    print("=" * 55)
    _ensure_dir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── 1. CSV de tareas limpias ───────────────────────────────────────────────
    tasks_path = os.path.join(OUTPUTS_DIR, "tasks_clean.csv")
    df_tasks.to_csv(tasks_path, index=False, encoding="utf-8-sig")
    print(f"[LOAD] tasks_clean.csv    → {tasks_path}  ({len(df_tasks)} filas)")

    # ── 2. CSV de resumen de estudiantes ──────────────────────────────────────
    summary_path = os.path.join(OUTPUTS_DIR, "student_summary.csv")
    student_summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
    print(f"[LOAD] student_summary.csv → {summary_path}  ({len(student_summary)} filas)")

    # ── 3. Reporte Excel (2 hojas) ────────────────────────────────────────────
    excel_path = os.path.join(OUTPUTS_DIR, "indicators_report.xlsx")
    try:
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df_tasks.to_excel(writer, sheet_name="Tareas Limpias", index=False)
            student_summary.to_excel(writer, sheet_name="Resumen Estudiantes", index=False)

            # Hoja de indicadores (KV)
            kv_rows = []
            for k, v in indicators.items():
                if k != "student_summary":
                    kv_rows.append({"Indicador": k, "Valor": str(v)})
            pd.DataFrame(kv_rows).to_excel(writer, sheet_name="Indicadores P4", index=False)

        print(f"[LOAD] indicators_report.xlsx → {excel_path}")
    except ImportError:
        print("[LOAD] WARNING: openpyxl no instalado — saltando Excel.")

    # ── 4. JSON de indicadores ────────────────────────────────────────────────
    json_path = os.path.join(OUTPUTS_DIR, "indicators.json")
    indicators_serializable = {k: v for k, v in indicators.items() if k != "student_summary"}
    indicators_serializable["generated_at"] = timestamp
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(indicators_serializable, f, ensure_ascii=False, indent=2)
    print(f"[LOAD] indicators.json    → {json_path}")

    print(f"\n[LOAD] ✅ Pipeline completado — {timestamp}")
    print(f"  Archivos en: {OUTPUTS_DIR}")
    return {
        "tasks_csv":    tasks_path,
        "summary_csv":  summary_path,
        "excel":        excel_path,
        "json":         json_path,
    }
