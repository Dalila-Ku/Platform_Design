-- ============================================================
--  Platform_Design — Sample Data
--  Autor: Esaú Palomo | Rol: Diseño de Base de Datos
--  Rama: esau/diseno-base-datos
--
--  Ejecutar DESPUÉS de schema.sql:
--    sqlite3 platform.db < sample_data.sql
--
--  Datos diseñados para responder las preguntas de investigación
--  del Assignment Submission Tracker:
--    P1: ¿Las tareas de alta prioridad se completan antes?
--    P2: ¿Los estudiantes comienzan antes las tareas difíciles?
-- ============================================================

PRAGMA foreign_keys = ON;

-- ── Usuarios ────────────────────────────────────────────────
INSERT INTO users (full_name, email, role) VALUES
  ('Dalila Ku',       'dalila.ku.dzul@gmail.com',  'admin'),
  ('Esaú Palomo',     'Esau_palomo@hotmail.com',   'leader'),
  ('Yeimi Piste',     'yeimypiste@gmail.com',       'member'),
  ('Gael Pérez',      'glape245@gmail.com',         'member'),
  ('Ingrid Castillo', 'jazcastillo0609@gmail.com',  'member'),
  ('Ana Torres',      'ana.torres@example.com',     'member'),
  ('Luis Méndez',     'luis.mendez@example.com',    'member'),
  ('Sofía Ramírez',   'sofia.ramirez@example.com',  'member');

-- ── Proyecto principal ───────────────────────────────────────
INSERT INTO projects (name, description, status, priority, start_date, due_date, owner_id) VALUES
  ('Platform Design UPY', 'Plataforma colaborativa de gestión de proyectos académicos TeamX 2026',
   'active', 'high', '2026-05-01', '2026-07-15', 1);

-- ── Miembros del proyecto ────────────────────────────────────
INSERT INTO project_members (project_id, user_id, role_in_project) VALUES
  (1, 1, 'leader'),
  (1, 2, 'contributor'),
  (1, 3, 'contributor'),
  (1, 4, 'contributor'),
  (1, 5, 'contributor'),
  (1, 6, 'contributor'),
  (1, 7, 'contributor'),
  (1, 8, 'contributor');

-- ── Tags ─────────────────────────────────────────────────────
INSERT INTO tags (name, color) VALUES
  ('backend',       '#0d6efd'),
  ('frontend',      '#6f42c1'),
  ('base-datos',    '#198754'),
  ('urgente',       '#dc3545'),
  ('documentacion', '#fd7e14'),
  ('api',           '#20c997'),
  ('pruebas',       '#ffc107'),
  ('despliegue',    '#6c757d');

-- ── Tareas — diseñadas para responder P1 y P2 ───────────────
--
-- Columnas clave:
--   assignment_date  = cuando se asignó
--   start_date       = cuando el estudiante comenzó (NULL = aún no inicia)
--   due_date         = fecha límite
--   completed_date   = cuando terminó (NULL = no completada)
--   priority         = low | medium | high | critical
--   difficulty       = easy | medium | hard | very_hard
--   status           = todo | in_progress | in_review | done | cancelled
--
-- Patrones de datos para P1 (prioridad alta → completa antes):
--   - Tareas critical/high completadas en pocos días desde due_date
--   - Tareas low/medium terminadas tarde o pendientes
--
-- Patrones para P2 (tareas difíciles → inician antes):
--   - Tareas hard/very_hard con start_date más temprano relativo a assignment_date
--   - Tareas easy con start_date tardío o igual a due_date

INSERT INTO tasks
  (project_id, title, status, priority, difficulty,
   assignment_date, start_date, due_date, completed_date,
   estimated_hours, actual_hours, created_by)
VALUES
-- CRITICAL / very_hard → inicia rápido, termina antes (soporta P1 y P2)
  (1, 'Diseñar esquema de base de datos',
   'done', 'critical', 'very_hard',
   '2026-05-01', '2026-05-02', '2026-05-15', '2026-05-12',
   20.0, 18.5, 2),

-- CRITICAL / hard → también termina antes
  (1, 'Implementar autenticación JWT',
   'done', 'critical', 'hard',
   '2026-05-01', '2026-05-03', '2026-05-20', '2026-05-17',
   16.0, 15.0, 3),

-- HIGH / hard → inicia pronto, termina a tiempo
  (1, 'Diseñar endpoints REST de la API',
   'done', 'high', 'hard',
   '2026-05-05', '2026-05-06', '2026-05-22', '2026-05-21',
   12.0, 13.0, 3),

-- HIGH / medium → termina justo a tiempo
  (1, 'Generar script de datos de prueba',
   'done', 'high', 'medium',
   '2026-05-05', '2026-05-09', '2026-05-25', '2026-05-25',
   8.0, 9.0, 1),

-- HIGH / very_hard → inicia muy pronto (P2), termina antes (P1)
  (1, 'Configurar entorno de despliegue',
   'in_review', 'high', 'very_hard',
   '2026-05-10', '2026-05-11', '2026-06-10', NULL,
   24.0, 20.0, 2),

-- MEDIUM / medium → inicia tarde respecto al assignment_date
  (1, 'Crear formularios HTML del frontend',
   'done', 'medium', 'medium',
   '2026-05-10', '2026-05-20', '2026-06-01', '2026-06-02',
   10.0, 11.0, 4),

-- MEDIUM / easy → inicia muy tarde, entrega tardía
  (1, 'Actualizar README con instrucciones',
   'done', 'medium', 'easy',
   '2026-05-15', '2026-05-28', '2026-06-01', '2026-06-03',
   3.0, 2.5, 5),

-- LOW / easy → inicia el último día posible
  (1, 'Agregar comentarios al código SQL',
   'done', 'low', 'easy',
   '2026-05-15', '2026-06-04', '2026-06-05', '2026-06-05',
   2.0, 1.5, 2),

-- MEDIUM / hard → inicia relativamente rápido (P2 parcial)
  (1, 'Pruebas de integración de la API',
   'in_progress', 'medium', 'hard',
   '2026-05-20', '2026-05-24', '2026-06-20', NULL,
   14.0, 8.0, 3),

-- LOW / medium → no ha iniciado todavía
  (1, 'Documentar modelo entidad-relación',
   'todo', 'low', 'medium',
   '2026-05-25', NULL, '2026-06-25', NULL,
   6.0, NULL, 5),

-- CRITICAL / hard → inicia al día siguiente (P1 y P2)
  (1, 'Corregir error en llave foránea de tasks',
   'done', 'critical', 'hard',
   '2026-06-01', '2026-06-02', '2026-06-05', '2026-06-04',
   4.0, 3.5, 2),

-- HIGH / very_hard → inicia pronto
  (1, 'Migrar datos a formato CSV y JSON',
   'done', 'high', 'very_hard',
   '2026-06-01', '2026-06-02', '2026-06-15', '2026-06-13',
   10.0, 11.0, 1),

-- LOW / easy → entrega tardía
  (1, 'Revisar ortografía en documentación',
   'done', 'low', 'easy',
   '2026-06-05', '2026-06-14', '2026-06-15', '2026-06-16',
   1.5, 1.0, 5),

-- MEDIUM / easy → inicio normal
  (1, 'Subir archivos de datos al repositorio',
   'done', 'medium', 'easy',
   '2026-06-10', '2026-06-12', '2026-06-19', '2026-06-19',
   2.0, 1.5, 4),

-- HIGH / hard → en progreso, inició rápido
  (1, 'Optimizar consultas SQL con índices',
   'in_progress', 'high', 'hard',
   '2026-06-15', '2026-06-16', '2026-06-28', NULL,
   8.0, 4.0, 2),

-- LOW / very_hard → no ha iniciado (tarea difícil pero baja prioridad)
  (1, 'Implementar sistema de notificaciones',
   'todo', 'low', 'very_hard',
   '2026-06-15', NULL, '2026-07-10', NULL,
   30.0, NULL, 3),

-- CRITICAL / medium → completada antes
  (1, 'Revisión final del skeleton antes de entrega',
   'done', 'critical', 'medium',
   '2026-06-18', '2026-06-18', '2026-06-19', '2026-06-19',
   5.0, 4.5, 1),

-- MEDIUM / hard → inicia al 3er día
  (1, 'Diseñar flujo de autenticación de usuarios',
   'in_review', 'medium', 'hard',
   '2026-06-10', '2026-06-13', '2026-06-30', NULL,
   12.0, 10.0, 3),

-- HIGH / easy → inicia tarde a pesar de la prioridad alta
  (1, 'Crear presentación del avance al equipo',
   'todo', 'high', 'easy',
   '2026-06-20', NULL, '2026-06-26', NULL,
   3.0, NULL, 4),

-- CRITICAL / very_hard → inicia inmediatamente
  (1, 'Configurar GitHub Actions para deploy automático',
   'in_progress', 'critical', 'very_hard',
   '2026-06-20', '2026-06-20', '2026-06-27', NULL,
   16.0, 6.0, 2);

-- ── Asignaciones de tareas ───────────────────────────────────
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES
  (1, 2, 1), (2, 3, 1), (3, 3, 1), (4, 1, 1), (5, 2, 1),
  (6, 4, 1), (7, 5, 1), (8, 2, 1), (9, 3, 1), (10, 5, 1),
  (11, 2, 1), (12, 1, 1), (13, 5, 1), (14, 4, 1), (15, 2, 1),
  (16, 3, 1), (17, 1, 1), (18, 3, 1), (19, 4, 1), (20, 2, 1);

-- ── Tags en tareas ───────────────────────────────────────────
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES
  (1,3),(1,1), (2,1),(2,4), (3,6),(3,2), (4,7),(4,3),
  (5,8),(5,4), (6,2),(6,5), (7,5),       (8,3),
  (9,6),(9,7), (10,5),      (11,3),(11,4),(12,3),(12,7),
  (13,5),      (14,7),      (15,1),(15,3),(16,2),
  (17,4),(17,8),(18,6),     (19,2),      (20,8),(20,4);

-- ============================================================
-- Fin de datos de muestra
-- ============================================================
