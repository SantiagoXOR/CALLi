# Organización de Directorios

Este documento describe la organización de los directorios en el proyecto `backend-call-automation`.

## Directorios Principales

*   **api**: Contiene la definición de la API REST.
    *   **routes.py**: Define las rutas de la API.
*   **app**: Contiene la lógica principal de la aplicación.
    *   **\_\_init\_\_.py**: Archivo de inicialización del paquete.
    *   **main.py**: Punto de entrada de la aplicación FastAPI.
    *   **api**: Subpaquete que contiene los endpoints de la API.
        *   **campaigns.py**: Endpoints relacionados con las campañas.
        *   **endpoints**: Subpaquete que contiene los endpoints específicos.
            *   **cache.py**: Endpoints relacionados con la caché.
            *   **calls.py**: Endpoints relacionados con las llamadas.
    *   **config**: Subpaquete que contiene la configuración de la aplicación.
        *   **ai\_config.py**: Configuración de los servicios de IA.
        *   **database.py**: Configuración de la base de datos.
        *   **dependencies.py**: Define las dependencias de la aplicación.
        *   **metrics\_config.py**: Configuración de las métricas.
        *   **redis\_client.py**: Configuración del cliente Redis.
        *   **secrets.py**: Manejo de secretos.
        *   **settings.py**: Configuración general de la aplicación.
        *   **supabase.py**: Configuración de Supabase.
    *   **models**: Subpaquete que contiene los modelos de datos.
        *   **\_\_init\_\_.py**: Archivo de inicialización del paquete.
        *   **base.py**: Clase base para los modelos.
        *   **cache\_metrics.py**: Modelo para las métricas de la caché.
        *   **call\_metrics.py**: Modelo para las métricas de las llamadas.
        *   **call.py**: Modelo para las llamadas.
        *   **campaign.py**: Modelo para las campañas.
        *   **contact.py**: Modelo para los contactos.
        *   **user.py**: Modelo para los usuarios.
    *   **monitoring**: Subpaquete que contiene la configuración del monitoreo.
        *   **alert\_rules.yml**: Reglas de alerta.
        *   **elevenlabs\_metrics.py**: Métricas de ElevenLabs.
    *   **routers**: Subpaquete que contiene los routers de la API.
        *   **cache\_router.py**: Router para los endpoints de la caché.
        *   **call\_router.py**: Router para los endpoints de las llamadas.
        *   **campaign\_router.py**: Router para los endpoints de las campañas.
    *   **schemas**: Subpaquete que contiene los esquemas de datos (Pydantic).
        *   **call.py**: Esquema para las llamadas.
        *   **campaign.py**: Esquema para las campañas.
        *   **client.py**: Esquema para los clientes.
    *   **services**: Subpaquete que contiene la lógica de negocio de la aplicación.
        *   **ai\_conversation\_service.py**: Servicio para la conversación con IA.
        *   **alert\_service.py**: Servicio para las alertas.
        *   **cache\_service.py**: Servicio para la caché.
        *   **call\_service.py**: Servicio para las llamadas.
        *   **campaign\_scheduler.py**: Servicio para la programación de campañas.
        *   **campaign\_service.py**: Servicio para las campañas.
        *   **contact\_service.py**: Servicio para los contactos.
        *   **elevenlabs\_service.py**: Servicio para la integración con ElevenLabs.
        *   **fallback\_service.py**: Servicio de respaldo (fallback).
        *   **metrics\_service.py**: Servicio para las métricas.
        *   **monitoring\_service.py**: Servicio para el monitoreo.
        *   **twilio\_service.py**: Servicio para la integración con Twilio.
    *   **utils**: Subpaquete que contiene utilidades.
        *   **\_\_init\_\_.py**: Archivo de inicialización del paquete.
        *   **connection\_pool.py**: Pool de conexiones.
        *   **decorators.py**: Decoradores.
        *   **logger.py**: Configuración del logger.
        *   **logging\_config.py**: Configuración del logging.
*   **call\_automation.egg-info**: Información del paquete.
*   **docs**: Contiene la documentación del proyecto.
    *   **ai\_api\_endpoints.md**: Documentación de los endpoints de la API de IA.
    *   **cache\_system.md**: Documentación del sistema de caché.
    *   **conf.py**: Configuración de Sphinx para la documentación.
    *   **elevenlabs\_integration.md**: Documentación de la integración con ElevenLabs.
    *   **index.rst**: Página principal de la documentación.
    *   **Makefile**: Makefile para la documentación.
    *   **plantuml.jar**: Archivo JAR para generar diagramas UML.
    *   **troubleshooting.md**: Guía de resolución de problemas.
    *   **\_build**: Directorio de construcción de la documentación.
    *   **\_static**: Archivos estáticos para la documentación.
    *   **api**: Documentación de la API.
    *   **diagrams**: Diagramas del proyecto.
    *   **modules**: Documentación de los módulos.
    *   **runbooks**: Runbooks para operaciones.
    *   **scripts**: Scripts para la documentación.
*   **migrations**: Contiene los scripts de migración de la base de datos.
*   **scripts**: Contiene scripts para tareas específicas.
*   **supabase**: Contiene la configuración de Supabase.
*   **tests**: Contiene las pruebas unitarias e de integración.
*   **frontend-call-automation**: Contiene el código del frontend.
