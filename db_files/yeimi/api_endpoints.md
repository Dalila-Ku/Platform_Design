# Diseño de API REST — Platform_Design

**Autora:** Yeimi Piste  
**Rol:** Diseño de API  
**Rama:** `yelmy/diseno-api`  
**Plataforma:** Gestor de Proyectos

---

## Base URL

```
http://localhost:3000/api/v1
```

## Autenticación

Todos los endpoints (excepto login) requieren un token JWT en el header:

```
Authorization: Bearer <token>
```

---

## Endpoints

### AUTH

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/login` | Iniciar sesión, devuelve token JWT |
| POST | `/auth/logout` | Cerrar sesión |

**POST /auth/login — Body:**
```json
{
  "email": "Esau_palomo@hotmail.com",
  "password": "tu_password"
}
```
**Respuesta:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": { "user_id": 2, "full_name": "Esau Palomo", "role": "leader" }
}
```

---

### USERS

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/users` | Listar todos los usuarios |
| GET | `/users/:id` | Obtener un usuario por ID |
| POST | `/users` | Crear usuario nuevo |
| PUT | `/users/:id` | Actualizar usuario |
| DELETE | `/users/:id` | Eliminar usuario (solo admin) |

---

### PROJECTS

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/projects` | Listar proyectos (con paginación) |
| GET | `/projects/:id` | Obtener proyecto con hitos y miembros |
| POST | `/projects` | Crear proyecto nuevo |
| PUT | `/projects/:id` | Actualizar proyecto |
| DELETE | `/projects/:id` | Eliminar proyecto |
| GET | `/projects/:id/members` | Listar miembros del proyecto |
| POST | `/projects/:id/members` | Agregar miembro al proyecto |

**GET /projects — Query params opcionales:**
```
?status=active&priority=high&page=1&limit=10
```

**POST /projects — Body:**
```json
{
  "name": "Nuevo Proyecto",
  "description": "Descripción del proyecto",
  "priority": "high",
  "start_date": "2026-07-01",
  "due_date": "2026-08-30"
}
```

---

### TASKS

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/projects/:id/tasks` | Listar tareas de un proyecto |
| GET | `/tasks/:id` | Obtener tarea con asignados y comentarios |
| POST | `/projects/:id/tasks` | Crear tarea en un proyecto |
| PUT | `/tasks/:id` | Actualizar tarea |
| DELETE | `/tasks/:id` | Eliminar tarea |
| POST | `/tasks/:id/assign` | Asignar usuario a tarea |
| DELETE | `/tasks/:id/assign/:userId` | Desasignar usuario de tarea |

**POST /projects/:id/tasks — Body:**
```json
{
  "title": "Diseñar formulario de login",
  "description": "HTML con validación de campos",
  "priority": "high",
  "due_date": "2026-07-10",
  "estimated_hours": 4.0,
  "milestone_id": 2
}
```

---

### MILESTONES

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/projects/:id/milestones` | Listar hitos de un proyecto |
| POST | `/projects/:id/milestones` | Crear hito |
| PUT | `/milestones/:id` | Actualizar hito |
| PATCH | `/milestones/:id/complete` | Marcar hito como completado |

---

### COMMENTS

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/tasks/:id/comments` | Listar comentarios de una tarea |
| POST | `/tasks/:id/comments` | Agregar comentario a tarea |
| DELETE | `/comments/:id` | Eliminar comentario (solo autor) |

---

### TAGS

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/tags` | Listar todas las etiquetas |
| POST | `/tags` | Crear etiqueta |
| POST | `/tasks/:id/tags` | Agregar etiqueta a tarea |
| DELETE | `/tasks/:id/tags/:tagId` | Quitar etiqueta de tarea |

---

## Códigos de respuesta

| Código | Significado |
|--------|-------------|
| 200 | OK |
| 201 | Creado exitosamente |
| 400 | Bad Request (datos inválidos) |
| 401 | No autenticado |
| 403 | Sin permisos suficientes |
| 404 | Recurso no encontrado |
| 500 | Error interno del servidor |
