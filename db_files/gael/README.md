# Frontend / Diseño de Formulario — Gael Pérez

**Rol:** Frontend / Diseño de Formulario  
**Rama:** `gael/frontend-diseno-formulario`

## ¿Qué es tu parte?

Te toca diseñar los formularios con los que los usuarios van a interactuar en la plataforma. Básicamente es la parte visual: las pantallas donde alguien puede crear un proyecto, agregar una tarea, asignar prioridades, etc.

## Archivos

- **`project_form.html`** — Formulario completo con dos secciones: una para crear proyectos y otra para crear tareas. Incluye campos de prioridad, fecha límite, asignación de usuarios y etiquetas. Se puede abrir directo en el navegador sin necesitar servidor.

## Cómo probarlo antes de subir

Solo abre `project_form.html` en tu navegador (doble clic al archivo). Puedes llenar los campos y al dar clic en "Crear" te muestra en pantalla los datos que se enviarían a la API.

## Cómo subirlo a GitHub

**1. Descarga Git** si no lo tienes: https://git-scm.com/downloads

**2. Abre Git Bash** y configura tu cuenta (solo la primera vez):
```bash
git config --global user.name "Gael Perez"
git config --global user.email "glape245@gmail.com"
```

**3. Clona el repositorio:**
```bash
cd ~/Documents
git clone https://github.com/Dalila-Ku/Platform_Design.git
cd Platform_Design
```

**4. Crea y entra a tu rama:**
```bash
git checkout -b gael/frontend-diseno-formulario
```

**5. Crea tu carpeta y copia tu archivo ahí:**
```bash
mkdir -p db_files/gael
```
Copia `project_form.html` a la carpeta `Platform_Design/db_files/gael/` desde el explorador de archivos.

**6. Sube los cambios:**
```bash
git add db_files/gael/
git commit -m "feat: formularios HTML para crear proyectos y tareas"
git push -u origin gael/frontend-diseno-formulario
```

> Si te pide contraseña, usa un Personal Access Token de GitHub:  
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token → marca `repo` → copia y pega el token.
