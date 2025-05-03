import logging
import time
from datetime import datetime
from typing import Any

from prometheus_client import Counter, Gauge, Histogram, Summary

from app.config.metrics_config import MetricNames, get_metrics_settings
from app.config.supabase import supabase_client

logger = logging.getLogger(__name__)

# Obtener configuración de métricas
metrics_settings = get_metrics_settings()

# Definición de métricas globales
AI_RESPONSE_TIME = Histogram(
    MetricNames.AI_RESPONSE_TIME, "Tiempo de procesamiento de respuestas de IA"
)
AI_REQUESTS_TOTAL = Counter(MetricNames.AI_REQUESTS_TOTAL, "Total de solicitudes de IA procesadas")
AI_ERRORS_TOTAL = Counter(MetricNames.AI_ERRORS_TOTAL, "Total de errores en procesamiento de IA")
AI_SENTIMENT_SCORE = Gauge(
    MetricNames.AI_SENTIMENT_SCORE, "Puntuación de sentimiento detectado por IA"
)
AI_TOKENS_USED = Summary(
    MetricNames.AI_TOKENS_USED, "Número de tokens utilizados en solicitudes de IA"
)

# Caché para métricas de IA
AI_METRICS_CACHE: dict[str, dict[str, Any]] = {}


class AIMetricsService:
    """
    Servicio para recopilar y registrar métricas relacionadas con el procesamiento de IA.

    Registra métricas importantes como tiempos de respuesta, número total
    de solicitudes y errores durante el procesamiento de IA.
    """

    @staticmethod
    async def record_metrics(
        start_time: float,
        success: bool,
        conversation_id: str | None = None,
        extra_metrics: dict[str, Any] | None = None,
    ) -> None:
        """
        Registra métricas de una operación de IA.

        Args:
            start_time: Tiempo de inicio de la operación (timestamp)
            success: Indica si la operación fue exitosa o no
            conversation_id: Identificador de la conversación si está disponible
            extra_metrics: Métricas adicionales como tokens, sentimiento, etc.
        """
        duration = time.time() - start_time
        AI_RESPONSE_TIME.observe(duration)
        AI_REQUESTS_TOTAL.inc()

        if not success:
            AI_ERRORS_TOTAL.inc()

        # Registrar métricas adicionales si están disponibles
        if extra_metrics:
            if "sentiment_score" in extra_metrics:
                AI_SENTIMENT_SCORE.set(extra_metrics["sentiment_score"])

            if "tokens_used" in extra_metrics:
                AI_TOKENS_USED.observe(extra_metrics["tokens_used"])

        # Almacenar en caché si hay ID de conversación
        if conversation_id and extra_metrics:
            AI_METRICS_CACHE[conversation_id] = {
                "timestamp": time.time(),
                "duration": duration,
                "success": success,
                **extra_metrics,
            }

        logger.debug(f"Métricas de IA registradas: duración={duration:.2f}s, éxito={success}")

    @staticmethod
    def get_metrics_summary() -> dict[str, Any]:
        """
        Obtiene un resumen de las métricas de IA registradas.

        Returns:
            dict[str, Any]: Resumen con:
                total_requests: Total de solicitudes procesadas
                total_errors: Total de errores registrados
                cached_conversations: Número de conversaciones en caché
        """
        return {
            "total_requests": float(AI_REQUESTS_TOTAL._value.get()),
            "total_errors": float(AI_ERRORS_TOTAL._value.get()),
            "cached_conversations": len(AI_METRICS_CACHE),
        }

    @staticmethod
    async def record_conversation_metrics(conversation_id: str, metrics: dict[str, Any]) -> None:
        """Registra métricas de conversación."""
        try:
            # Guardar en Supabase
            await (
                supabase_client.table("conversation_metrics")
                .insert(
                    {
                        "conversation_id": conversation_id,
                        "timestamp": datetime.now().isoformat(),
                        "input_sentiment": metrics["input_sentiment"],
                        "response_sentiment": metrics["response_sentiment"],
                        "response_time": metrics.get("response_time", 0),
                        "tokens_used": metrics.get("tokens_used", 0),
                    }
                )
                .execute()
            )

            # Actualizar métricas en tiempo real
            await AIMetricsService.record_metrics(
                start_time=time.time(),
                success=True,
                conversation_id=conversation_id,
                extra_metrics=metrics,
            )
        except Exception as e:
            logger.error(f"Error registrando métricas: {e!s}")
