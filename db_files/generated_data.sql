-- ============================================================
--  Platform_Design — Datos Generados Automaticamente
--  Generado: 2026-06-19 23:35:09
--  Autora: Dalila Ku | generacion-datos
-- ============================================================

PRAGMA foreign_keys = ON;

-- Usuarios del equipo
INSERT INTO users (full_name, email, role) VALUES ('Dalila Ku', 'dalila.ku.dzul@gmail.com', 'admin');
INSERT INTO users (full_name, email, role) VALUES ('Esau Palomo', 'Esau_palomo@hotmail.com', 'leader');
INSERT INTO users (full_name, email, role) VALUES ('Yeimi Piste', 'yeimypiste@gmail.com', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Gael Perez', 'glape245@gmail.com', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Ingrid Castillo', 'jazcastillo0609@gmail.com', 'member');

-- Usuarios adicionales generados
INSERT INTO users (full_name, email, role) VALUES ('Joaquín Montaño', 'abel52@example.com', 'leader');
INSERT INTO users (full_name, email, role) VALUES ('Camilo Luis Miguel Montañez', 'minervacampos@example.com', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Ramiro Delgadillo Rosas', 'cbustos@example.org', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Srita. Sara Hernandes', 'uriel32@example.com', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Yuridia Dolores Valenzuela Leiva', 'lorenzozamudio@example.org', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Lic. Angélica Ramón', 'marco-antoniozepeda@example.org', 'leader');
INSERT INTO users (full_name, email, role) VALUES ('Cristina Pamela Mendoza Jaime', 'saenzines@example.com', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Sra. Natalia Farías', 'toledoestela@example.org', 'member');
INSERT INTO users (full_name, email, role) VALUES ('Miguel Ángel Garibay', 'jose-carlosavila@example.net', 'leader');
INSERT INTO users (full_name, email, role) VALUES ('Rubén Guerrero Laboy', 'jose-manuelcervantes@example.org', 'member');

-- Etiquetas
INSERT INTO tags (name, color) VALUES ('backend', '#0d6efd');
INSERT INTO tags (name, color) VALUES ('frontend', '#6f42c1');
INSERT INTO tags (name, color) VALUES ('base-datos', '#198754');
INSERT INTO tags (name, color) VALUES ('urgente', '#dc3545');
INSERT INTO tags (name, color) VALUES ('revision', '#fd7e14');
INSERT INTO tags (name, color) VALUES ('bug', '#20c997');
INSERT INTO tags (name, color) VALUES ('feature', '#0dcaf0');
INSERT INTO tags (name, color) VALUES ('documentacion', '#ffc107');
INSERT INTO tags (name, color) VALUES ('pruebas', '#6c757d');
INSERT INTO tags (name, color) VALUES ('despliegue', '#d63384');

-- Proyectos
INSERT INTO projects (name, description, status, priority, start_date, due_date, owner_id) VALUES ('Plataforma Web Equipo Yucateco', 'Proyecto 1 del gestor de proyectos del equipo.', 'cancelled', 'critical', '2026-05-04', '2026-07-23', 4);
INSERT INTO projects (name, description, status, priority, start_date, due_date, owner_id) VALUES ('Rediseno de API REST', 'Proyecto 2 del gestor de proyectos del equipo.', 'completed', 'high', '2026-05-03', '2026-07-25', 1);
INSERT INTO projects (name, description, status, priority, start_date, due_date, owner_id) VALUES ('Migracion de Base de Datos', 'Proyecto 3 del gestor de proyectos del equipo.', 'completed', 'medium', '2026-04-25', '2026-09-07', 4);
INSERT INTO projects (name, description, status, priority, start_date, due_date, owner_id) VALUES ('App Movil de Seguimiento', 'Proyecto 4 del gestor de proyectos del equipo.', 'completed', 'critical', '2026-04-29', '2026-07-17', 3);
INSERT INTO projects (name, description, status, priority, start_date, due_date, owner_id) VALUES ('Portal de Reportes', 'Proyecto 5 del gestor de proyectos del equipo.', 'completed', 'medium', '2026-05-20', '2026-06-22', 4);

-- Miembros de proyectos
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (1, 5, 'leader');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (1, 3, 'viewer');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (1, 1, 'contributor');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (1, 2, 'viewer');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (2, 4, 'leader');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (2, 2, 'contributor');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (3, 3, 'leader');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (3, 1, 'contributor');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (3, 4, 'viewer');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (4, 5, 'leader');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (4, 2, 'contributor');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (4, 4, 'contributor');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (4, 1, 'viewer');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (4, 3, 'contributor');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (5, 5, 'leader');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (5, 1, 'viewer');
INSERT OR IGNORE INTO project_members (project_id, user_id, role_in_project) VALUES (5, 2, 'contributor');

-- Tareas
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (5, 'Disenar esquema de base de datos', 'done', 'high', '2026-07-06', 3.6, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (5, 'Implementar autenticacion JWT', 'cancelled', 'low', '2026-07-04', 4.1, 2);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (3, 'Crear formulario de registro', 'in_review', 'high', '2026-07-27', 7.6, 2);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (5, 'Documentar endpoints de la API', 'todo', 'high', '2026-07-09', 7.6, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (5, 'Pruebas unitarias del modulo de usuarios', 'in_progress', 'high', '2026-07-27', 4.2, 5);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (4, 'Configurar entorno de produccion', 'cancelled', 'critical', '2026-06-26', 3.8, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (5, 'Revisar pull requests del equipo', 'in_progress', 'low', '2026-07-24', 5.7, 4);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (1, 'Diseno de interfaz de dashboard', 'in_review', 'high', '2026-06-23', 1.3, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (1, 'Integracion con API externa', 'todo', 'medium', '2026-06-25', 2.8, 4);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (3, 'Optimizar consultas SQL', 'cancelled', 'medium', '2026-07-08', 5.7, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (1, 'Crear script de migracion', 'in_review', 'high', '2026-06-24', 7.5, 2);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (1, 'Actualizar dependencias del proyecto', 'done', 'critical', '2026-06-25', 4.5, 5);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (3, 'Disenar modelo de datos para reportes', 'in_progress', 'critical', '2026-07-07', 7.9, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (5, 'Implementar paginacion en endpoints', 'cancelled', 'low', '2026-07-01', 2.7, 4);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (1, 'Agregar validaciones de formularios', 'in_review', 'low', '2026-07-15', 4.9, 2);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (4, 'Subir archivos al repositorio', 'todo', 'critical', '2026-06-28', 6.8, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (4, 'Revisar documentacion tecnica', 'cancelled', 'critical', '2026-07-06', 1.9, 2);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (5, 'Crear datos de prueba', 'in_progress', 'critical', '2026-08-15', 1.4, 1);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (3, 'Diseno de flujo de trabajo', 'done', 'critical', '2026-06-29', 5.2, 3);
INSERT INTO tasks (project_id, title, status, priority, due_date, estimated_hours, created_by) VALUES (3, 'Presentacion del avance al equipo', 'cancelled', 'low', '2026-08-04', 7.2, 2);

-- Asignaciones de tareas
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (1, 2, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (2, 5, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (3, 2, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (4, 3, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (5, 3, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (6, 1, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (7, 4, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (8, 4, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (9, 3, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (10, 2, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (11, 4, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (12, 5, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (13, 3, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (14, 5, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (15, 3, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (16, 3, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (17, 3, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (18, 4, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (19, 1, 1);
INSERT OR IGNORE INTO task_assignments (task_id, user_id, assigned_by) VALUES (20, 4, 1);

-- Etiquetas en tareas
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (1, 4);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (1, 7);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (2, 5);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (2, 10);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (2, 3);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (3, 9);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (4, 5);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (4, 8);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (5, 2);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (5, 6);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (5, 1);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (6, 10);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (6, 6);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (7, 4);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (8, 9);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (8, 4);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (9, 5);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (9, 4);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (9, 10);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (10, 5);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (11, 10);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (12, 7);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (12, 10);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (13, 2);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (14, 10);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (14, 2);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (15, 4);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (15, 1);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (15, 3);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (16, 8);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (16, 3);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (16, 7);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (17, 8);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (17, 5);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (17, 9);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (18, 7);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (18, 3);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (19, 9);
INSERT OR IGNORE INTO task_tags (task_id, tag_id) VALUES (20, 2);

-- Fin del archivo generado