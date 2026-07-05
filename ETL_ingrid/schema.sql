-- ============================================================
--  Platform_Design — Database Schema
--  Autor: Esaú Palomo | Rol: Diseño de Base de Datos
--  Rama: esau/diseno-base-datos
--  Motor: SQLite (compatible con MySQL/PostgreSQL)
--
--  Uso:
--    sqlite3 platform.db < schema.sql
--
--  Nota: PRAGMA foreign_keys = ON debe ejecutarse antes de
--  insertar datos para que las llaves foráneas funcionen.
-- ============================================================

PRAGMA foreign_keys = ON;

-- ──────────────────────────────────────────────────────────────
-- 1. USERS — Usuarios del sistema
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name  TEXT    NOT NULL,
    email      TEXT    NOT NULL UNIQUE,
    role       TEXT    NOT NULL CHECK(role IN ('admin', 'leader', 'member'))
                       DEFAULT 'member',
    created_at TEXT    NOT NULL DEFAULT (DATE('now'))
);

-- ──────────────────────────────────────────────────────────────
-- 2. PROJECTS — Proyectos del sistema
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT,
    status      TEXT    NOT NULL CHECK(status IN ('active','on_hold','completed','cancelled'))
                        DEFAULT 'active',
    priority    TEXT    NOT NULL CHECK(priority IN ('low','medium','high','critical'))
                        DEFAULT 'medium',
    start_date  TEXT,
    due_date    TEXT,
    owner_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at  TEXT    NOT NULL DEFAULT (DATE('now'))
);

CREATE INDEX IF NOT EXISTS idx_projects_status   ON projects(status);
CREATE INDEX IF NOT EXISTS idx_projects_priority ON projects(priority);
CREATE INDEX IF NOT EXISTS idx_projects_owner    ON projects(owner_id);

-- ──────────────────────────────────────────────────────────────
-- 3. MILESTONES — Hitos dentro de un proyecto
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS milestones (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id   INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title        TEXT    NOT NULL,
    due_date     TEXT,
    is_completed INTEGER NOT NULL DEFAULT 0 CHECK(is_completed IN (0,1)),
    created_at   TEXT    NOT NULL DEFAULT (DATE('now'))
);

CREATE INDEX IF NOT EXISTS idx_milestones_project ON milestones(project_id);

-- ──────────────────────────────────────────────────────────────
-- 4. TASKS — Tareas individuales (Assignment Submission Tracker)
--
--  Campos clave para las preguntas de investigación:
--    assignment_date → cuándo se asignó la tarea
--    start_date      → cuándo el estudiante comenzó a trabajar
--    due_date        → fecha límite de entrega
--    completed_date  → cuándo se marcó como completada
--    priority        → prioridad de la tarea
--    difficulty      → dificultad estimada (para la 2ª pregunta)
--    status          → estado actual
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tasks (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id       INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    parent_task_id   INTEGER REFERENCES tasks(id) ON DELETE SET NULL,
    title            TEXT    NOT NULL,
    description      TEXT,
    status           TEXT    NOT NULL CHECK(status IN ('todo','in_progress','in_review','done','cancelled'))
                             DEFAULT 'todo',
    priority         TEXT    NOT NULL CHECK(priority IN ('low','medium','high','critical'))
                             DEFAULT 'medium',
    difficulty       TEXT    NOT NULL CHECK(difficulty IN ('easy','medium','hard','very_hard'))
                             DEFAULT 'medium',
    assignment_date  TEXT    NOT NULL DEFAULT (DATE('now')),   -- fecha en que se asignó
    start_date       TEXT,                                      -- fecha en que el estudiante comenzó
    due_date         TEXT,                                      -- fecha límite de entrega
    completed_date   TEXT,                                      -- fecha en que se completó
    estimated_hours  REAL,
    actual_hours     REAL,
    created_by       INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at       TEXT    NOT NULL DEFAULT (DATE('now'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_project    ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status     ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority   ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_difficulty ON tasks(difficulty);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date   ON tasks(due_date);

-- ──────────────────────────────────────────────────────────────
-- 5. PROJECT_MEMBERS — Usuarios asignados a proyectos
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS project_members (
    project_id       INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id          INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_in_project  TEXT    NOT NULL CHECK(role_in_project IN ('leader','contributor','viewer'))
                             DEFAULT 'contributor',
    joined_at        TEXT    NOT NULL DEFAULT (DATE('now')),
    PRIMARY KEY (project_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_project_members_user ON project_members(user_id);

-- ──────────────────────────────────────────────────────────────
-- 6. TASK_ASSIGNMENTS — Usuarios asignados a tareas específicas
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS task_assignments (
    task_id     INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    assigned_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    assigned_at TEXT    NOT NULL DEFAULT (DATE('now')),
    PRIMARY KEY (task_id, user_id)
);

-- ──────────────────────────────────────────────────────────────
-- 7. COMMENTS — Comentarios en tareas o proyectos
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS comments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id    INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    body       TEXT    NOT NULL,
    created_at TEXT    NOT NULL DEFAULT (DATE('now')),
    CHECK (task_id IS NOT NULL OR project_id IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS idx_comments_task    ON comments(task_id);
CREATE INDEX IF NOT EXISTS idx_comments_project ON comments(project_id);

-- ──────────────────────────────────────────────────────────────
-- 8. TAGS — Etiquetas con color personalizado
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tags (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL DEFAULT '#6c757d'
);

-- ──────────────────────────────────────────────────────────────
-- 9. TASK_TAGS — Relación muchos-a-muchos: tareas ↔ etiquetas
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags(id)  ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- ============================================================
-- Fin del schema
-- ============================================================