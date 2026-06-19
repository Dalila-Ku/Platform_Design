# Diseño de API — Yeimi Piste

**Rol:** Diseño de API  
**Rama:** `yelmy/diseno-api`

## ¿Qué es tu parte?

Te toca documentar cómo se va a comunicar la plataforma con el servidor. Básicamente defines qué rutas (endpoints) va a tener la API REST del gestor de proyectos: qué datos recibe, qué devuelve y cómo funciona la autenticación.

## Archivos

- **`api_endpoints.md`** — Contiene todos los endpoints del sistema documentados: rutas, métodos HTTP (GET, POST, PUT, DELETE), ejemplos de request y response, y los códigos de error. Es la "guía" que el resto del equipo usa para saber cómo conectarse al backend.

## Cómo subirlo a GitHub

**1. Descarga Git** si no lo tienes: https://git-scm.com/downloads

**2. Abre Git Bash** y configura tu cuenta (solo la primera vez):
```bash
git config --global user.name "Yeimi Piste"
git config --global user.email "yeimypiste@gmail.com"
```

**3. Clona el repositorio:**
```bash
cd ~/Documents
git clone https://github.com/Dalila-Ku/Platform_Design.git
cd Platform_Design
```

**4. Crea y entra a tu rama:**
```bash
git checkout -b yelmy/diseno-api
```

**5. Crea tu carpeta y copia tu archivo ahí:**
```bash
mkdir -p db_files/yeimi
```
Copia `api_endpoints.md` a la carpeta `Platform_Design/db_files/yeimi/` desde el explorador de archivos.

**6. Sube los cambios:**
```bash
git add db_files/yeimi/
git commit -m "feat: diseño de endpoints REST para el gestor de proyectos"
git push -u origin yelmy/diseno-api
```

> Si te pide contraseña, usa un Personal Access Token de GitHub:  
> GitHub → Settings → Developer settings → Personal access tokens → Generate new token → marca `repo` → copia y pega el token.
