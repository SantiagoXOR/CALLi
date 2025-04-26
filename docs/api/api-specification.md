# Especificación de API - Sistema de Automatización de Llamadas

## Convenciones Generales

### Formato de Respuesta

Todas las respuestas de la API siguen un formato estándar:

```json
{
  "data": { ... },      // Datos de respuesta (omitido en caso de error)
  "meta": { ... },      // Metadatos (paginación, etc.)
  "error": { ... }      // Información de error (omitido en caso de éxito)
}
```

#### Respuesta Exitosa

```json
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Campaña de Ventas Q2",
    "created_at": "2025-04-01T10:00:00Z"
  },
  "meta": {
    "timestamp": "2025-04-01T10:05:23Z"
  }
}
```

#### Respuesta con Error

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "La campaña solicitada no existe",
    "details": {
      "resource_id": "123e4567-e89b-12d3-a456-426614174000"
    }
  },
  "meta": {
    "timestamp": "2025-04-01T10:05:23Z"
  }
}
```

### Códigos de Estado HTTP

| Código | Descripción                                                |
|--------|------------------------------------------------------------|
| 200    | OK - Solicitud exitosa                                     |
| 201    | Created - Recurso creado exitosamente                      |
| 204    | No Content - Solicitud exitosa sin contenido de respuesta  |
| 400    | Bad Request - Error en la solicitud del cliente            |
| 401    | Unauthorized - Autenticación requerida                     |
| 403    | Forbidden - Sin permisos para acceder al recurso           |
| 404    | Not Found - Recurso no encontrado                          |
| 409    | Conflict - Conflicto con el estado actual del recurso      |
| 422    | Unprocessable Entity - Validación fallida                  |
| 429    | Too Many Requests - Límite de tasa excedido                |
| 500    | Internal Server Error - Error interno del servidor         |

### Autenticación

La API utiliza autenticación basada en tokens JWT. El token debe incluirse en el encabezado `Authorization` de todas las solicitudes:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Paginación

Para endpoints que devuelven colecciones de recursos, se utiliza paginación basada en offset:

#### Parámetros de Consulta

| Parámetro | Descripción                                | Valor Predeterminado |
|-----------|--------------------------------------------|----------------------|
| limit     | Número de elementos por página             | 20                   |
| offset    | Índice del primer elemento a devolver      | 0                    |
| sort      | Campo por el cual ordenar                  | created_at           |
| order     | Dirección de ordenamiento (asc/desc)       | desc                 |

#### Respuesta Paginada

```json
{
  "data": [ ... ],
  "meta": {
    "pagination": {
      "total": 100,
      "limit": 20,
      "offset": 0,
      "next_offset": 20,
      "prev_offset": null
    }
  }
}
```

### Filtrado

Los endpoints que soportan filtrado aceptan parámetros de consulta con el formato `filter[campo]=valor`:

```
GET /api/campaigns?filter[status]=active&filter[created_at][gte]=2025-01-01
```

## Endpoints

### Campañas

#### Listar Campañas

```
GET /api/campaigns
```

**Parámetros de Consulta**
- `filter[status]`: Filtrar por estado (draft, active, paused, completed, archived)
- `filter[created_at][gte]`: Filtrar por fecha de creación mayor o igual
- `filter[created_at][lte]`: Filtrar por fecha de creación menor o igual
- `filter[name]`: Filtrar por nombre (búsqueda parcial)

**Respuesta**
```json
{
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Campaña de Ventas Q2",
      "description": "Campaña para promocionar nuevos productos",
      "status": "active",
      "schedule_start": "2025-04-01T10:00:00Z",
      "schedule_end": "2025-04-30T23:59:59Z",
      "total_calls": 150,
      "successful_calls": 120,
      "failed_calls": 30,
      "pending_calls": 0,
      "created_at": "2025-03-15T14:30:00Z",
      "updated_at": "2025-04-30T23:59:59Z"
    },
    // ...
  ],
  "meta": {
    "pagination": {
      "total": 25,
      "limit": 20,
      "offset": 0,
      "next_offset": 20,
      "prev_offset": null
    }
  }
}
```

#### Crear Campaña

```
POST /api/campaigns
```

**Cuerpo de la Solicitud**
```json
{
  "name": "Campaña de Ventas Q3",
  "description": "Campaña para promocionar productos de verano",
  "status": "draft",
  "schedule_start": "2025-07-01T10:00:00Z",
  "schedule_end": "2025-07-31T23:59:59Z",
  "contact_list_ids": ["a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"],
  "script_template": "Hola {nombre}, te llamo de {empresa} para hablarte sobre nuestras ofertas de verano...",
  "max_retries": 3,
  "retry_delay_minutes": 60,
  "calling_hours_start": "09:00",
  "calling_hours_end": "18:00"
}
```

**Respuesta (201 Created)**
```json
{
  "data": {
    "id": "456e7890-e12d-34f5-a678-901234567890",
    "name": "Campaña de Ventas Q3",
    "description": "Campaña para promocionar productos de verano",
    "status": "draft",
    "schedule_start": "2025-07-01T10:00:00Z",
    "schedule_end": "2025-07-31T23:59:59Z",
    "contact_list_ids": ["a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"],
    "script_template": "Hola {nombre}, te llamo de {empresa} para hablarte sobre nuestras ofertas de verano...",
    "max_retries": 3,
    "retry_delay_minutes": 60,
    "calling_hours_start": "09:00",
    "calling_hours_end": "18:00",
    "total_calls": 0,
    "successful_calls": 0,
    "failed_calls": 0,
    "pending_calls": 0,
    "created_at": "2025-06-15T14:30:00Z",
    "updated_at": "2025-06-15T14:30:00Z"
  },
  "meta": {
    "timestamp": "2025-06-15T14:30:00Z"
  }
}
```

#### Obtener Campaña

```
GET /api/campaigns/{id}
```

**Parámetros de Ruta**
- `id`: ID único de la campaña

**Respuesta**
```json
{
  "data": {
    "id": "456e7890-e12d-34f5-a678-901234567890",
    "name": "Campaña de Ventas Q3",
    "description": "Campaña para promocionar productos de verano",
    "status": "draft",
    "schedule_start": "2025-07-01T10:00:00Z",
    "schedule_end": "2025-07-31T23:59:59Z",
    "contact_list_ids": ["a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"],
    "script_template": "Hola {nombre}, te llamo de {empresa} para hablarte sobre nuestras ofertas de verano...",
    "max_retries": 3,
    "retry_delay_minutes": 60,
    "calling_hours_start": "09:00",
    "calling_hours_end": "18:00",
    "total_calls": 0,
    "successful_calls": 0,
    "failed_calls": 0,
    "pending_calls": 0,
    "created_at": "2025-06-15T14:30:00Z",
    "updated_at": "2025-06-15T14:30:00Z"
  },
  "meta": {
    "timestamp": "2025-06-15T14:35:00Z"
  }
}
```

#### Actualizar Campaña

```
PUT /api/campaigns/{id}
```

**Parámetros de Ruta**
- `id`: ID único de la campaña

**Cuerpo de la Solicitud**
```json
{
  "name": "Campaña de Ventas Q3 - Actualizada",
  "description": "Campaña para promocionar productos de verano con descuentos especiales",
  "status": "active",
  "max_retries": 5
}
```

**Respuesta**
```json
{
  "data": {
    "id": "456e7890-e12d-34f5-a678-901234567890",
    "name": "Campaña de Ventas Q3 - Actualizada",
    "description": "Campaña para promocionar productos de verano con descuentos especiales",
    "status": "active",
    "schedule_start": "2025-07-01T10:00:00Z",
    "schedule_end": "2025-07-31T23:59:59Z",
    "contact_list_ids": ["a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890"],
    "script_template": "Hola {nombre}, te llamo de {empresa} para hablarte sobre nuestras ofertas de verano...",
    "max_retries": 5,
    "retry_delay_minutes": 60,
    "calling_hours_start": "09:00",
    "calling_hours_end": "18:00",
    "total_calls": 0,
    "successful_calls": 0,
    "failed_calls": 0,
    "pending_calls": 0,
    "created_at": "2025-06-15T14:30:00Z",
    "updated_at": "2025-06-15T15:00:00Z"
  },
  "meta": {
    "timestamp": "2025-06-15T15:00:00Z"
  }
}
```

#### Eliminar Campaña

```
DELETE /api/campaigns/{id}
```

**Parámetros de Ruta**
- `id`: ID único de la campaña

**Respuesta (204 No Content)**
Sin cuerpo de respuesta

### Contactos

#### Listar Contactos

```
GET /api/contacts
```

**Parámetros de Consulta**
- `filter[name]`: Filtrar por nombre (búsqueda parcial)
- `filter[phone_number]`: Filtrar por número de teléfono
- `filter[email]`: Filtrar por email
- `filter[tags]`: Filtrar por etiquetas (separadas por comas)

**Respuesta**
```json
{
  "data": [
    {
      "id": "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890",
      "name": "Juan Pérez",
      "phone_number": "+34600123456",
      "email": "juan.perez@example.com",
      "notes": "Cliente potencial interesado en productos premium",
      "tags": ["cliente-potencial", "premium"],
      "additional_data": {
        "company": "Empresa ABC",
        "position": "Director de Compras"
      },
      "created_at": "2025-03-10T09:15:00Z",
      "updated_at": "2025-03-10T09:15:00Z"
    },
    // ...
  ],
  "meta": {
    "pagination": {
      "total": 150,
      "limit": 20,
      "offset": 0,
      "next_offset": 20,
      "prev_offset": null
    }
  }
}
```

#### Crear Contacto

```
POST /api/contacts
```

**Cuerpo de la Solicitud**
```json
{
  "name": "María García",
  "phone_number": "+34600789012",
  "email": "maria.garcia@example.com",
  "notes": "Interesada en servicios de consultoría",
  "tags": ["cliente-potencial", "consultoría"],
  "additional_data": {
    "company": "Empresa XYZ",
    "position": "CEO"
  }
}
```

**Respuesta (201 Created)**
```json
{
  "data": {
    "id": "b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901",
    "name": "María García",
    "phone_number": "+34600789012",
    "email": "maria.garcia@example.com",
    "notes": "Interesada en servicios de consultoría",
    "tags": ["cliente-potencial", "consultoría"],
    "additional_data": {
      "company": "Empresa XYZ",
      "position": "CEO"
    },
    "created_at": "2025-06-16T10:20:00Z",
    "updated_at": "2025-06-16T10:20:00Z"
  },
  "meta": {
    "timestamp": "2025-06-16T10:20:00Z"
  }
}
```

### Llamadas

#### Listar Llamadas

```
GET /api/calls
```

**Parámetros de Consulta**
- `filter[campaign_id]`: Filtrar por ID de campaña
- `filter[contact_id]`: Filtrar por ID de contacto
- `filter[status]`: Filtrar por estado (pending, in-progress, completed, failed, etc.)
- `filter[created_at][gte]`: Filtrar por fecha de creación mayor o igual
- `filter[created_at][lte]`: Filtrar por fecha de creación menor o igual

**Respuesta**
```json
{
  "data": [
    {
      "id": "c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012",
      "campaign_id": "456e7890-e12d-34f5-a678-901234567890",
      "contact_id": "a1b2c3d4-e5f6-7890-a1b2-c3d4e5f67890",
      "status": "completed",
      "scheduled_time": "2025-07-01T10:30:00Z",
      "started_at": "2025-07-01T10:30:05Z",
      "ended_at": "2025-07-01T10:35:12Z",
      "duration": 307,
      "recording_url": "https://storage.example.com/recordings/c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012.mp3",
      "notes": "Cliente interesado en recibir más información",
      "twilio_sid": "CA123456789012345678901234567890",
      "retry_attempts": 0,
      "error_message": null,
      "created_at": "2025-07-01T10:00:00Z",
      "updated_at": "2025-07-01T10:35:15Z"
    },
    // ...
  ],
  "meta": {
    "pagination": {
      "total": 75,
      "limit": 20,
      "offset": 0,
      "next_offset": 20,
      "prev_offset": null
    }
  }
}
```

#### Iniciar Llamada

```
POST /api/calls
```

**Cuerpo de la Solicitud**
```json
{
  "campaign_id": "456e7890-e12d-34f5-a678-901234567890",
  "contact_id": "b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901",
  "scheduled_time": "2025-07-02T11:00:00Z",
  "script_template": "Hola {nombre}, te llamo de {empresa} para hablarte sobre nuestras ofertas de verano...",
  "webhook_url": "https://api.example.com/webhooks/calls",
  "status_callback_url": "https://api.example.com/webhooks/call-status"
}
```

**Respuesta (201 Created)**
```json
{
  "data": {
    "id": "d4e5f6a7-b8c9-0123-d4e5-f6a7b8c90123",
    "campaign_id": "456e7890-e12d-34f5-a678-901234567890",
    "contact_id": "b2c3d4e5-f6a7-8901-b2c3-d4e5f6a78901",
    "status": "pending",
    "scheduled_time": "2025-07-02T11:00:00Z",
    "script_template": "Hola {nombre}, te llamo de {empresa} para hablarte sobre nuestras ofertas de verano...",
    "webhook_url": "https://api.example.com/webhooks/calls",
    "status_callback_url": "https://api.example.com/webhooks/call-status",
    "twilio_sid": null,
    "retry_attempts": 0,
    "max_retries": 3,
    "created_at": "2025-07-01T15:45:00Z",
    "updated_at": "2025-07-01T15:45:00Z"
  },
  "meta": {
    "timestamp": "2025-07-01T15:45:00Z"
  }
}
```

### Webhooks

#### Webhook de Twilio

```
POST /api/webhooks/twilio
```

**Cuerpo de la Solicitud (enviado por Twilio)**
```
CallSid=CA123456789012345678901234567890&
CallStatus=in-progress&
Called=+34600789012&
Caller=+12025550142&
...
```

**Respuesta (TwiML)**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="woman">Hola María, te llamo de Empresa XYZ para hablarte sobre nuestras ofertas de verano...</Say>
    <Gather input="speech dtmf" timeout="3" numDigits="1">
        <Say voice="woman">Presiona 1 si estás interesado, o 2 si prefieres que te llamemos en otro momento.</Say>
    </Gather>
</Response>
```

#### Webhook de Estado de Llamada

```
POST /api/webhooks/call-status
```

**Cuerpo de la Solicitud (enviado por Twilio)**
```
CallSid=CA123456789012345678901234567890&
CallStatus=completed&
CallDuration=307&
RecordingUrl=https://api.twilio.com/2010-04-01/Accounts/AC123/Recordings/RE123&
...
```

**Respuesta (200 OK)**
```json
{
  "success": true
}
```

### Reportes

#### Reporte de Campañas

```
GET /api/reports/campaigns
```

**Parámetros de Consulta**
- `start_date`: Fecha de inicio (YYYY-MM-DD)
- `end_date`: Fecha de fin (YYYY-MM-DD)
- `campaign_ids`: IDs de campañas separados por comas (opcional)
- `group_by`: Agrupar por (day, week, month)

**Respuesta**
```json
{
  "data": {
    "summary": {
      "total_campaigns": 5,
      "total_calls": 1250,
      "successful_calls": 950,
      "failed_calls": 300,
      "success_rate": 76,
      "average_duration": 245
    },
    "campaigns": [
      {
        "id": "456e7890-e12d-34f5-a678-901234567890",
        "name": "Campaña de Ventas Q3 - Actualizada",
        "total_calls": 350,
        "successful_calls": 280,
        "failed_calls": 70,
        "success_rate": 80,
        "average_duration": 260
      },
      // ...
    ],
    "timeline": [
      {
        "date": "2025-07-01",
        "total_calls": 120,
        "successful_calls": 95,
        "failed_calls": 25
      },
      // ...
    ]
  },
  "meta": {
    "filters": {
      "start_date": "2025-07-01",
      "end_date": "2025-07-31",
      "campaign_ids": ["456e7890-e12d-34f5-a678-901234567890"],
      "group_by": "day"
    }
  }
}
```

#### Reporte de Llamadas

```
GET /api/reports/calls
```

**Parámetros de Consulta**
- `start_date`: Fecha de inicio (YYYY-MM-DD)
- `end_date`: Fecha de fin (YYYY-MM-DD)
- `campaign_id`: ID de campaña (opcional)
- `status`: Estado de llamadas (opcional)

**Respuesta**
```json
{
  "data": {
    "summary": {
      "total_calls": 350,
      "by_status": {
        "completed": 280,
        "failed": 45,
        "no-answer": 25
      },
      "average_duration": 260,
      "busiest_hour": "10:00-11:00",
      "busiest_day": "Tuesday"
    },
    "calls": [
      {
        "id": "c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012",
        "contact_name": "Juan Pérez",
        "status": "completed",
        "duration": 307,
        "started_at": "2025-07-01T10:30:05Z",
        "recording_url": "https://storage.example.com/recordings/c3d4e5f6-a7b8-9012-c3d4-e5f6a7b89012.mp3"
      },
      // ...
    ]
  },
  "meta": {
    "filters": {
      "start_date": "2025-07-01",
      "end_date": "2025-07-31",
      "campaign_id": "456e7890-e12d-34f5-a678-901234567890",
      "status": null
    },
    "pagination": {
      "total": 350,
      "limit": 20,
      "offset": 0,
      "next_offset": 20,
      "prev_offset": null
    }
  }
}
```

## Modelos de Datos

### Campaign

| Campo               | Tipo      | Descripción                                   |
|---------------------|-----------|-----------------------------------------------|
| id                  | UUID      | Identificador único                           |
| name                | String    | Nombre de la campaña                          |
| description         | String    | Descripción detallada                         |
| status              | Enum      | Estado (draft, active, paused, completed, archived) |
| schedule_start      | DateTime  | Fecha y hora de inicio                        |
| schedule_end        | DateTime  | Fecha y hora de finalización                  |
| contact_list_ids    | UUID[]    | IDs de listas de contactos                    |
| script_template     | String    | Plantilla de script para llamadas             |
| max_retries         | Integer   | Número máximo de reintentos                   |
| retry_delay_minutes | Integer   | Tiempo entre reintentos (minutos)             |
| calling_hours_start | String    | Hora de inicio para llamadas (HH:MM)          |
| calling_hours_end   | String    | Hora de fin para llamadas (HH:MM)             |
| total_calls         | Integer   | Total de llamadas realizadas                  |
| successful_calls    | Integer   | Llamadas exitosas                             |
| failed_calls        | Integer   | Llamadas fallidas                             |
| pending_calls       | Integer   | Llamadas pendientes                           |
| created_at          | DateTime  | Fecha de creación                             |
| updated_at          | DateTime  | Fecha de última actualización                 |

### Contact

| Campo          | Tipo      | Descripción                                   |
|----------------|-----------|-----------------------------------------------|
| id             | UUID      | Identificador único                           |
| name           | String    | Nombre completo                               |
| phone_number   | String    | Número de teléfono                            |
| email          | String    | Dirección de email                            |
| notes          | String    | Notas adicionales                             |
| tags           | String[]  | Etiquetas para categorización                 |
| additional_data| Object    | Datos adicionales en formato JSON             |
| created_at     | DateTime  | Fecha de creación                             |
| updated_at     | DateTime  | Fecha de última actualización                 |

### Call

| Campo               | Tipo      | Descripción                                   |
|---------------------|-----------|-----------------------------------------------|
| id                  | UUID      | Identificador único                           |
| campaign_id         | UUID      | ID de la campaña                              |
| contact_id          | UUID      | ID del contacto                               |
| status              | Enum      | Estado (pending, in-progress, completed, failed, etc.) |
| scheduled_time      | DateTime  | Fecha y hora programada                       |
| started_at          | DateTime  | Fecha y hora de inicio                        |
| ended_at            | DateTime  | Fecha y hora de finalización                  |
| duration            | Integer   | Duración en segundos                          |
| recording_url       | String    | URL de la grabación                           |
| notes               | String    | Notas adicionales                             |
| twilio_sid          | String    | SID de Twilio                                 |
| retry_attempts      | Integer   | Número de intentos realizados                 |
| max_retries         | Integer   | Número máximo de reintentos                   |
| error_message       | String    | Mensaje de error (si aplica)                  |
| created_at          | DateTime  | Fecha de creación                             |
| updated_at          | DateTime  | Fecha de última actualización                 |

## Errores Comunes

| Código                | Descripción                                           |
|-----------------------|-------------------------------------------------------|
| INVALID_REQUEST       | La solicitud contiene datos inválidos                 |
| RESOURCE_NOT_FOUND    | El recurso solicitado no existe                       |
| AUTHENTICATION_FAILED | Fallo en la autenticación                             |
| PERMISSION_DENIED     | Sin permisos para realizar la operación               |
| VALIDATION_ERROR      | Error de validación en los datos enviados             |
| RATE_LIMIT_EXCEEDED   | Se ha excedido el límite de solicitudes               |
| TWILIO_ERROR          | Error en la integración con Twilio                    |
| ELEVENLABS_ERROR      | Error en la integración con ElevenLabs                |
| DATABASE_ERROR        | Error en la base de datos                             |
| INTERNAL_ERROR        | Error interno del servidor                            |

## Versionado

La API está versionada en la URL. La versión actual es `v1`:

```
https://api.example.com/api/v1/campaigns
```

## Límites de Tasa

Para prevenir abusos, la API implementa límites de tasa:

- 100 solicitudes por minuto por IP
- 1000 solicitudes por hora por usuario autenticado

Las respuestas incluyen encabezados para monitorear el uso:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1625097600
```

## Mejores Prácticas

1. **Utilizar paginación** para colecciones grandes
2. **Incluir solo los campos necesarios** en las solicitudes
3. **Manejar errores** adecuadamente en el cliente
4. **Implementar reintentos** con backoff exponencial para errores temporales
5. **Validar datos** antes de enviarlos a la API
6. **Utilizar HTTPS** para todas las solicitudes
7. **Almacenar tokens** de forma segura

## Herramientas de Desarrollo

- **Documentación Interactiva**: Disponible en `/docs` cuando el servidor está en modo desarrollo
- **Colección Postman**: Disponible para descarga en `/api/postman-collection`
- **OpenAPI Spec**: Disponible en `/api/openapi.json`
