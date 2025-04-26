# Arquitectura de Componentes - Sistema de Automatización de Llamadas

## Visión General

El Sistema de Automatización de Llamadas está diseñado como una aplicación modular y escalable, construida con una arquitectura de microservicios. Cada componente es responsable de una tarea específica, lo que permite una mayor flexibilidad, mantenibilidad y escalabilidad.

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Cliente Web                                │
│                     (Next.js + ShadCN UI)                           │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          API Gateway                                 │
│                           (FastAPI)                                  │
└───────┬───────────────────────┬────────────────────────┬────────────┘
        │                       │                        │
        ▼                       ▼                        ▼
┌───────────────┐      ┌────────────────┐      ┌─────────────────────┐
│  Servicios de │      │  Servicios de  │      │    Servicios de     │
│   Campaña     │      │    Llamada     │      │      Contacto       │
└───────┬───────┘      └────────┬───────┘      └──────────┬──────────┘
        │                       │                         │
        └───────────────────────┼─────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Capa de Integración                             │
├─────────────────────┬─────────────────────┬─────────────────────────┤
│      Twilio         │     ElevenLabs      │       LangChain         │
│  (Telefonía)        │  (Síntesis de Voz)  │    (Procesamiento IA)   │
└─────────────────────┴─────────────────────┴─────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Capa de Persistencia                            │
├─────────────────────┬─────────────────────┬─────────────────────────┤
│     Supabase        │        Redis        │     Almacenamiento      │
│  (Base de Datos)    │      (Caché)        │       (Archivos)        │
└─────────────────────┴─────────────────────┴─────────────────────────┘
```

## Componentes Principales

### 1. Frontend (Next.js + ShadCN UI)

#### Componentes Clave
- **Layout**: Estructura general de la aplicación, incluyendo navegación y contenedores.
- **Páginas**: Implementaciones específicas para cada ruta de la aplicación.
- **Componentes UI**: Elementos reutilizables como tablas, formularios, modales, etc.
- **Servicios API**: Módulos para comunicación con el backend.
- **Hooks Personalizados**: Lógica reutilizable para gestión de estado y efectos.

#### Responsabilidades
- Presentar interfaz de usuario intuitiva y responsive
- Gestionar estado local de la aplicación
- Comunicarse con el backend a través de API REST
- Validar entradas de usuario
- Proporcionar feedback visual sobre operaciones

### 2. Backend API (FastAPI)

#### Capas
- **API Layer**: Endpoints FastAPI, middleware, validación de datos
- **Service Layer**: Lógica de negocio, orquestación de servicios
- **Data Access Layer**: Interacción con Supabase, modelos de datos
- **Integration Layer**: Servicios externos (Twilio, ElevenLabs, LangChain)

#### Componentes Clave
- **Routers**: Definen los endpoints de la API agrupados por funcionalidad
- **Models**: Definen la estructura de datos utilizando Pydantic
- **Services**: Implementan la lógica de negocio
- **Repositories**: Abstraen el acceso a datos
- **Middleware**: Manejan aspectos transversales como autenticación, logging, etc.

#### Responsabilidades
- Exponer API REST para el frontend
- Implementar lógica de negocio
- Gestionar transacciones de datos
- Integrar con servicios externos
- Manejar errores y excepciones

### 3. Servicios de Campaña

#### Componentes
- **CampaignService**: Gestión del ciclo de vida de campañas
- **CampaignScheduler**: Programación y ejecución de campañas
- **CampaignAnalytics**: Análisis y reportes de campañas

#### Responsabilidades
- Crear, actualizar y eliminar campañas
- Programar ejecución de campañas
- Gestionar estado de campañas
- Generar reportes y métricas

### 4. Servicios de Llamada

#### Componentes
- **CallService**: Gestión del ciclo de vida de llamadas
- **CallProcessor**: Procesamiento de eventos de llamada
- **CallRecorder**: Grabación y almacenamiento de llamadas

#### Responsabilidades
- Iniciar y finalizar llamadas
- Procesar eventos de llamada
- Gestionar grabaciones
- Manejar reintentos y errores

### 5. Servicios de Contacto

#### Componentes
- **ContactService**: Gestión de contactos
- **ContactListService**: Gestión de listas de contactos
- **ContactImporter**: Importación de contactos desde diferentes fuentes

#### Responsabilidades
- Crear, actualizar y eliminar contactos
- Gestionar listas de contactos
- Importar y exportar contactos
- Validar datos de contacto

### 6. Capa de Integración

#### Componentes
- **TwilioService**: Integración con API de Twilio
- **ElevenLabsService**: Integración con API de ElevenLabs
- **AIConversationService**: Integración con LangChain para IA conversacional

#### Responsabilidades
- Abstraer la complejidad de las APIs externas
- Manejar autenticación con servicios externos
- Implementar reintentos y manejo de errores
- Optimizar uso de recursos externos

### 7. Capa de Persistencia

#### Componentes
- **SupabaseClient**: Cliente para interactuar con Supabase
- **CacheService**: Servicio de caché con Redis
- **StorageService**: Servicio para almacenamiento de archivos

#### Responsabilidades
- Persistir datos de la aplicación
- Optimizar rendimiento con caché
- Almacenar archivos (grabaciones, importaciones, etc.)
- Mantener consistencia de datos

## Flujos de Datos Principales

### 1. Creación de Campaña

```
┌─────────┐     ┌─────────┐     ┌───────────────┐     ┌─────────────┐
│ Usuario │────▶│Frontend │────▶│CampaignService│────▶│SupabaseClient│
└─────────┘     └─────────┘     └───────────────┘     └─────────────┘
                                        │
                                        ▼
                                ┌────────────────┐
                                │CampaignScheduler│
                                └────────────────┘
```

### 2. Ejecución de Llamada

```
┌────────────────┐     ┌───────────┐     ┌───────────┐     ┌─────────────┐
│CampaignScheduler│────▶│CallService│────▶│TwilioService│───▶│  Twilio API │
└────────────────┘     └───────────┘     └───────────┘     └─────────────┘
                             │
                             ▼
                      ┌─────────────────┐
                      │ElevenLabsService │
                      └─────────────────┘
                             │
                             ▼
                      ┌─────────────────┐
                      │AIConversationService│
                      └─────────────────┘
```

### 3. Procesamiento de Webhook de Llamada

```
┌─────────┐     ┌───────────┐     ┌─────────────┐     ┌───────────────┐
│Twilio API│────▶│CallWebhook│────▶│CallProcessor│────▶│SupabaseClient │
└─────────┘     └───────────┘     └─────────────┘     └───────────────┘
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │CampaignService│
                                  └─────────────┘
```

## Consideraciones de Diseño

### Escalabilidad
- Arquitectura modular que permite escalar componentes individualmente
- Uso de caché para reducir carga en base de datos
- Procesamiento asíncrono para tareas pesadas

### Mantenibilidad
- Separación clara de responsabilidades
- Interfaces bien definidas entre componentes
- Documentación exhaustiva

### Seguridad
- Autenticación y autorización en todos los endpoints
- Validación de datos de entrada
- Protección contra ataques comunes (CSRF, XSS, etc.)

### Rendimiento
- Estrategias de caché para datos frecuentemente accedidos
- Optimización de consultas a base de datos
- Lazy loading de componentes en frontend

## Tecnologías Utilizadas

### Frontend
- **Next.js**: Framework React con App Router
- **TypeScript**: Tipado estático
- **Tailwind CSS**: Utilidades CSS
- **ShadCN UI**: Componentes UI
- **Axios**: Cliente HTTP
- **React Hook Form**: Gestión de formularios

### Backend
- **FastAPI**: Framework API REST
- **Pydantic**: Validación de datos
- **SQLAlchemy**: ORM
- **Supabase**: Base de datos y autenticación
- **Redis**: Caché
- **LangChain**: Framework para aplicaciones de IA

### Servicios Externos
- **Twilio**: API de telefonía
- **ElevenLabs**: API de síntesis de voz
- **OpenAI/Google AI**: Modelos de lenguaje

## Referencias
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Next.js](https://nextjs.org/docs)
- [Documentación de Twilio](https://www.twilio.com/docs)
- [Documentación de ElevenLabs](https://docs.elevenlabs.io/)
- [Documentación de Supabase](https://supabase.com/docs)
