# ETL — Assignment Submission Tracker (Q3)

**Autora:** Dalila de los Ángeles Ku Dzul  
**Proyecto:** Platform Design — UPY  
**Pregunta de investigación:** Do high-priority assignments get completed earlier, on average, than medium- and low-priority assignments?

---

## Estructura

```
ETL_Dalila/
├── main.py              # Orquestador del pipeline
├── requirements.txt
├── README.md
├── outputs/             # Resultados generados automáticamente
│   ├── tasks_clean.csv
│   ├── priority_summary.csv
│   ├── indicators_report.xlsx
│   └── indicators.json
└── UTILS/
    ├── __init__.py
    ├── extract.py       # EXTRACT: CSV de GitHub
    ├── transform.py     # TRANSFORM: limpieza + completion_days por prioridad
    ├── indicators.py    # INDICATORS: promedio días por nivel de prioridad
    └── load.py          # LOAD: CSV, Excel y JSON
```

---

## Fuentes de datos

| # | Fuente | URL |
|---|--------|-----|
| 1 | tasks_sample.csv | `db_files/dalila/data/tasks_sample.csv` (GitHub) |
| 2 | users.csv | `db_files/esau/data/users.csv` (GitHub — roster compartido del equipo) |

Si no hay conexión, el pipeline usa datos de fallback incorporados.

La segunda fuente (equipo/usuarios) se limpia en TRANSFORM (normalización de columnas,
deduplicado, email/rol en minúsculas) y se usa en INDICATORS para reportar tamaño de
equipo y distribución de roles; se exporta también en `outputs/users_clean.csv` y en
una hoja separada del Excel.

---

## Variable del indicador Q3

| Variable | Columna | Descripción |
|----------|---------|-------------|
| X | `priority` | Nivel de prioridad (high / medium / low) |
| Y | `completion_days` | Días entre `assignment_date` y `completed_date` |

**Indicador:** Promedio de `completion_days` agrupado por `priority`.  
Si `avg(high) < avg(medium/low)` → las tareas de alta prioridad se completan antes.

---

## Ejecución

```bash
# Instalar dependencias (una sola vez)
pip install -r requirements.txt

# Correr el pipeline
python main.py
```

Los resultados quedan en `outputs/`.
