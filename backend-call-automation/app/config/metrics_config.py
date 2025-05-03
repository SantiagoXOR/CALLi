"""Configuración centralizada para el sistema de métricas y monitoreo."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class MetricsSettings(BaseSettings):
    """
    Configuración para el sistema de métricas y monitoreo.

    Attributes:
        enabled (bool): Indica si el sistema de métricas está habilitado
        prometheus_endpoint (str): URL del endpoint de Prometheus
        opentelemetry_enabled (bool): Indica si OpenTelemetry está habilitado
        log_level (str): Nivel de log para las métricas
        retention_days (int): Días de retención de métricas históricas
        alert_thresholds (Dict[str, float]): Umbrales para alertas de métricas
    """

    enabled: bool = True
    prometheus_endpoint: str = "http://localhost:9090"
    opentelemetry_enabled: bool = False
    log_level: str = "INFO"
    retention_days: int = 30
    alert_thresholds: dict[str, float] = {
        "call_latency": 5.0,  # segundos
        "audio_quality": 0.7,  # puntuación mínima
        "ai_response_time": 3.0,  # segundos
        "error_rate": 0.05,  # 5% de tasa de error
    }

    # Métricas que se deben recopilar
    enabled_metrics: list[str] = [
        "call_latency",
        "audio_quality",
        "total_calls",
        "call_duration",
        "ai_response_time",
        "ai_requests_total",
        "ai_errors_total",
        "ai_sentiment_score",
        "ai_tokens_used",
    ]

    class Config:
        env_prefix = "METRICS_"
        case_sensitive = False


@lru_cache
def get_metrics_settings() -> MetricsSettings:
    """
    Obtiene la configuración de métricas con caché para evitar recargas innecesarias.

    Returns:
        MetricsSettings: Configuración de métricas
    """
    return MetricsSettings()


# Constantes para nombres de métricas
class MetricNames:
    """
    Nombres de métricas utilizados en toda la aplicación.
    Centralizar los nombres evita errores de tipeo y mantiene consistencia.
    """

    # Métricas de llamadas
    CALL_LATENCY = "call_latency_seconds"
    AUDIO_QUALITY = "audio_quality_score"
    TOTAL_CALLS = "total_calls"
    CALL_DURATION = "call_duration_seconds"

    # Métricas de IA
    AI_RESPONSE_TIME = "ai_response_time_seconds"
    AI_REQUESTS_TOTAL = "ai_requests_total"
    AI_ERRORS_TOTAL = "ai_errors_total"
    AI_SENTIMENT_SCORE = "ai_sentiment_score"
    AI_TOKENS_USED = "ai_tokens_used"
