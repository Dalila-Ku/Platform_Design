# ETL Gael — Project #08

## Research Question

Do students who start working on assignments within 24 hours of receiving them have a higher on-time submission rate than students who start later?

## Structure

```text
ETL_gael/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   ├── tasks_sample_seed.csv
│   └── users_seed.csv
├── outputs/
└── UTILS/
    ├── __init__.py
    ├── extract_platform.py
    ├── generate_synthetic.py
    ├── transform.py
    ├── indicators.py
    └── load.py
```

## Sources

The pipeline connects to two shared-platform sources from GitHub:

1. `db_files/dalila/data/tasks_sample.csv`
2. `db_files/esau/data/users.csv`

If GitHub is unavailable, local fallback files in `data/` are used so the demo can still run end to end.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Outputs

Generated in `outputs/`:

- `gael_final_assignment_dataset.csv`
- `gael_indicator_summary.csv`
- `gael_indicator_result.json`
- `gael_etl_report.xlsx`
