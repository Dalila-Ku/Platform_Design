# Frontend / Formularios — Gael

**Rol:** Frontend / Formularios  
**Rama:** `gael/frontend-diseno-formulario`  
**Proyecto:** `Platform_Design` — Gestor de Proyectos

## ¿Qué contiene esta parte?

Esta carpeta contiene la parte correspondiente al diseño frontend de formularios para la plataforma de gestión de proyectos.

El archivo principal es:

- `project_form.html` — Interfaz estática en HTML, CSS y JavaScript para capturar proyectos y tareas.

## ¿Qué hace el formulario?

El formulario permite capturar información relacionada con dos módulos principales del sistema:

1. **Creación de proyectos**
   - Nombre del proyecto
   - Descripción
   - Estado
   - Prioridad
   - Fecha de inicio
   - Fecha límite
   - ID del responsable

2. **Creación de tareas**
   - ID del proyecto
   - ID del usuario creador
   - Título de la tarea
   - Descripción
   - Estado
   - Prioridad
   - Fecha límite
   - Horas estimadas
   - Hito opcional
   - Tarea padre opcional

## Relación con el resto del proyecto

Esta parte se conecta conceptualmente con:

- La base de datos diseñada por Esaú, especialmente las tablas `projects` y `tasks`.
- La API diseñada por Yeimi, usando rutas esperadas como `POST /projects` y `POST /projects/:id/tasks`.
- La documentación de Ingrid, donde se describe que el navegador funciona como cliente del sistema.
- Los datos generados por Dalila, que pueden servir para probar la plataforma.

## Cómo abrirlo

No requiere instalación ni servidor.

Solo abre el archivo:

```text
project_form.html
```

en cualquier navegador moderno.

## Cómo subirlo al repositorio

La estructura recomendada dentro del repositorio es:

```text
Platform_Design/
└── db_files/
    └── gael/
        ├── README.md
        └── project_form.html
```

Comandos sugeridos:

```bash
git checkout gael/frontend-diseno-formulario
mkdir -p db_files/gael
# Copiar aquí README.md y project_form.html
git add db_files/gael/
git commit -m "feat: agregar formularios frontend de Gael"
git push -u origin gael/frontend-diseno-formulario
```

Después de subir los cambios, se debe crear un Pull Request hacia `main`.
