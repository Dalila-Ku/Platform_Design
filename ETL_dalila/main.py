"""
ETL/main.py — Pipeline ETL para Q3 de Dalila Ku.

Pregunta de investigación:
  ¿Las tareas de alta prioridad se completan antes, en promedio,
  que las de prioridad media y baja?

Indicador: Promedio de días de completado por nivel de prioridad.

Uso:
  python main.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from UTILS.extract    import extract_all
from UTILS.transform  import transform
from UTILS.indicators import compute_indicators
from UTILS.load       import load_all


def main():
    print("\n" + "=" * 55)
    print("  PIPELINE ETL — Assignment Submission Tracker")
    print("  Autora : Dalila de los Ángeles Ku Dzul")
    print("  Pregunta Q3: Priority vs Completion Time")
    print("=" * 55 + "\n")

    # EXTRACT
    df_tasks, df_users = extract_all()

    # TRANSFORM
    df_clean, priority_summary, df_users_clean = transform(df_tasks, df_users)

    # INDICATORS
    indicators = compute_indicators(df_clean, priority_summary, df_users_clean)

    # LOAD
    load_all(df_clean, priority_summary, indicators, df_users_clean)

    # Resultado final
    print("\n" + "=" * 55)
    print("  RESULTADO FINAL — Pregunta Q3")
    print("=" * 55)
    print(f"  {indicators.get('conclusion', 'Sin conclusión')}")
    print("=" * 55 + "\n")

    return indicators


if __name__ == "__main__":
    main()
