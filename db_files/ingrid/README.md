# Documentación — Ingrid Castillo

**Rol:** Documentación  
**Rama:** `ingrid/documentacion`

## ¿Qué es tu parte?

Te toca documentar todo el proyecto para que cualquier persona (incluyendo el maestro) entienda cómo está construida la plataforma, para qué sirve cada parte y cómo ejecutarla. Es la pieza que une el trabajo de todos.

## Archivos

- **`DOCUMENTATION.md`** — Documentación técnica completa del sistema. Incluye: descripción del proyecto, tabla de integrantes con roles, arquitectura general, estructura del repositorio, descripción de cada tabla de la BD, cómo ejecutar el proyecto en local y notas técnicas importantes.

## Cómo editarla

Puedes abrir `DOCUMENTATION.md` con cualquier editor de texto (VS Code, Bloc de notas, etc.). Si usas VS Code puedes ver la vista previa con `Ctrl+Shift+V`. Si necesitas agregar algo del proyecto, edita directamente el archivo.

## Cómo subirlo a GitHub

**1. Descarga Git** si no lo tienes: https://git-scm.com/downloads

**2. Abre Git Bash** y configura tu cuenta (solo la primera vez):
```bash
git config --global user.name "Ingrid Castillo"
git config --global user.email "jazcastillo0609@gmail.com"
```

**3. Clona el repositorio:**
```bash
cd ~/Documents
git clone https://github.com/Dalila-Ku/Platform_Design.git
cd Platform_Design
```

**4. Crea y entra a tu rama:**
```bash
git checkout -b ingrid/documentacion
```

**5. Crea tu carpeta y copia tu archivo ahí:**
```bash
mkdir -p db_files/ingrid
```
Copia `DOCUMENTATION.md` a la carpeta `Platform_Design/db_files/ingrid/` desde el explorador de archivos.

**6. Sube los cambios:**
```bash
git add db_files/ingrid/
git commit -m "feat: documentacion tecnica del gestor de proyectos"
git push -u origin ingrid/documentacion
```

> Si te pide contraseña, usa un Personal Access Token de GitHub:  
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token → marca `repo` → copia y pega el token.
