"""
ETL/main.py — Orquestador del pipeline ETL para P4.

Pregunta de investigación:
  ¿Existe relación entre el número de tareas activas de un estudiante
  en un momento dado y su porcentaje de entregas a tiempo?

Flujo:
  EXTRACT → TRANSFORM → INDICATORS → LOAD

Uso:
  cd Platform_Design-main
  python ETL/main.py
"""

import sys
import os

# Asegurar que el paquete ETL/UTILS sea importable
sys.path.insert(0, os.path.dirname(__file__))

from UTILS.extract    import extract_all
from UTILS.transform  import transform
from UTILS.indicators import compute_indicators
from UTILS.load       import load_all


def main():
    print("\n" + "=" * 55)
    print("  PIPELINE ETL — Assignment Submission Tracker")
    print("  Autor  : Esaú Palomo")
    print("  Proyecto: Platform Design (P4)")
    print("=" * 55 + "\n")

    # ── 1. EXTRACT ────────────────────────────────────────────────────────────
    df_sqlite, df_csv, df_users = extract_all()

    # Usar SQLite como fuente primaria; CSV como respaldo si SQLite está vacío
    df_primary = df_sqlite if df_sqlite is not None and len(df_sqlite) > 0 else df_csv

    # ── 2. TRANSFORM ──────────────────────────────────────────────────────────
    df_clean, student_summary = transform(df_primary, df_users)

    # ── 3. INDICATORS ─────────────────────────────────────────────────────────
    indicators = compute_indicators(df_clean, student_summary)

    # ── 4. LOAD ───────────────────────────────────────────────────────────────
    paths = load_all(df_clean, student_summary, indicators)

    # ── Resumen final ─────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  RESULTADO FINAL — Pregunta P4")
    print("=" * 55)
    r    = indicators.get("pearson_r")
    n    = indicators.get("pearson_n", 0)
    interp = indicators.get("pearson_interpretation", "")
    print(f"  r de Pearson : {r}")
    print(f"  n            : {n} estudiantes")
    print(f"  Conclusión   : {interp}")
    print("=" * 55 + "\n")

    return indicators


if __name__ == "__main__":
    main()
