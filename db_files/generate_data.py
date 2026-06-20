# -*- coding: utf-8 -*-
# ============================================================
#  Platform_Design — Generación de Datos de Ejemplo
#  Autora: Dalila Ku | Rol: Generación de Datos
#  Rama: dalila/generacion-datos
#  Plataforma: Gestor de Proyectos
#
#  Uso:
#    pip install faker
#    python generate_data.py
#
#  Genera: generated_data.sql listo para ejecutar despues de schema.sql
# ============================================================

import random
from datetime import datetime, timedelta

try:
    from faker import Faker
    fake = Faker('es_MX')
    USE_FAKER = True
except ImportError:
    USE_FAKER = False
    print("Faker no instalado. Usando datos estaticos de ejemplo.")

# ── Configuración ──────────────────────────────────────────
NUM_USERS    = 10
NUM_PROJECTS = 5
NUM_TASKS    = 20
OUTPUT_FILE  = "generated_data.sql"

# ── Datos estáticos del equipo (siempre incluidos) ─────────
TEAM = [
    ("Dalila Ku",       "dalila.ku.dzul@gmail.com",  "admin"),
    ("Esau Palomo",     "Esau_palomo@hotmail.com",   "leader"),
    ("Yeimi Piste",     "yeimypiste@gmail.com",       "member"),
    ("Gael Perez",      "glape245@gmail.com",         "member"),
    ("Ingrid Castillo", "jazcastillo0609@gmail.com",  "member"),
]

STATUSES_PROJECT = ["active", "on_hold", "completed", "cancelled"]
STATUSES_TASK    = ["todo", "in_progress", "in_review", "done", "cancelled"]
PRIORITIES       = ["low", "medium", "high", "critical"]
ROLES_PROJECT    = ["leader", "contributor", "viewer"]
TAG_NAMES        = ["backend", "frontend", "base-datos", "urgente", "revision",
                    "bug", "feature", "documentacion", "pruebas", "despliegue"]
TAG_COLORS       = ["#0d6efd", "#6f42c1", "#198754", "#dc3545", "#fd7e14",
                    "#20c997", "#0dcaf0", "#ffc107", "#6c757d", "#d63384"]

def rand_date(start_days_ago=60, span_days=120):
    base = datetime.now() - timedelta(days=start_days_ago)
    return (base + timedelta(days=random.randint(0, span_days))).strftime("%Y-%m-%d")

def esc(s):
    return s.replace("'", "''")

# ── Generar SQL ────────────────────────────────────────────
lines = [
    "-- ============================================================",
    "--  Platform_Design — Datos Generados Automaticamente",
    f"--  Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "--  Autora: Dalila Ku | generacion-datos",
    "-- ============================================================",
    "",
    "PRAGMA foreign_keys = ON;",
    "",
    "-- Usuarios del equipo",
]

for name, email, role in TEAM:
    lines.append(f"INSERT INTO users (full_name, email, role) VALUES ('{esc(name)}', '{email}', '{role}');")

# Usuarios extra generados
if USE_FAKER:
    lines.append("")
    lines.append("-- Usuarios adicionales generados")
    for i in range(NUM_USERS):
        name  = esc(fake.name())
        email = fake.email()
        role  = random.choice(["member", "member", "member", "leader"])
        lines.append(f"INSERT INTO users (full_name, email, role) VALUES ('{name}', '{email}', '{role}');")

# Tags
lines += ["", "-- Etiquetas"]
for i, (tag, color) in enumerate(zip(TAG_NAMES, TAG_COLORS)):
    lines.append(f"INSERT INTO tags (name, color) VALUES ('{tag}', '{color}');")

# Proyectos
lines += ["", "-- Proyectos"]
project_names = [
    "Plataforma Web Equipo Yucateco",
    "Rediseno de API REST",
    "Migracion de Base de Datos",
    "App Movil de Seguimiento",
    "Portal de Reportes",
]
for i, pname in enumerate(project_names):
    status   = random.choice(STATUSES_PROJECT)
    priority = random.choice(PRIORITIES)
    owner    = random.randint(1, len(TEAM))
    sd       = rand_date(60, 30)
    dd       = rand_date(0, 90)
    desc     = f"Proyecto {i+1} del gestor de proyectos del equipo."
    lines.append(
        f"INSERT INTO projects (name, description, status, priority, start_date, due_date, owner_id) "
        f"VALUES ('{esc(pname)}', '{desc}', '{status}', '{priority}', '{sd}', '{dd}', {owner});"
    )

# Miembros de proyecto
lines += ["", "-- Miembros de proyectos"]
for p in range(1, NUM_PROJECTS + 1):
    members = random.sample(range(1, len(TEAM) + 1), k=random.randint(2, len(TEAM)))
    for j, uid in enumerate(members):
        role = "leader" if j == 0 else random.choice(["contributor", "contributor", "viewer"])
        lines.append(
            f"INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) "
            f"VALUES ({p}, {uid}, '{role}');"
        )

# Tareas
lines += ["", "-- Tareas"]
task_titles = [
    "Disenar esquema de base de datos",
    "Implementar autenticacion JWT",
    "Crear formulario de registro",
    "Documentar endpoints de la API",
    "Pruebas unitarias del modulo de usuarios",
    "Configurar entorno de produccion",
    "Revisar pull requests del equipo",
    "Diseno de interfaz de dashboard",
    "Integracion con API externa",
    "Optimizar consultas SQL",
    "Crear script de migracion",
    "Actualizar dependencias del proyecto",
    "Disenar modelo de datos para reportes",
    "Implementar paginacion en endpoints",
    "Agregar validaciones de formularios",
    "Subir archivos al repositorio",
    "Revisar documentacion tecnica",
    "Crear datos de prueba",
    "Diseno de flujo de trabajo",
    "Presentacion del avance al equipo",
]
for i in range(NUM_TASKS):
    pid      = random.randint(1, NUM_PROJECTS)
    title    = esc(task_titles[i % len(task_titles)])
    status   = random.choice(STATUSES_TASK)
    priority = random.choice(PRIORITIES)
    due      = rand_date(0, 60)
    hours    = round(random.uniform(1, 8), 1)
    creator  = random.randint(1, len(TEAM))
    lines.append(
        f"INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) "
        f"VALUES ({pid}, '{title}', '{status}', '{priority}', '{due}', {hours}, {creator});"
    )

# Asignaciones
lines += ["", "-- Asignaciones de tareas"]
for i in range(1, NUM_TASKS + 1):
    uid = random.randint(1, len(TEAM))
    lines.append(
        f"INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) "
        f"VALUES ({i}, {uid}, 1);"
    )

# Tags en tareas
lines += ["", "-- Etiquetas en tareas"]
for i in range(1, NUM_TASKS + 1):
    used = random.sample(range(1, len(TAG_NAMES) + 1), k=random.randint(1, 3))
    for tag_id in used:
        lines.append(
            f"INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES ({i}, {tag_id});"
        )

lines += ["", "-- Fin del archivo generado"]

# ── Escribir archivo ───────────────────────────────────────
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Archivo generado: {OUTPUT_FILE}")
print(f"  Usuarios del equipo : {len(TEAM)}")
print(f"  Proyectos           : {NUM_PROJECTS}")
print(f"  Tareas              : {NUM_TASKS}")
print(f"  Tags                : {len(TAG_NAMES)}")
