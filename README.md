# Platform_Design — Assignment Submission Tracker

Repositorio del **Equipo Yucateco Unido** para el proyecto **Platform Design & GitHub Repository**.

**Platform_Design** es una plataforma académica para gestionar proyectos, tareas, asignaciones, usuarios, estados de avance y fechas de entrega. El repositorio integra una base de datos SQLite, archivos de muestra, diseño de API REST, formularios frontend, scripts de generación de datos y pipelines ETL para analizar el comportamiento de entrega de asignaciones.

---

## Objective

Design and implement the data infrastructure of a shared platform that supports ETL analysis about assignment progress, student interaction, deadlines, and on-time submissions.

The repository includes:

- Database schema.
- Sample data files in CSV and JSON.
- Data generation scripts.
- API endpoint documentation.
- Frontend form prototype.
- ETL pipelines.
- GitHub Actions validation workflow.
- Technical documentation.

---

## Team and Roles

| Member | Role | Branch |
|---|---|---|
| Dalila Ku | Data Generation / Sample Data | `dalila/generacion-datos` |
| Esaú Palomo | Database Design / ETL Pipeline | `esau/diseno-base-datos` |
| Yeimy Piste | API REST Design | `yeimy/diseno-api` |
| Gael Lara | Frontend / Forms | `gael/frontend-diseno-formulario` |
| Ingrid Castillo | Documentation / ETL Pipeline | `ingrid/documentacion` |

---

## Repository Structure

```text
Platform_Design/
├── README.md
├── documentation.md
├── Dockerfile
├── docker-compose.yml
├── app.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── deploy.yml
├── db_files/
│   ├── generate_data.py
│   ├── generated_data.sql
│   ├── esau/
│   │   ├── README.md
│   │   ├── schema.sql
│   │   ├── sample_data.sql
│   │   └── data/
│   │       ├── users.csv
│   │       ├── projects.csv
│   │       ├── tasks.csv
│   │       ├── sample_data.json
│   │       └── sample_data.xlsx
│   ├── dalila/
│   │   └── data/
│   │       ├── tasks_sample.csv
│   │       └── tasks_sample.json
│   ├── yeimy/
│   │   └── api_endpoints.md
│   └── gael/
│       ├── README.md
│       └── project_form.html
├── ETL/
│   ├── main.py
│   ├── requirements.txt
│   ├── README.md
│   ├── outputs/
│   └── UTILS/
└── ETL_ingrid/
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── outputs/
    └── utils/
```

---

## Main Data Sources

The platform currently uses the following shared data sources:

| Source | Path | Description |
|---|---|---|
| SQLite schema | `db_files/esau/schema.sql` | Defines the database structure. |
| SQLite sample data | `db_files/esau/sample_data.sql` | Inserts initial platform records. |
| Users CSV | `db_files/esau/data/users.csv` | User/student reference data. |
| Tasks CSV | `db_files/esau/data/tasks.csv` | Assignment/task records. |
| Tasks sample CSV | `db_files/dalila/data/tasks_sample.csv` | Sample assignment dataset for ETL analysis. |
| Tasks sample JSON | `db_files/dalila/data/tasks_sample.json` | JSON version of the sample assignment dataset. |

---

## Database

The database is designed in **SQLite** and supports the core entities of the platform.

Main tables:

- `users`
- `projects`
- `milestones`
- `tasks`
- `project_members`
- `task_assignments`
- `comments`
- `tags`
- `task_tags`

The `tasks` table includes fields used for ETL analysis:

- `assignment_date`
- `start_date`
- `due_date`
- `completed_date`
- `status`
- `priority`
- `difficulty`
- `estimated_hours`
- `actual_hours`

These fields allow the team to analyze questions related to early starts, on-time submissions, active workload, priority level, dashboard activity, and status updates.

---

## API REST Design

The API documentation is located at:

```text
db_files/yeimy/api_endpoints.md
```

The proposed base URL is:

```text
http://localhost:3000/api/v1
```

Main endpoint groups:

- Authentication
- Users
- Projects
- Tasks
- Milestones
- Comments
- Tags

---

## Frontend Prototype

The frontend form prototype is located at:

```text
db_files/gael/project_form.html
```

It provides a static HTML interface for capturing project and task information. It also prepares JSON-style payloads for future API integration.

---

## ETL Pipelines

The repository includes ETL work for analyzing assignment behavior.

Current ETL modules:

```text
ETL/
ETL_ingrid/
```

Each ETL pipeline follows the same general structure:

1. Extract data from at least two platform sources.
2. Clean and standardize columns.
3. Transform records into analytical variables.
4. Calculate indicators.
5. Export final outputs.

Generated outputs may include:

- Clean CSV datasets.
- Excel reports.
- JSON indicator files.
- Summary tables.

---

## Research Questions

The team analyzes the shared platform from different perspectives:

| Member | Research Question | Indicator |
|---|---|---|
| Gael | Do students who start working on assignments within 24 hours of receiving them have a higher on-time submission rate than students who start later? | Mean on-time submission rate by early-start group. |
| Ingrid | Is there a relationship between the number of assignment status updates and the likelihood of submitting before the deadline? | Pearson correlation between status update count and on-time rate. |
| Dalila | Do high-priority assignments get completed earlier than medium- and low-priority assignments? | Mean completion time by priority level. |
| Esaú | Is there a relationship between active assignment count and on-time submission percentage? | Pearson correlation between active assignment count and on-time rate. |
| Yeimy | Do students who regularly check the dashboard submit a higher percentage of assignments on time? | Mean on-time submission rate by dashboard access frequency. |

---

## How to Run Locally

### Requirements

- Python 3.8+
- SQLite
- pip
- Optional: Docker

---

### 1. Clone the repository

```bash
git clone https://github.com/Dalila-Ku/Platform_Design.git
cd Platform_Design
```

---

### 2. Create the SQLite database

Using SQLite CLI:

```bash
sqlite3 platform.db < db_files/esau/schema.sql
sqlite3 platform.db < db_files/esau/sample_data.sql
```

Using Python:

```bash
python - <<'PY'
import sqlite3

conn = sqlite3.connect("platform.db")
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript(open("db_files/esau/schema.sql", encoding="utf-8").read())
conn.executescript(open("db_files/esau/sample_data.sql", encoding="utf-8").read())
conn.close()

print("Database created successfully: platform.db")
PY
```

---

### 3. Run the data generation script

```bash
pip install faker
cd db_files
python generate_data.py
cd ..
```

This generates:

```text
db_files/generated_data.sql
```

---

### 4. Open the frontend prototype

Open this file directly in a browser:

```text
db_files/gael/project_form.html
```

---

### 5. Run the ETL pipeline

For the ETL module:

```bash
pip install -r ETL/requirements.txt
python ETL/main.py
```

For Ingrid's ETL module:

```bash
pip install -r ETL_ingrid/requirements.txt
python ETL_ingrid/main.py
```

Outputs are saved inside each pipeline's `outputs/` folder.

---

### 6. Run with Docker

If Docker is available:

```bash
docker-compose up --build
```

---

## GitHub Actions

The workflow located at:

```text
.github/workflows/deploy.yml
```

validates the platform skeleton by checking:

- Database schema.
- Sample data loading.
- Required CSV/JSON files.
- API documentation file.
- Frontend file.
- Data generation script.

---
