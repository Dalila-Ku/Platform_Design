# ETL — Assignment Submission Tracker (P4)

**Autor:** Esaú Palomo  
**Proyecto:** Platform Design — UPY  
**Pregunta de investigación:** ¿Existe relación entre el número de tareas activas de un estudiante en un momento dado y su porcentaje de entregas a tiempo?

---

## Estructura

```
ETL/
├── main.py              # Orquestador del pipeline
├── requirements.txt     # Dependencias Python
├── README.md
├── outputs/             # Resultados generados automáticamente
│   ├── tasks_clean.csv
│   ├── student_summary.csv
│   ├── indicators_report.xlsx
│   └── indicators.json
└── UTILS/
    ├── __init__.py
    ├── extract.py       # EXTRACT: SQLite + CSV de GitHub
    ├── transform.py     # TRANSFORM: limpieza, fechas, columnas derivadas
    ├── indicators.py    # INDICATORS: correlación de Pearson (P4)
    └── load.py          # LOAD: exporta CSV, Excel y JSON
```

---

## Fuentes de datos

| # | Fuente | Tipo | Descripción |
|---|--------|------|-------------|
| 1 | `platform.db` | SQLite local | Tareas de la plataforma (Flask app) |
| 2 | `tasks_sample.csv` | CSV / GitHub | Datos de muestra del repo compartido |

Si la fuente principal no está disponible, el pipeline usa datos de fallback incorporados para no interrumpir la ejecución.

---

## Variables del indicador P4

| Variable | Columna | Descripción |
|----------|---------|-------------|
| X | `active_at_ref` | Número de tareas activas simultáneas el 2026-06-10 |
| Y | `on_time_rate` | Porcentaje de tareas entregadas antes o en la fecha límite |

**Indicador estadístico:** Correlación de Pearson (r)

| Rango |r|| Interpretación |
|----------|----------------|
| 0.00–0.10 | Nula o despreciable |
| 0.10–0.30 | Débil |
| 0.30–0.50 | Moderada |
| 0.50–0.70 | Fuerte |
| 0.70–1.00 | Muy fuerte |

---

## Ejecución

```bash
# Instalar dependencias (una sola vez)
pip install -r ETL/requirements.txt

# Ejecutar el pipeline desde la raíz del repositorio
python ETL/main.py
```

Los resultados quedan en `ETL/outputs/`.

---

## Columnas derivadas (TRANSFORM)

| Columna | Fórmula |
|---------|---------|
| `is_active_at_ref` | `assignment_date ≤ ref_date ≤ due_date AND status ∉ {done, cancelled}` |
| `on_time` | `status = done AND completed_date ≤ due_date` |
| `days_to_start` | `start_date − assignment_date` (días) |
| `days_vs_deadline` | `completed_date − due_date` (negativo = antes de tiempo) |
