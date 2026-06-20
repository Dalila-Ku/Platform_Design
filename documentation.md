# Documentación Técnica — Platform_Design

**Autora:** Ingrid Castillo  
**Rol:** Documentación  
**Rama:** `ingrid/documentacion`  
**Plataforma:** Gestor de Proyectos (Project Management System)

---

## Descripción del Proyecto

**Platform_Design** es una plataforma web colaborativa para la gestión de proyectos. Permite a equipos de trabajo crear proyectos, asignar tareas, dar seguimiento a hitos y comunicarse mediante comentarios. Fue desarrollada como proyecto académico por el Equipo Yucateco Unido de la UPY.

---

## Integrantes del Equipo

| Nombre | Correo | Rol | Rama |
|--------|--------|-----|------|
| Dalila Ku | dalila.ku.dzul@gmail.com | Generación de Datos | `dalila/generacion-datos` |
| Esaú Palomo | Esau_palomo@hotmail.com | Diseño de Base de Datos | `esau/diseno-base-datos` |
| Yeimi Piste | yeimypiste@gmail.com | Diseño de API | `yelmy/diseno-api` |
| Gael Pérez | glape245@gmail.com | Frontend / Formularios | `gael/frontend-diseno-formulario` |
| Ingrid Castillo | jazcastillo0609@gmail.com | Documentación | `ingrid/documentacion` |

---

## Arquitectura General

```
┌─────────────────────────────────────────────┐
│              Cliente (Browser)              │
│         Formularios HTML (Gael)             │
└──────────────┬──────────────────────────────┘
               │ HTTP / JSON
┌──────────────▼──────────────────────────────┐
│              API REST (Yeimi)               │
│    Endpoints: /projects /tasks /users ...   │
│    Autenticación: JWT                       │
└──────────────┬──────────────────────────────┘
               │ SQL
┌──────────────▼──────────────────────────────┐
│         Base de Datos SQLite (Esaú)         │
│    9 tablas: users, projects, tasks,        │
│    milestones, comments, tags, ...          │
└─────────────────────────────────────────────┘
               ▲
               │ Scripts de datos
┌──────────────┴──────────────────────────────┐
│     Generación de Datos (Dalila)            │
│     generate_data.py → generated_data.sql   │
└─────────────────────────────────────────────┘
```

---

## Estructura del Repositorio

```
Platform_Design/
└── db_files/
    ├── esau/
    │   ├── schema.sql          ← Esquema de la BD (tablas, índices, FK)
    │   ├── sample_data.sql     ← Datos de ejemplo del equipo
    │   └── README.md           ← Notas del módulo de BD
    ├── yeimi/
    │   └── api_endpoints.md    ← Diseño de endpoints REST
    ├── gael/
    │   └── project_form.html   ← Formularios de proyectos y tareas
    ├── dalila/
    │   └── generate_data.py    ← Script para generar datos de prueba
    └── ingrid/
        └── DOCUMENTATION.md    ← Este archivo
```

---

## Base de Datos

### Tablas principales

**users** — Usuarios del sistema con rol global (`admin`, `leader`, `member`).

**projects** — Proyectos con nombre, descripción, estado (`active`, `on_hold`, `completed`, `cancelled`) y prioridad (`low`, `medium`, `high`, `critical`).

**milestones** — Hitos o entregables dentro de un proyecto, con fecha límite y estado de completado.

**tasks** — Tareas individuales dentro de un proyecto. Soportan subtareas mediante `parent_task_id`. Tienen estado (`todo`, `in_progress`, `in_review`, `done`, `cancelled`) y prioridad.

**project_members** — Relación entre usuarios y proyectos con rol dentro del proyecto (`leader`, `contributor`, `viewer`).

**task_assignments** — Usuarios asignados a tareas específicas.

**comments** — Comentarios en tareas o proyectos.

**tags** — Etiquetas con color personalizado.

**task_tags** — Relación muchos-a-muchos entre tareas y etiquetas.

---

## API

La API REST fue diseñada por Yeimi Piste. Los endpoints principales son:

- `POST /auth/login` — Autenticación con JWT
- `GET/POST /projects` — Listar o crear proyectos
- `GET/POST /projects/:id/tasks` — Tareas de un proyecto
- `GET/POST /projects/:id/milestones` — Hitos de un proyecto
- `POST /tasks/:id/assign` — Asignar usuario a tarea
- `GET/POST /tasks/:id/comments` — Comentarios de una tarea

Para la documentación completa ver `yeimi/api_endpoints.md`.

---

## Cómo ejecutar en local

### 1. Crear la base de datos

```bash
# Opción A: con sqlite3 CLI
sqlite3 platform.db < db_files/esau/schema.sql
sqlite3 platform.db < db_files/esau/sample_data.sql

# Opción B: con DB Browser for SQLite
# Archivo > Nuevo > Ejecutar SQL > pegar schema.sql > ejecutar
# Volver a Ejecutar SQL > pegar sample_data.sql > ejecutar
```

### 2. Generar datos adicionales (opcional)

```bash
cd db_files/dalila/
pip install faker
python generate_data.py
# Genera: generated_data.sql
sqlite3 ../../platform.db < generated_data.sql
```

### 3. Ver los formularios

Abrir `db_files/gael/project_form.html` en cualquier navegador. No requiere servidor.

---

## Prueba rápida en DB Browser for SQLite

1. Abrir DB Browser for SQLite
2. Archivo → Nueva Base de Datos → guardar como `platform.db`
3. Pestaña "Ejecutar SQL" → pegar contenido de `schema.sql` → clic en ▶
4. Pestaña "Ejecutar SQL" → pegar contenido de `sample_data.sql` → clic en ▶
5. Pestaña "Explorar datos" → revisar cada tabla

---

## Notas técnicas

- El motor es **SQLite** pero el schema es compatible con MySQL/PostgreSQL cambiando `INTEGER PRIMARY KEY AUTOINCREMENT` por `SERIAL PRIMARY KEY` y `TEXT` por `VARCHAR`.
- `PRAGMA foreign_keys = ON` es obligatorio en SQLite para que las llaves foráneas funcionen.
- Los índices creados cubren: `status`, `due_date`, `priority`, `project_id` en tasks; y `user_id` en project_members.
- Las fechas se almacenan como `TEXT` en formato `YYYY-MM-DD` para máxima compatibilidad.

---

## Control de versiones

El proyecto usa **Git** con ramas por integrante. Cada persona trabaja en su rama y los cambios se integran a `main` mediante Pull Requests revisados por el equipo.

Repositorio: [https://github.com/Dalila-Ku/Platform_Design](https://github.com/Dalila-Ku/Platform_Design)
