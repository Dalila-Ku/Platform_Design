"""
INDICATORS — Calcula el indicador central de la pregunta P4.

Pregunta: ¿Existe relación entre el número de tareas activas de un
          estudiante en un momento dado y su porcentaje de entregas a tiempo?

Indicador: Correlación de Pearson entre active_at_ref y on_time_rate
"""

import pandas as pd
import numpy as np


def pearson_r(x: pd.Series, y: pd.Series):
    """Calcula el coeficiente de correlación de Pearson manualmente."""
    x = x.dropna()
    y = y.dropna()
    n = min(len(x), len(y))
    if n < 2:
        return None, None, n
    x = x.iloc[:n]
    y = y.iloc[:n]
    mean_x, mean_y = x.mean(), y.mean()
    std_x,  std_y  = x.std(ddof=1), y.std(ddof=1)
    if std_x == 0 or std_y == 0:
        return None, None, n
    r = ((x - mean_x) * (y - mean_y)).sum() / ((n - 1) * std_x * std_y)
    return round(float(r), 6), n


def interpret_r(r):
    """Interpreta el valor de r en texto."""
    if r is None:
        return "Sin datos suficientes"
    abs_r = abs(r)
    direction = "positiva" if r >= 0 else "negativa"
    if abs_r < 0.10:
        strength = "nula o despreciable"
    elif abs_r < 0.30:
        strength = "débil"
    elif abs_r < 0.50:
        strength = "moderada"
    elif abs_r < 0.70:
        strength = "fuerte"
    else:
        strength = "muy fuerte"
    return f"Correlación {direction} {strength} (r = {r:.4f})"


def compute_indicators(df_tasks: pd.DataFrame, student_summary: pd.DataFrame) -> dict:
    """
    Recibe el DataFrame de tareas limpio y el resumen por estudiante.
    Devuelve un dict con todos los indicadores calculados.
    """
    print("=" * 55)
    print("  INDICATORS PHASE")
    print("=" * 55)

    result = {}

    # ── 1. Estadísticas generales de tareas ───────────────────────────────────
    total = len(df_tasks)
    done  = (df_tasks["status"] == "done").sum() if "status" in df_tasks.columns else 0
    result["total_tasks"]     = int(total)
    result["completed_tasks"] = int(done)
    result["completion_rate"] = round(done / total, 4) if total > 0 else 0

    print(f"[INDICATORS] Total tareas   : {total}")
    print(f"[INDICATORS] Completadas    : {done}")
    print(f"[INDICATORS] Tasa completado: {result['completion_rate']:.1%}")

    # ── 2. Distribución de cargas activas ─────────────────────────────────────
    if "active_at_ref" in student_summary.columns:
        result["active_assignments_mean"] = round(student_summary["active_at_ref"].mean(), 2)
        result["active_assignments_max"]  = int(student_summary["active_at_ref"].max())
        result["active_assignments_min"]  = int(student_summary["active_at_ref"].min())
        print(f"[INDICATORS] Tareas activas (promedio): {result['active_assignments_mean']}")
        print(f"[INDICATORS] Tareas activas (rango)  : {result['active_assignments_min']} – {result['active_assignments_max']}")

    # ── 3. Correlación de Pearson: P4 ─────────────────────────────────────────
    if "active_at_ref" in student_summary.columns and "on_time_rate" in student_summary.columns:
        r, n = pearson_r(student_summary["active_at_ref"], student_summary["on_time_rate"])
        interpretation = interpret_r(r)
        result["pearson_r"]             = r
        result["pearson_n"]             = n
        result["pearson_interpretation"]= interpretation

        print(f"\n[INDICATORS] ─── RESULTADO P4 ───")
        print(f"  Variable X : active_at_ref  (tareas activas simultáneas)")
        print(f"  Variable Y : on_time_rate   (porcentaje de entregas a tiempo)")
        print(f"  n          : {n} estudiantes")
        print(f"  r de Pearson: {r}")
        print(f"  Interpretación: {interpretation}")
    else:
        result["pearson_r"] = None
        result["pearson_n"] = 0
        result["pearson_interpretation"] = "Columnas necesarias no encontradas"
        print("[INDICATORS] WARNING: No se pudo calcular correlación — columnas faltantes.")

    # ── 4. Tabla detalle estudiantes ──────────────────────────────────────────
    result["student_summary"] = student_summary.to_dict(orient="records")

    print("\n[INDICATORS] Detalle por estudiante:")
    cols = [c for c in ["student_id","student_name","total_tasks","active_at_ref",
                         "completed_tasks","on_time_count","on_time_rate"] if c in student_summary.columns]
    print(student_summary[cols].to_string(index=False))
    print()

    return result
