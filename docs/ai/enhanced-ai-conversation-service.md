# Servicio Mejorado de Conversación con IA

## Descripción

El Servicio Mejorado de Conversación con IA es una evolución del servicio original, diseñado para proporcionar respuestas más personalizadas y contextuales según el tipo de campaña. Este servicio utiliza prompts optimizados para diferentes escenarios de llamadas, mejorando significativamente la calidad de las interacciones.

## Características Principales

- **Prompts optimizados por tipo de campaña**: Plantillas específicas para ventas, soporte, encuestas, seguimiento, educación y retención.
- **Personalización avanzada**: Adaptación de respuestas según el contexto específico de la campaña y el cliente.
- **Análisis de sentimientos**: Evaluación del tono emocional de los mensajes para adaptar las respuestas.
- **Sugerencias de acciones**: Recomendaciones inteligentes sobre los siguientes pasos a seguir en la conversación.
- **Soporte para múltiples proveedores de IA**: Integración con OpenAI y Google AI.
- **Gestión de memoria de conversación**: Mantenimiento del contexto a lo largo de la interacción.

## Tipos de Campañas Soportados

### 1. Ventas (Sales)

Optimizado para presentar productos o servicios, destacar beneficios y manejar objeciones de manera efectiva.

**Variables específicas:**
- `product`: Producto o servicio que se está vendiendo
- `objective`: Objetivo principal de la llamada
- `key_points`: Puntos clave a mencionar
- `company_name`: Nombre de la empresa
- `contact_name`: Nombre del contacto
- `contact_history`: Historial previo con el cliente

### 2. Soporte (Support)

Diseñado para resolver problemas técnicos, proporcionar asistencia y mejorar la satisfacción del cliente.

**Variables específicas:**
- `product`: Producto o servicio para el que se brinda soporte
- `common_issues`: Problemas comunes y sus soluciones
- `company_name`: Nombre de la empresa
- `contact_name`: Nombre del contacto
- `support_history`: Historial de soporte previo

### 3. Encuestas (Survey)

Optimizado para recopilar información, opiniones y feedback de manera estructurada y no invasiva.

**Variables específicas:**
- `topic`: Tema de la encuesta
- `key_questions`: Preguntas principales a realizar
- `contact_name`: Nombre del participante

### 4. Seguimiento (Follow-up)

Diseñado para dar continuidad a interacciones previas, verificar satisfacción y avanzar en el proceso de venta o soporte.

**Variables específicas:**
- `objective`: Objetivo del seguimiento
- `previous_interaction`: Resumen de la interacción anterior
- `company_name`: Nombre de la empresa
- `contact_name`: Nombre del contacto
- `contact_history`: Historial completo con el cliente

### 5. Educativo (Educational)

Optimizado para explicar conceptos, proporcionar información y responder preguntas de manera didáctica.

**Variables específicas:**
- `topic`: Tema educativo
- `educational_goals`: Objetivos de aprendizaje
- `key_points`: Conceptos clave a transmitir
- `company_name`: Nombre de la organización
- `contact_name`: Nombre del participante
- `knowledge_level`: Nivel de conocimiento previo (básico, intermedio, avanzado)

### 6. Retención (Retention)

Diseñado para prevenir la cancelación de servicios, abordar insatisfacciones y ofrecer soluciones para mantener al cliente.

**Variables específicas:**
- `objective`: Objetivo de retención
- `company_name`: Nombre de la empresa
- `contact_name`: Nombre del cliente
- `customer_tenure`: Tiempo como cliente
- `current_services`: Servicios actuales contratados
- `cancellation_reason`: Motivo de posible cancelación

## Integración con el Modelo de Campaña

El servicio se integra con el modelo de campaña a través de los siguientes campos:

- `campaign_type`: Determina el tipo de plantilla de prompt a utilizar
- `ai_config`: Configuración específica para el modelo de IA
- `key_points`: Puntos clave a mencionar durante la conversación

## Ejemplo de Uso

```python
from app.services.enhanced_ai_conversation_service import EnhancedAIConversationService

# Inicializar el servicio
ai_service = EnhancedAIConversationService()

# Procesar un mensaje en una campaña de ventas
response = await ai_service.process_message(
    message="Me gustaría saber más sobre sus precios",
    campaign_type="sales",
    conversation_id="conv_123",
    context={
        "company_name": "TechSolutions Inc.",
        "product": "Software de Automatización",
        "objective": "Presentar beneficios y planes de precios",
        "key_points": [
            "Ahorro de tiempo del 40%",
            "Soporte 24/7 incluido",
            "Prueba gratuita de 30 días"
        ],
        "contact_name": "Juan Pérez"
    }
)

# Acceder a la respuesta y metadatos
print(response["response"])  # Respuesta generada
print(response["input_sentiment"])  # Análisis de sentimiento del mensaje
print(response["suggested_actions"])  # Acciones sugeridas
```

## Configuración Avanzada

El servicio puede configurarse a través de la clase `AISettings` en `app/config/ai_config.py`:

```python
# Configuración del proveedor de IA
LLM_PROVIDER: str = "google"  # "openai" o "google"
DEFAULT_MODEL: str = "gpt-4"
GOOGLE_MODEL: str = "gemini-pro"

# Parámetros de generación
MAX_TOKENS: int = 150
TEMPERATURE: float = 0.7

# Configuración de memoria
MAX_HISTORY_TOKENS: int = 2000
MEMORY_TTL: int = 86400  # 24 horas
```

## Mejores Prácticas

1. **Personalización de prompts**: Adaptar las plantillas según las necesidades específicas de cada tipo de campaña.
2. **Contexto enriquecido**: Proporcionar la mayor cantidad de información relevante en el contexto.
3. **Monitoreo de sentimientos**: Utilizar el análisis de sentimientos para adaptar el tono de las respuestas.
4. **Seguimiento de acciones sugeridas**: Implementar las acciones recomendadas por el sistema.
5. **Pruebas A/B**: Comparar diferentes configuraciones para optimizar resultados.

## Limitaciones y Consideraciones

- El servicio requiere una conexión estable a las APIs de OpenAI o Google.
- La calidad de las respuestas depende de la calidad del contexto proporcionado.
- Se recomienda implementar un sistema de fallback para manejar casos donde el servicio no esté disponible.
- Considerar las implicaciones éticas y de privacidad al utilizar IA en llamadas automatizadas.

## Próximas Mejoras

- Implementación de fine-tuning específico por industria
- Soporte para más idiomas y dialectos regionales
- Análisis avanzado de emociones con detección de tonos
- Integración con sistemas de conocimiento para respuestas más precisas
- Personalización dinámica de prompts basada en resultados previos
