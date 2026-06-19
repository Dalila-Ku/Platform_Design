# Generación de Datos — Dalila Ku

**Rol:** Generación de Datos  
**Rama:** `dalila/generacion-datos`

## ¿Qué es tu parte?

Te toca crear los datos de prueba que se van a usar para probar la plataforma. En lugar de inventarlos a mano, tienes un script de Python que los genera automáticamente: usuarios, proyectos, tareas, etiquetas y asignaciones.

## Archivos

- **`generate_data.py`** — Script Python que genera un archivo `generated_data.sql` con datos de ejemplo listos para insertar en la base de datos. Usa la librería `Faker` para crear nombres y correos realistas. Si no tienes Faker instalado, igual funciona con datos estáticos del equipo.

## Cómo ejecutarlo antes de subir

Necesitas tener Python instalado. Abre una terminal en la carpeta donde está el archivo y corre:

```bash
pip install faker
python generate_data.py
```

Eso genera un archivo `generated_data.sql` en la misma carpeta. Puedes abrirlo en DB Browser for SQLite y ejecutarlo después de `schema.sql` para ver los datos generados.

## Cómo subirlo a GitHub

**1. Descarga Git** si no lo tienes: https://git-scm.com/downloads

**2. Abre Git Bash** y configura tu cuenta (solo la primera vez):
```bash
git config --global user.name "Dalila Ku"
git config --global user.email "dalila.ku.dzul@gmail.com"
```

**3. Clona el repositorio:**
```bash
cd ~/Documents
git clone https://github.com/Dalila-Ku/Platform_Design.git
cd Platform_Design
```

**4. Crea y entra a tu rama:**
```bash
git checkout -b dalila/generacion-datos
```

**5. Crea tu carpeta y copia tus archivos ahí:**
```bash
mkdir -p db_files/dalila
```
Copia `generate_data.py` (y `generated_data.sql` si ya lo generaste) a `Platform_Design/db_files/dalila/` desde el explorador de archivos.

**6. Sube los cambios:**
```bash
git add db_files/dalila/
git commit -m "feat: script de generacion de datos para el gestor de proyectos"
git push -u origin dalila/generacion-datos
```

> Si te pide contraseña, usa un Personal Access Token de GitHub:  
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token → marca `repo` → copia y pega el token.
