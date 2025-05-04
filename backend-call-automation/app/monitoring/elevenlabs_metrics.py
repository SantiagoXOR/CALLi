"""
Módulo para la definición de métricas de Prometheus relacionadas con la integración de ElevenLabs.

Este módulo contiene contadores, histogramas y gauges para monitorear el rendimiento,
errores y estado de las interacciones con la API de ElevenLabs.
"""

from prometheus_client import Counter, Gauge, Histogram

# Métricas básicas para la integración con ElevenLabs

# Contador para el total de solicitudes a la API de ElevenLabs
# Etiquetas:
# - method: El método de la API llamado (e.g., 'generate_audio', 'generate_response')
# - status: El resultado de la solicitud ('success', 'error')
elevenlabs_requests_total = Counter(
    "elevenlabs_requests_total", "Total number of requests to ElevenLabs API", ["method", "status"]
)

# Histograma para la latencia de las solicitudes a la API de ElevenLabs
# Etiquetas:
# - method: El método de la API llamado
elevenlabs_request_duration_seconds = Histogram(
    "elevenlabs_request_duration_seconds",
    "Request latency in seconds for ElevenLabs API calls",
    ["method"],
    # Buckets ajustados a la latencia esperada
    buckets=[0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0],
)

# Gauge para el número de conexiones activas en el pool de ElevenLabs
elevenlabs_pool_connections_active = Gauge(
    "elevenlabs_pool_connections_active",
    "Number of active connections in the ElevenLabs connection pool",
)

# Gauge para el tamaño configurado del pool de conexiones
elevenlabs_pool_size = Gauge(
    "elevenlabs_pool_size", "Configured size of the ElevenLabs connection pool"
)

# Contador para errores específicos durante la interacción con ElevenLabs
# Etiquetas:
# - error_type: El tipo de error ocurrido (e.g., 'ConnectionError', 'TimeoutError', 'APIError')
elevenlabs_errors_total = Counter(
    "elevenlabs_errors_total",
    "Total number of specific errors encountered with ElevenLabs API",
    ["error_type"],
)

# Histograma para la duración de la generación de audio (tiempo específico de síntesis)
# Podría ser útil si la librería o la API proporcionan esta información
elevenlabs_generation_duration_seconds = Histogram(
    "elevenlabs_generation_duration_seconds",
    "Duration of the audio generation process itself",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0],  # Adjust buckets as needed
    labelnames=["voice"],  # Podría etiquetarse por voz si es relevante
)

# Gauge para la calidad del audio generado (si se puede medir)
elevenlabs_audio_quality_score = Histogram(
    "elevenlabs_audio_quality_score",
    "Calidad del audio generado",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)

# Gauge para el ratio de uso del pool de conexiones
elevenlabs_pool_usage_ratio = Gauge(
    "elevenlabs_pool_usage_ratio", "Ratio de uso del pool de conexiones"
)

# Contador para el número total de reintentos
elevenlabs_retry_count_total = Counter(
    "elevenlabs_retry_count_total",
    "Número total de reintentos",
    ["method"],  # Etiquetar por método para ver dónde ocurren los reintentos
)

# Métricas adicionales pueden ser agregadas según las necesidades del servicio
