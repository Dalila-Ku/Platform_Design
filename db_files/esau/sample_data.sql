-- ============================================================
--  Platform_Design — Datos de Ejemplo
--  Ejecutar DESPUES de schema.sql
--  Plataforma: Gestor de Proyectos
--  Autor: Esau Palomo | Rol: Diseno de Base de Datos
-- ============================================================

-- Usuarios reales del equipo
INSERT OR IGNORE INTO users (full_name, email, role) VALUES
    ('Dalila Ku',        'dalila.ku.dzul@gmail.com',  'admin'),
    ('Esau Palomo',      'Esau_palomo@hotmail.com',   'leader'),
    ('Yeimi Piste',      'yeimypiste@gmail.com',       'member'),
    ('Gael Perez',       'glape245@gmail.com',         'member'),
    ('Ingrid Castillo',  'jazcastillo0609@gmail.com',  'member');

-- Proyectos
INSERT OR IGNORE INTO projects (name, description, status, priority, start_date, due_date, owner_id) VALUES
    ('Plataforma Web Equipo Yucateco',
     'Desarrollo de un gestor de proyectos colaborativo para el equipo.',
     'active', 'high', '2026-05-01', '2026-07-30', 1),

    ('Rediseno de API REST',
     'Refactorizacion de los endpoints existentes para mejorar rendimiento.',
     'active', 'medium', '2026-06-01', '2026-07-15', 2),

    ('Migracion de Base de Datos',
     'Migrar datos del sistema legacy a la nueva estructura relacional.',
     'on_hold', 'critical', '2026-04-15', '2026-06-30', 1);

-- Hitos
INSERT OR IGNORE INTO milestones (project_id, title, description, due_date, completed) VALUES
    (1, 'Diseno de base de datos',   'Esquema SQL completo y datos de ejemplo listos.', '2026-06-20', 1),
    (1, 'Diseno de API',             'Endpoints documentados y funcionales.',            '2026-07-01', 0),
    (1, 'Interfaz de usuario v1',    'Formularios y vistas principales implementadas.',  '2026-07-15', 0),
    (2, 'Endpoints de autenticacion','Login, logout y JWT funcionando.',                 '2026-06-25', 0),
    (3, 'Script de migracion listo', 'Script de Python para migrar datos legacy.',       '2026-06-28', 0);

-- Tareas
INSERT OR IGNORE INTO tasks (project_id, milestone_id, title, description, status, priority, due_date, estimated_hours, created_by) VALUES
    (1, 1, 'Crear schema.sql',
     'Definir todas las tablas, relaciones e indices del gestor.',
     'done', 'high', '2026-06-19', 4.0, 2),

    (1, 1, 'Insertar datos de ejemplo',
     'Agregar registros representativos en sample_data.sql.',
     'done', 'medium', '2026-06-19', 2.0, 2),

    (1, 2, 'Disenar endpoint GET /projects',
     'Retornar lista de proyectos con paginacion.',
     'in_progress', 'high', '2026-06-30', 3.0, 1),

    (1, 2, 'Disenar endpoint POST /tasks',
     'Crear nueva tarea dentro de un proyecto.',
     'todo', 'high', '2026-07-01', 2.5, 1),

    (1, 3, 'Crear formulario de registro de tarea',
     'Formulario HTML con campos: titulo, descripcion, prioridad, fecha limite.',
     'todo', 'medium', '2026-07-10', 5.0, 3),

    (2, 4, 'Implementar JWT',
     'Generacion y validacion de tokens para autenticacion.',
     'in_progress', 'critical', '2026-06-22', 6.0, 4),

    (3, 5, 'Analizar estructura legacy',
     'Documentar columnas y tipos del sistema anterior.',
     'todo', 'high', '2026-06-25', 3.0, 2);

-- Miembros por proyecto
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES
    (1, 1, 'leader'),
    (1, 2, 'contributor'),
    (1, 3, 'contributor'),
    (1, 4, 'contributor'),
    (1, 5, 'viewer'),
    (2, 2, 'leader'),
    (2, 3, 'contributor'),
    (3, 1, 'leader'),
    (3, 4, 'contributor');

-- Asignaciones de tareas
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES
    (1, 2, 1),
    (2, 2, 1),
    (3, 3, 1),
    (4, 3, 1),
    (5, 4, 1),
    (6, 3, 2),
    (7, 5, 1);

-- Comentarios
INSERT OR IGNORE INTO comments (task_id, author_id, body) VALUES
    (1, 2, 'Schema terminado, incluye 9 tablas con indices y foreign keys.'),
    (1, 1, 'Revisado y aprobado. Buen trabajo.'),
    (3, 3, 'Empece con la ruta GET, necesito definir el formato de paginacion.'),
    (6, 3, 'JWT implementado con expiracion de 24h, falta el refresh token.');

-- Etiquetas
INSERT OR IGNORE INTO tags (name, color) VALUES
    ('backend',    '#0d6efd'),
    ('frontend',   '#6f42c1'),
    ('base-datos', '#198754'),
    ('urgente',    '#dc3545'),
    ('revision',   '#fd7e14');

-- Etiquetas en tareas
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES
    (1, 3), (2, 3),
    (3, 1), (4, 1),
    (5, 2),
    (6, 1), (6, 4),
    (7, 3), (7, 4);
