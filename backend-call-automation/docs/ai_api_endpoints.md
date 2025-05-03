# Endpoints de IA

## Procesar Mensaje

`POST /api/v1/ai/process`

**Request Body:**

```json
{
    "message": "¿Cuál es el precio?",
    "context": {
        "campaign_type": "sales",
        "product": "Premium Plan"
    },
    "conversation_id": "conv_123"
}
```

**Response:**

```json
{
    "response": "El Plan Premium tiene un costo de $99/mes",
    "confidence": 0.85,
    "sentiment": {
        "positive": 0.7,
        "neutral": 0.3,
        "negative": 0.0
    },
    "next_actions": ["send_pricing", "schedule_follow_up"]
}
```

### Obtener Historial de Conversación

```http
GET /api/v1/ai/conversation/{conversation_id}/history
```

**Descripción**: Recupera el historial completo de una conversación.

**Parámetros de URL**:

- `conversation_id` (string, requerido): Identificador único de la conversación.

**Respuesta Exitosa (200 OK)**:

```json
{
  "conversation_id": "conv_123",
  "messages": [
    {
      "role": "system",
      "content": "Eres un vendedor profesional...",
      "timestamp": "2023-06-15T14:30:00Z"
    },
    {
      "role": "user",
      "content": "¿Cuáles son los beneficios del producto?",
      "timestamp": "2023-06-15T14:30:30Z"
    },
    {
      "role": "assistant",
      "content": "Nuestro Software CRM ofrece múltiples beneficios...",
      "timestamp": "2023-06-15T14:30:45Z"
    }
  ]
}
```

## Endpoints de Generación de Audio

### Generar Audio

```http
POST /api/v1/ai/tts/generate
```

**Descripción**: Genera audio a partir de texto utilizando el servicio ElevenLabs.

**Cuerpo de la Solicitud**:

```json
{
  "text": "Hola, ¿cómo puedo ayudarte hoy?",
  "voice": "Bella"
}
```

**Respuesta Exitosa (200 OK)**:

```text
Contenido binario del audio (audio/mpeg)
```

**Encabezados de Respuesta**:

- `Content-Type`: audio/mpeg
- `Content-Disposition`: attachment; filename="audio.mp3"

## Endpoints de Configuración

### Obtener Configuración de IA

```http
GET /api/v1/ai/config
```

**Descripción**: Recupera la configuración actual de los servicios de IA.

**Respuesta Exitosa (200 OK)**:

```json
{
  "default_model": "gpt-4",
  "max_tokens": 150,
  "temperature": 0.7,
  "available_voices": [
    "Bella",
    "Antonio",
    "Emma",
    "Thomas"
  ]
}
```

### Actualizar Configuración de IA

```http
PUT /api/v1/ai/config
```

**Descripción**: Actualiza la configuración de los servicios de IA.

**Cuerpo de la Solicitud**:

```json
{
  "default_model": "gpt-4",
  "max_tokens": 200,
  "temperature": 0.8
}
```

**Respuesta Exitosa (200 OK)**:

```json
{
  "message": "Configuración actualizada correctamente",
  "updated_fields": ["max_tokens", "temperature"]
}
```

## Endpoints de Prompts

### Obtener Prompts Predefinidos

```http
GET /api/v1/ai/prompts
```

**Descripción**: Recupera los prompts predefinidos disponibles en el sistema.

**Respuesta Exitosa (200 OK)**:

```json
{
  "sales": "Eres un vendedor profesional experto en {product}"
}
```
