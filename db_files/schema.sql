-- ============================================================
--  Platform_Design — Esquema de Base de Datos
--  Autor: Esaú Palomo | Rol: Diseño de Base de Datos
--  Rama: esau/diseno-base-datos
--  Plataforma: Gestor de Proyectos (Project Management System)
--  Motor: SQLite (compatible con MySQL/PostgreSQL con ajustes mínimos)
--  Fecha: 2026-06-19
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- TABLA: users
-- Usuarios del sistema (administradores, líderes y miembros)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT    NOT NULL,
    email         TEXT    NOT NULL UNIQUE,
    role          TEXT    NOT NULL DEFAULT 'member'
                          CHECK(role IN ('admin', 'leader', 'member')),
    avatar_url    TEXT,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ------------------------------------------------------------
-- TABLA: projects
-- Proyectos registrados en la plataforma
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
    project_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT    NOT NULL,
    description   TEXT,
    status        TEXT    NOT NULL DEFAULT 'active'
                          CHECK(status IN ('active', 'on_hold', 'completed', 'cancelled')),
    priority      TEXT    NOT NULL DEFAULT 'medium'
                          CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    start_date    TEXT,
    due_date      TEXT,
    owner_id      INTEGER NOT NULL,
    created_at    TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- TABLA: milestones
-- Hitos o entregables importantes dentro de un proyecto
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS milestones (
    milestone_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id    INTEGER NOT NULL,
    title         TEXT    NOT NULL,
    description   TEXT,
    due_date      TEXT,
    completed     INTEGER NOT NULL DEFAULT 0
                          CHECK(completed IN (0, 1)),
    completed_at  TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- TABLA: tasks
-- Tareas individuales dentro de un proyecto
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    task_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      INTEGER NOT NULL,
    milestone_id    INTEGER,
    parent_task_id  INTEGER,
    title           TEXT    NOT NULL,
    description     TEXT,
    status          TEXT    NOT NULL DEFAULT 'todo'
                            CHECK(status IN ('todo', 'in_progress', 'in_review', 'done', 'cancelled')),
    priority        TEXT    NOT NULL DEFAULT 'medium'
                            CHECK(priority IN ('low', 'medium', 'high', 'critical')),
    due_date        TEXT,
    estimated_hours REAL,
    actual_hours    REAL,
    created_by      INTEGER NOT NULL,
    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT    NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (project_id)      REFERENCES projects(project_id)     ON DELETE CASCADE,
    FOREIGN KEY (milestone_id)    REFERENCES milestones(milestone_id) ON DELETE SET NULL,
    FOREIGN KEY (parent_task_id)  REFERENCES tasks(task_id)           ON DELETE SET NULL,
    FOREIGN KEY (created_by)      REFERENCES users(user_id)           ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- TABLA: project_members
-- Miembros asignados a cada proyecto y su rol dentro de él
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS project_members (
    project_id      INTEGER NOT NULL,
    user_id         INTEGER NOT NULL,
    role_in_project TEXT    NOT NULL DEFAULT 'contributor'
                            CHECK(role_in_project IN ('leader', 'contributor', 'viewer')),
    joined_at       TEXT    NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)    REFERENCES users(user_id)       ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- TABLA: task_assignments
-- Usuarios asignados a tareas específicas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS task_assignments (
    task_id     INTEGER NOT NULL,
    user_id     INTEGER NOT NULL,
    assigned_at TEXT    NOT NULL DEFAULT (datetime('now')),
    assigned_by INTEGER NOT NULL,
    PRIMARY KEY (task_id, user_id),
    FOREIGN KEY (task_id)     REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)     REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(user_id) ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- TABLA: comments
-- Comentarios en tareas o en proyectos
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS comments (
    comment_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id     INTEGER,
    project_id  INTEGER,
    author_id   INTEGER NOT NULL,
    body        TEXT    NOT NULL,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    CHECK (task_id IS NOT NULL OR project_id IS NOT NULL),
    FOREIGN KEY (task_id)    REFERENCES tasks(task_id)       ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
    FOREIGN KEY (author_id)  REFERENCES users(user_id)       ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- TABLA: tags
-- Etiquetas reutilizables para clasificar tareas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tags (
    tag_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT    NOT NULL UNIQUE,
    color   TEXT    NOT NULL DEFAULT '#6c757d'
);

-- ------------------------------------------------------------
-- TABLA: task_tags
-- Relacion muchos-a-muchos entre tareas y etiquetas
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS task_tags (
    task_id INTEGER NOT NULL,
    tag_id  INTEGER NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)  REFERENCES tags(tag_id)   ON DELETE CASCADE
);

-- ============================================================
-- INDICES — aceleran las consultas mas frecuentes
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_tasks_project   ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status    ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date  ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_priority  ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_comments_task   ON comments(task_id);
CREATE INDEX IF NOT EXISTS idx_members_user    ON project_members(user_id);
CREATE INDEX IF NOT EXISTS idx_milestones_proj ON milestones(project_id);
