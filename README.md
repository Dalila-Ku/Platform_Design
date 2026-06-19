# Platform_Design — Gestor de Proyectos

Repositorio del **Equipo Yucateco Unido** — UPY, Octavo Cuatrimestre.

Plataforma web colaborativa para gestión de proyectos: creación de proyectos, asignación de tareas, seguimiento de hitos y comunicación por comentarios.

---

## Equipo y Roles

| Nombre | Correo | Rol | Rama |
|--------|--------|-----|------|
| Dalila Ku | dalila.ku.dzul@gmail.com | Generación de Datos | `dalila/generacion-datos` |
| Esaú Palomo | Esau_palomo@hotmail.com | Diseño de Base de Datos | `esau/diseno-base-datos` |
| Yeimi Piste | yeimypiste@gmail.com | Diseño de API | `yelmy/diseno-api` |
| Gael Pérez | glape245@gmail.com | Frontend / Formularios | `gael/frontend-diseno-formulario` |
| Ingrid Castillo | jazcastillo0609@gmail.com | Documentación | `ingrid/documentacion` |

---

## Estructura del Repositorio

```
Platform_Design/
├── README.md                        ← Este archivo
├── .github/
│   └── workflows/
│       └── deploy.yml               ← GitHub Actions (CI/CD)
└── db_files/
    ├── esau/                        ← Diseño de Base de Datos
    │   ├── schema.sql               ← Esquema completo (9 tablas + índices)
    │   ├── sample_data.sql          ← Datos de ejemplo (INSERT)
    │   └── data/
    │       ├── users.csv
    │       ├── projects.csv
    │       ├── tasks.csv
    │       └── sample_data.json
    ├── yeimi/                       ← Diseño de API REST
    │   └── api_endpoints.md
    ├── gael/                        ← Frontend / Formularios
    │   └── project_form.html
    ├── dalila/                      ← Generación de Datos
    │   └── generate_data.py
    └── ingrid/                      ← Documentación
        └── DOCUMENTATION.md
```

---

## Base de Datos

Motor: **SQLite** (compatible con MySQL/PostgreSQL con ajustes mínimos).

### Tablas

| Tabla | Descripción |
|-------|-------------|
| `users` | Usuarios con rol: `admin`, `leader`, `member` |
| `projects` | Proyectos con estado y prioridad |
| `milestones` | Hitos/entregables por proyecto |
| `tasks` | Tareas con soporte de subtareas |
| `project_members` | Miembros por proyecto con su rol |
| `task_assignments` | Asignaciones de tareas a usuarios |
| `comments` | Comentarios en tareas o proyectos |
| `tags` | Etiquetas con color personalizado |
| `task_tags` | Relación tareas ↔ etiquetas |

### Diagrama simplificado

```
users ──< project_members >── projects ──< milestones
                                      └──< tasks ──< task_assignments >── users
                                                └──< comments
                                                └──< task_tags >── tags
```

---

## Cómo correr localmente

### Requisitos
- Python 3.8+
- SQLite (incluido en Python)
- Navegador web moderno

### 1. Clonar el repositorio

```bash
git clone https://github.com/Dalila-Ku/Platform_Design.git
cd Platform_Design
```

### 2. Crear la base de datos

```bash
# Con Python (recomendado)
python3 -c "
import sqlite3
conn = sqlite3.connect('platform.db')
conn.executescript(open('db_files/esau/schema.sql').read())
conn.executescript(open('db_files/esau/sample_data.sql').read())
conn.close()
print('Base de datos lista: platform.db')
"
```

O con DB Browser for SQLite:
1. Archivo → Nueva Base de Datos → guardar como `platform.db`
2. Execute SQL → pegar `schema.sql` → ▶
3. Execute SQL → pegar `sample_data.sql` → ▶

### 3. Generar datos adicionales (opcional)

```bash
cd db_files/dalila
pip install faker
python generate_data.py
# Genera: generated_data.sql
```

### 4. Ver formularios

Abrir `db_files/gael/project_form.html` en el navegador — no requiere servidor.

### 5. Consultar la API

Ver `db_files/yeimi/api_endpoints.md` para la especificación completa de endpoints.

---

## API

Base URL: `http://localhost:3000/api/v1`  
Autenticación: JWT (`Authorization: Bearer <token>`)

Endpoints principales:
- `POST /auth/login` — Autenticación
- `GET/POST /projects` — Proyectos
- `GET/POST /projects/:id/tasks` — Tareas
- `GET/POST /projects/:id/milestones` — Hitos
- `POST /tasks/:id/comments` — Comentarios

Documentación completa: [`db_files/yeimi/api_endpoints.md`](db_files/yeimi/api_endpoints.md)

---

## GitHub Actions

El workflow en `.github/workflows/deploy.yml` valida automáticamente el schema de la base de datos al hacer push a `main`.

---

## Tecnologías

- **Base de datos:** SQLite / PostgreSQL
- **Backend:** API REST con JWT
- **Frontend:** HTML5, CSS3, JavaScript
- **Generación de datos:** Python + Faker
- **Control de versiones:** Git + GitHub
