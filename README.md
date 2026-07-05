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
