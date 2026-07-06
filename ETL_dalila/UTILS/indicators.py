"""
INDICATORS — Calcula el indicador central para Q3 de Dalila.

Pregunta: ¿Las tareas de alta prioridad se completan antes, en promedio,
          que las de prioridad media y baja?

Indicador: Promedio de días de completado agrupado por nivel de prioridad.
           También se calcula la diferencia entre high vs medium/low.
"""

import pandas as pd
import numpy as np


def compute_indicators(df_tasks: pd.DataFrame, priority_summary: pd.DataFrame,
                        df_users: pd.DataFrame = None) -> dict:
    print("=" * 55)
    print("  INDICATORS PHASE")
    print("=" * 55)

    result = {}

    # ── 0. Indicadores de la 2da fuente: equipo/usuarios ──────────────────────
    if df_users is not None and len(df_users) > 0:
        result["team_size"] = int(len(df_users))
        if "role" in df_users.columns:
            role_counts = df_users["role"].value_counts().to_dict()
            result["roles_breakdown"] = role_counts
            print(f"[INDICATORS] Equipo: {result['team_size']} integrantes | roles: {role_counts}")
        else:
            print(f"[INDICATORS] Equipo: {result['team_size']} integrantes")

    # ── 1. Estadísticas generales ─────────────────────────────────────────────
    total = len(df_tasks)
    done  = (df_tasks["status"] == "done").sum() if "status" in df_tasks.columns else 0
    result["total_tasks"]     = int(total)
    result["completed_tasks"] = int(done)
    result["completion_rate"] = round(done / total, 4) if total > 0 else 0

    print(f"[INDICATORS] Total tareas   : {total}")
    print(f"[INDICATORS] Completadas    : {done} ({result['completion_rate']:.1%})")

    # ── 2. Promedio de días por prioridad ─────────────────────────────────────
    result["priority_summary"] = priority_summary.to_dict(orient="records")

    print(f"\n[INDICATORS] Días promedio de completado por prioridad:")
    for _, row in priority_summary.iterrows():
        print(f"  {row['priority']:10s} → {row['avg_completion_days']} días  ({int(row['task_count'])} tareas)")

    # ── 3. Indicador principal Q3: high vs rest ───────────────────────────────
    high_row   = priority_summary[priority_summary["priority"] == "high"]
    others_row = priority_summary[priority_summary["priority"].isin(["medium", "low"])]

    if not high_row.empty and not others_row.empty:
        avg_high   = high_row["avg_completion_days"].values[0]
        avg_others = others_row["avg_completion_days"].mean()
        diff       = round(avg_high - avg_others, 2)

        result["avg_days_high"]   = round(float(avg_high), 2)
        result["avg_days_others"] = round(float(avg_others), 2)
        result["diff_high_vs_others"] = diff

        print(f"\n[INDICATORS] ─── RESULTADO Q3 ───")
        print(f"  Promedio días HIGH        : {avg_high} días")
        print(f"  Promedio días MEDIUM+LOW  : {round(avg_others, 2)} días")
        print(f"  Diferencia (high - otros) : {diff} días")

        if diff < 0:
            conclusion = (f"Las tareas de alta prioridad se completan {abs(diff)} días ANTES "
                          f"en promedio que las de prioridad media/baja. "
                          f"Respuesta a Q3: SÍ, se completan más rápido.")
        elif diff > 0:
            conclusion = (f"Las tareas de alta prioridad tardan {diff} días MÁS en completarse "
                          f"que las de prioridad media/baja. "
                          f"Respuesta a Q3: NO, no se completan más rápido.")
        else:
            conclusion = "Sin diferencia significativa entre niveles de prioridad."

        result["conclusion"] = conclusion
        print(f"  Conclusión: {conclusion}")
    else:
        result["conclusion"] = "Datos insuficientes para comparar prioridades."
        print("[INDICATORS] WARNING: No hay datos de high y/o medium/low para comparar.")

    print()
    return result
