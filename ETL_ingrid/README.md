# ETL — Assignment Status Updates Tracker

**Autora:** Ingrid Castillo  
**Proyecto:** Platform Design — UPY  
**Pregunta de investigación:** ¿Existe relación entre el número de actualizaciones de estado de una tarea y la probabilidad de que se entregue antes de la fecha límite?

---

## Estructura

```
ETL_ingrid/
├── main.py              # Orquestador del pipeline
├── requirements.txt     # Dependencias Python
├── README.md
├── schema.sql            # Esquema de la BD (equipo)
├── generated_data.sql    # Datos semilla (equipo)
├── outputs/             # Resultados generados automáticamente
│   ├── tasks_clean.csv
│   ├── student_summary.csv
│   ├── indicators_report.xlsx
│   └── indicators.json
└── utils/
    ├── __init__.py
    ├── extract.py       # EXTRACT: SQLite (tasks) + log de actividad JSON
    ├── transform.py     # TRANSFORM: limpieza, fechas, columnas derivadas
    ├── indicators.py    # INDICATORS: correlación y tasas de entrega a tiempo
    └── load.py          # LOAD: exporta CSV, Excel y JSON
```

---

## Fuentes de datos

| # | Fuente | Tipo | Descripción |
|---|--------|------|-------------|
| 1 | `platform.db` | SQLite local | Tabla `tasks` de la plataforma (base de datos oficial del equipo) |
| 2 | `status_activity_log.json` | JSON | Log de actividad de cambios de estado por tarea |

La plataforma todavía no registra un historial de estados (`comments` está vacía y no existe `status_history`), así que la fuente 2 se genera automáticamente la primera vez que corre el pipeline, simulando lo que emitiría un microservicio de auditoría — ver el docstring de `utils/extract.py` para el detalle completo.

---

## Variables del indicador

| Variable | Columna | Descripción |
|----------|---------|-------------|
| X | `status_update_count` | Número de actualizaciones de estado registradas para la tarea |
| Y | `submitted_on_time` | `True` si la tarea se completó antes o en la fecha límite, `False` si fue tarde (solo aplica a tareas con `status = done`) |

**Indicador estadístico:** Correlación (status_update_count vs. submitted_on_time como 0/1)

| Rango \|r\| | Interpretación |
|----------|----------------|
| 0.00–0.10 | Nula o despreciable |
| 0.10–0.30 | Débil |
| 0.30–0.50 | Moderada |
| 0.50–0.70 | Fuerte |
| 0.70–1.00 | Muy fuerte |

> ⚠️ Con el dataset de 20 tareas de `generated_data.sql` solo hay 3 casos evaluables (status='done'), por lo que la correlación puede salir `N/A` por falta de variación. Se recomienda regenerar con 150–300 tareas antes de la entrega final.

---

## Ejecución

```bash
# Instalar dependencias (una sola vez)
pip install -r ETL_ingrid/requirements.txt

# Ejecutar el pipeline desde la raíz del repositorio
python ETL_ingrid/main.py
```

Los resultados quedan en `ETL_ingrid/outputs/`. `platform.db` y `status_activity_log.json` se generan solos si no existen.

---

## Columnas derivadas (TRANSFORM)

| Columna | Fórmula |
|---------|---------|
| `status_update_count` | Conteo de eventos en `status_activity_log.json` agrupados por `task_id` |
| `submitted_on_time` | `status = done AND completed_date ≤ due_date` |
| `update_bucket` | Rango categórico de `status_update_count`: Baja (0–2), Media (3–4), Alta (5+) |

---

## Salidas (`outputs/`)

| Archivo | Contenido |
|---------|-----------|
| `tasks_clean.csv` | Dataset final a nivel tarea con todas las columnas derivadas |
| `student_summary.csv` | Resumen por usuario asignado: total de tareas, promedio de actualizaciones, % de entregas a tiempo |
| `indicators.json` | Indicadores agregados: tasa global, correlación, promedios por grupo |
| `indicators_report.xlsx` | Mismo contenido en Excel, en 4 hojas (`overview`, `tasks_clean`, `student_summary`, `rate_by_bucket`) |