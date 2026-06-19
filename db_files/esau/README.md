# Diseño de Base de Datos — Platform_Design

**Autor:** Esaú Palomo  
**Rol:** Diseño de Base de Datos  
**Rama:** `esau/diseno-base-datos`  
**Plataforma:** Gestor de Proyectos (Project Management System)

## Descripción

Este módulo contiene el esquema relacional para la plataforma de gestión de proyectos del equipo Yucateco Unido. La base de datos fue diseñada en SQLite y puede migrarse a MySQL o PostgreSQL con cambios mínimos en los tipos de datos.

El modelo soporta proyectos con múltiples miembros, tareas jerarquicas (subtareas), hitos, asignaciones, comentarios y etiquetas.

## Archivos

| Archivo | Descripción |
|---|---|
| `schema.sql` | Definición de tablas, relaciones, restricciones e índices |
| `sample_data.sql` | Datos de ejemplo listos para insertar (ejecutar después de schema.sql) |

## Diagrama de Relaciones

```
users ──< project_members >── projects ──< milestones
                                      └──< tasks ──< task_assignments >── users
                                                └──< comments
                                                └──< task_tags >── tags
tasks ──< tasks (subtareas via parent_task_id)
```

## Tablas

- **users** — Usuarios del sistema con rol global: `admin`, `leader` o `member`
- **projects** — Proyectos con estado (`active`, `on_hold`, `completed`, `cancelled`) y prioridad
- **milestones** — Hitos/entregables dentro de un proyecto con fecha límite
- **tasks** — Tareas con estado, prioridad, horas estimadas y soporte de subtareas
- **project_members** — Relación usuarios-proyectos con rol dentro del proyecto
- **task_assignments** — Qué usuarios tienen asignada cada tarea
- **comments** — Comentarios asociados a tareas o proyectos
- **tags** — Etiquetas reutilizables con color personalizado
- **task_tags** — Relación muchos-a-muchos entre tareas y etiquetas

## Cómo ejecutar

```bash
# Crear la base de datos desde cero
sqlite3 platform.db < schema.sql
sqlite3 platform.db < sample_data.sql

# Verificar tablas creadas
sqlite3 platform.db ".tables"

# Consulta de ejemplo: tareas pendientes con su proyecto y responsable
sqlite3 platform.db "
SELECT t.title, p.name AS proyecto, u.full_name AS asignado, t.status, t.due_date
FROM tasks t
JOIN projects p ON t.project_id = p.project_id
JOIN task_assignments ta ON t.task_id = ta.task_id
JOIN users u ON ta.user_id = u.user_id
WHERE t.status != 'done'
ORDER BY t.due_date ASC;
"
```

## Notas de diseño

- `tasks.parent_task_id` permite crear subtareas sin necesidad de una tabla separada.
- `comments` puede asociarse a una tarea (`task_id`) o directamente a un proyecto (`project_id`), no necesariamente a los dos.
- Los índices cubren los campos más consultados: `status`, `due_date`, `priority` y `project_id`.
- `ON DELETE CASCADE` en tareas y miembros garantiza integridad al eliminar un proyecto.
