Sistema de Caché
===============

.. _cache-architecture:

Arquitectura Multi-nivel
------------------------

El sistema implementa una arquitectura de caché por niveles:

1. **Caché L1 (Memoria)**
   * Tiempo de acceso: <1ms
   * Capacidad: 100 elementos
   * TTL: 5 minutos

2. **Caché L2 (Redis)**
   * Tiempo de acceso: 1-5ms
   * Compresión adaptativa
   * TTL: 1 hora

3. **Persistencia (Supabase)**
   * Almacenamiento permanente
   * Sincronización asíncrona
   * Batch updates

.. _cache-diagram:

.. plantuml::
   :caption: Arquitectura de Caché

   @startuml
   component "Aplicación" as app
   database "L1\nMemoria" as l1
   database "L2\nRedis" as l2
   database "Supabase" as l3
   
   app --> l1
   l1 --> l2
   l2 --> l3
   @enduml

Referencias
------------

* :ref:`diagrams-architecture`
* :ref:`modules-config`
* :ref:`modules-architecture`
* :ref:`modules-deployment`
