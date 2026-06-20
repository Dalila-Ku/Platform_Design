# Frontend / Formularios — Gael

**Rol:** Frontend / Formularios  
**Rama:** `gael/frontend-diseno-formulario`  
**Proyecto:** `Platform_Design` — Gestor de Proyectos

## Descripción

Esta carpeta contiene la parte correspondiente al diseño del frontend para la captura de información dentro de la plataforma. El archivo principal es `project_form.html`, el cual funciona como una maqueta funcional de formularios para registrar proyectos y tareas.

El objetivo de esta sección es representar la interfaz inicial que permitiría a los usuarios ingresar información básica antes de conectarla con la API y la base de datos del sistema.

## Archivos incluidos

```text
db_files/gael/
├── README.md
└── project_form.html
```

## Archivo principal

### `project_form.html`

Contiene una interfaz HTML para:

- Crear proyectos.
- Registrar tareas asociadas a un proyecto.
- Visualizar la información capturada en formato JSON.
- Simular la estructura de datos que posteriormente podría enviarse al backend/API.

## Relación con el proyecto general

Esta parte se integra al skeleton general de la plataforma como la sección visual de captura de datos. Mientras otros módulos del repositorio cubren la base de datos, API, generación de datos y documentación general, esta sección aporta una propuesta inicial de interfaz para que el usuario pueda interactuar con el sistema.

## Cómo visualizarlo localmente

1. Descargar o clonar el repositorio.
2. Entrar a la carpeta:

```text
db_files/gael/
```

3. Abrir el archivo:

```text
project_form.html
```

4. Dar doble clic sobre el archivo o abrirlo desde el navegador.

No requiere instalación de dependencias adicionales, ya que es un archivo HTML estático.

## Estado actual

Esta versión funciona como prototipo inicial de frontend. No está conectada todavía a una API real, pero deja preparada la estructura visual y lógica básica para una futura integración con los endpoints del backend.
