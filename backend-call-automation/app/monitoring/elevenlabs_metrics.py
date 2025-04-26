from prometheus_client import Counter, Histogram, Gauge

# Métricas básicas para la integración con ElevenLabs

# Contador para el total de solicitudes a la API de ElevenLabs
# Etiquetas:
# - method: El método de la API llamado (e.g., 'generate_audio', 'generate_response', 'start_conversation')
# - status: El resultado de la solicitud ('success', 'error')
elevenlabs_requests_total = Counter(
    'elevenlabs_requests_total',
    'Total number of requests to ElevenLabs API',
    ['method', 'status']
)

# Histograma para la latencia de las solicitudes a la API de ElevenLabs
# Etiquetas:
# - method: El método de la API llamado
elevenlabs_request_duration_seconds = Histogram(
    'elevenlabs_request_duration_seconds',
    'Request latency in seconds for ElevenLabs API calls',
    ['method']
    # Se pueden ajustar los buckets según la latencia esperada
    # buckets=(0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, float("inf"))
)

# Gauge para el número de conexiones activas en el pool de ElevenLabs
elevenlabs_pool_connections_active = Gauge(
    'elevenlabs_pool_connections_active',
    'Number of active connections in the ElevenLabs connection pool'
)

# Gauge para el tamaño configurado del pool de conexiones
elevenlabs_pool_size = Gauge(
    'elevenlabs_pool_size',
    'Configured size of the ElevenLabs connection pool'
)

# Contador para errores específicos durante la interacción con ElevenLabs
# Etiquetas:
# - error_type: El tipo de error ocurrido (e.g., 'ConnectionError', 'TimeoutError', 'APIError')
elevenlabs_errors_total = Counter(
    'elevenlabs_errors_total',
    'Total number of specific errors encountered with ElevenLabs API',
    ['error_type']
)

# Histograma para la duración de la generación de audio (tiempo específico de síntesis)
# Podría ser útil si la librería o la API proporcionan esta información
elevenlabs_generation_duration_seconds = Histogram(
    'elevenlabs_generation_duration_seconds',
    'Duration of the audio generation process itself',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0], # Adjust buckets as needed
    labelnames=['voice'] # Podría etiquetarse por voz si es relevante
)

# Gauge para la calidad del audio generado (si se puede medir)
elevenlabs_audio_quality_score = Histogram(
    'elevenlabs_audio_quality_score',
    'Calidad del audio generado',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)

# Gauge para el ratio de uso del pool de conexiones
elevenlabs_pool_usage_ratio = Gauge(
    'elevenlabs_pool_usage_ratio',
    'Ratio de uso del pool de conexiones'
)

# Contador para el número total de reintentos
elevenlabs_retry_count_total = Counter(
    'elevenlabs_retry_count_total',
    'Número total de reintentos',
    ['method'] # Etiquetar por método para ver dónde ocurren los reintentos
)

# Contador para fallos en el streaming (si se implementa lógica específica de streaming)
# elevenlabs_stream_failures_total = Counter(
#     'elevenlabs_stream_failures_total',
#     'Total number of failures during audio streaming with ElevenLabs'
# )

# Ejemplo de cómo usar las métricas (esto iría en el código del servicio):
# from .elevenlabs_metrics import elevenlabs_requests_total, elevenlabs_request_duration_seconds

# @elevenlabs_request_duration_seconds.labels(method='generate_audio').time()
# async def generate_audio(...):
#     try:
#         # ... lógica de la llamada a la API ...
#         elevenlabs_requests_total.labels(method='generate_audio', status='success').inc()
#     except Exception as e:
