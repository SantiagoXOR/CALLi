Sistema de Automatización de Llamadas
=====================================

.. _main-index:

Bienvenido a la documentación del Sistema de Automatización de Llamadas.

.. _architecture-overview:

Arquitectura del Sistema
------------------------

El sistema está construido con:

* **Frontend**: Next.js + ShadCN UI
* **Backend**: FastAPI + Supabase
* **Servicios**: Twilio, ElevenLabs
* **Caché**: Sistema por niveles (Memoria, Redis, Supabase)

.. toctree::
   :maxdepth: 2
   :caption: Contenido:

   modules/getting_started
   modules/architecture
   modules/services
   modules/models  
   modules/config
   modules/getting_started
   modules/architecture
   modules/services
   modules/models
   modules/config
   modules/diagrams
   modules/cache
   modules/deployment
   directories

.. _reference-index:

Índice de Referencias
---------------------

* :ref:`cache-architecture` - Sistema de Caché
* :ref:`diagrams-architecture` - Diagramas de Arquitectura
* :ref:`modules/config` - Configuración del Sistema
* :ref:`modules/deployment` - Guía de Despliegue

Índices y Referencias
---------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
