# Platform_Design — Project Management Platform

Repository for **Project #06 — Platform Design & GitHub Repository**.

This project contains the working skeleton of a collaborative project management platform. The platform is designed to manage projects, tasks, milestones, users, comments, and tags through a shared data infrastructure.

---

## Project Objective

Design the data infrastructure of the shared platform and deliver a working skeleton ready for review and deployment.

The repository includes:

- Database schema
- API endpoint design
- Data generation scripts
- Sample data files
- Frontend form prototype
- Technical documentation
- GitHub Actions workflow

---

## Team and Roles

| Member | Role | Branch |
|---|---|---|
| Dalila Ku | Data Generation | `dalila/generacion-datos` |
| Esaú Palomo | Database Design | `esau/diseno-base-datos` |
| Yeimy Piste | API Design | `yeimy/diseno-api` |
| Gael Lara | Frontend / Forms | `gael/frontend-diseno-formulario` |
| Ingrid Castillo | Documentation | `ingrid/documentacion` |

---

## Repository Structure

```text
Platform_Design/
├── README.md
├── documentation.md
├── .github/
│   └── workflows/
│       └── deploy.yml
└── db_files/
    ├── esau/
    │   ├── schema.sql
    │   ├── sample_data.sql
    │   └── data/
    ├── yeimy/
    │   └── api_endpoints.md
    ├── gael/
    │   ├── README.md
    │   └── project_form.html
    └── generate_data.py
