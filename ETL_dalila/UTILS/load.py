"""
LOAD — Guarda los resultados del ETL de Dalila en outputs/.

Archivos generados:
  outputs/tasks_clean.csv
  outputs/priority_summary.csv
  outputs/indicators_report.xlsx   (2 hojas)
  outputs/indicators.json
"""

import os
import json
import pandas as pd
from datetime import datetime

OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")


def _ensure_dir():
    os.makedirs(OUTPUTS_DIR, exist_ok=True)


def load_all(df_tasks: pd.DataFrame, priority_summary: pd.DataFrame, indicators: dict,
             df_users: pd.DataFrame = None):
    print("=" * 55)
    print("  LOAD PHASE")
    print("=" * 55)
    _ensure_dir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── 1. CSV tareas limpias ─────────────────────────────────────────────────
    tasks_path = os.path.join(OUTPUTS_DIR, "tasks_clean.csv")
    df_tasks.to_csv(tasks_path, index=False, encoding="utf-8-sig")
    print(f"[LOAD] tasks_clean.csv      → {tasks_path}  ({len(df_tasks)} filas)")

    # ── 2. CSV resumen por prioridad ──────────────────────────────────────────
    summary_path = os.path.join(OUTPUTS_DIR, "priority_summary.csv")
    priority_summary.to_csv(summary_path, index=False, encoding="utf-8-sig")
    print(f"[LOAD] priority_summary.csv → {summary_path}  ({len(priority_summary)} filas)")

    # ── 2b. CSV usuarios/equipo limpios (2da fuente) ──────────────────────────
    users_path = None
    if df_users is not None and len(df_users) > 0:
        users_path = os.path.join(OUTPUTS_DIR, "users_clean.csv")
        df_users.to_csv(users_path, index=False, encoding="utf-8-sig")
        print(f"[LOAD] users_clean.csv      → {users_path}  ({len(df_users)} filas)")

    # ── 3. Excel ──────────────────────────────────────────────────────────────
    excel_path = os.path.join(OUTPUTS_DIR, "indicators_report.xlsx")
    try:
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df_tasks.to_excel(writer, sheet_name="Tareas Limpias", index=False)
            priority_summary.to_excel(writer, sheet_name="Resumen por Prioridad", index=False)
            if df_users is not None and len(df_users) > 0:
                df_users.to_excel(writer, sheet_name="Equipo (Usuarios)", index=False)
            kv = [{"Indicador": k, "Valor": str(v)}
                  for k, v in indicators.items() if k != "priority_summary"]
            pd.DataFrame(kv).to_excel(writer, sheet_name="Indicadores Q3", index=False)
        print(f"[LOAD] indicators_report.xlsx → {excel_path}")
    except ImportError:
        print("[LOAD] WARNING: openpyxl no instalado — saltando Excel.")

    # ── 4. JSON indicadores ───────────────────────────────────────────────────
    json_path = os.path.join(OUTPUTS_DIR, "indicators.json")
    serializable = {k: v for k, v in indicators.items() if k != "priority_summary"}
    serializable["generated_at"] = timestamp
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)
    print(f"[LOAD] indicators.json      → {json_path}")

    print(f"\n[LOAD] ✅ Pipeline completado — {timestamp}")
    return {
        "tasks_csv":   tasks_path,
        "summary_csv": summary_path,
        "users_csv":   users_path,
        "excel":       excel_path,
        "json":        json_path,
    }
