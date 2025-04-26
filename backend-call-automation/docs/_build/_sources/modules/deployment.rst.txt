Despliegue del Sistema
======================

.. _modules-deployment:

Esta sección documenta el proceso de despliegue del sistema.

Visión general del despliegue
-------------------------------

El sistema de automatización de llamadas se despliega utilizando contenedores Docker. Esto permite una mayor portabilidad y facilidad de despliegue en diferentes entornos.

Entornos de despliegue
----------------------

*   **Desarrollo**: Utilizado para el desarrollo y pruebas locales.
*   **Pruebas**: Utilizado para pruebas de integración y aceptación.
*   **Producción**: Utilizado para el despliegue en producción.

Requisitos del sistema
---------------------

*   Docker
*   Docker Compose

Proceso detallado de despliegue
--------------------------------

1.  Construir las imágenes de Docker:

    .. code-block:: bash

        docker-compose build

2.  Desplegar los contenedores:

    .. code-block:: bash

        docker-compose up -d

Comandos Docker para el despliegue
----------------------------------

*   Construir las imágenes: `docker-compose build`
*   Desplegar los contenedores: `docker-compose up -d`
*   Detener los contenedores: `docker-compose down`

Procedimiento de rollback
--------------------------

1.  Detener los contenedores:

    .. code-block:: bash

        docker-compose down

2.  Restaurar la versión anterior del código.

3.  Construir las imágenes de Docker con la versión anterior del código:

    .. code-block:: bash

        docker-compose build

4.  Desplegar los contenedores con la versión anterior del código:

    .. code-block:: bash

        docker-compose up -d

Referencias
------------

*   :ref:`modules/architecture`
*   :ref:`modules/config`
