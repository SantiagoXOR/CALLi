"""Servicio de monitoreo para registrar métricas y trazas del sistema de llamadas automatizadas."""

from typing import Any
import logging
from prometheus_client import Counter, Histogram, Gauge, Summary
import time
from app.config.metrics_config import get_metrics_settings, MetricNames

logger = logging.getLogger(__name__)

# Obtener configuración de métricas
metrics_settings = get_metrics_settings()

# Definición de métricas globales para evitar reinicialización
CALL_LATENCY = Histogram(MetricNames.CALL_LATENCY, "Tiempo de latencia de llamadas")
AUDIO_QUALITY = Gauge(MetricNames.AUDIO_QUALITY, "Puntuación de calidad de audio")
TOTAL_CALLS = Counter(MetricNames.TOTAL_CALLS, "Número total de llamadas procesadas")
CALL_DURATION = Summary(MetricNames.CALL_DURATION, "Duración de las llamadas")

# Diccionario para almacenar métricas en caché si es necesario
METRICS_CACHE: dict[str, dict[str, Any]] = {}


class MetricsClient:
    """Cliente para enviar métricas a Prometheus.

    Esta clase proporciona una interfaz unificada para registrar diferentes tipos de métricas
    utilizando la biblioteca prometheus_client.
    """

    def histogram(self, name: str, value: float, labels: dict[str, str] | None = None):
        """Registra un valor en un histograma.

        Args:
            name (str): Nombre del histograma
            value (float): Valor a registrar
            labels (dict[str, str] | None): Etiquetas para categorizar la métrica
        """
        if name == "call_latency":
            if labels:
                # En una implementación real, se usarían las etiquetas correctamente
                CALL_LATENCY.observe(value)
            else:
                CALL_LATENCY.observe(value)
        logger.debug(f"Prometheus histogram: {name}={value} {labels}")

    def gauge(self, name: str, value: float, labels: dict[str, str] | None = None):
        """Registra un valor en un gauge.

        Args:
            name (str): Nombre del gauge
            value (float): Valor a registrar
            labels (dict[str, str] | None): Etiquetas para categorizar la métrica
        """
        if name == "audio_quality":
            if labels:
                # En una implementación real, se usarían las etiquetas correctamente
                AUDIO_QUALITY.set(value)
            else:
                AUDIO_QUALITY.set(value)
        logger.debug(f"Prometheus gauge: {name}={value} {labels}")

    def counter(self, name: str):
        """Devuelve un contador que puede incrementarse.

        Args:
            name (str): Nombre del contador

        Returns:
            CounterWrapper: Objeto contador que puede incrementarse
        """

        class CounterWrapper:
            def inc(self, labels: dict[str, str] | None = None):
                """Incrementa el contador.

                Args:
                    labels (dict[str, str] | None): Etiquetas para categorizar la métrica
                """
                if name == "total_calls":
                    TOTAL_CALLS.inc()
                logger.debug(f"Prometheus counter: {name} increment {labels}")

        return CounterWrapper()


class OpenTelemetryClient:
    """Cliente para enviar trazas a OpenTelemetry.

    Esta clase proporciona una interfaz para crear y gestionar spans de trazabilidad
    distribuida utilizando OpenTelemetry.
    """

    def __init__(self):
        # En un entorno real, aquí se inicializaría la conexión con OpenTelemetry
        pass

    def start_span(self, name: str):
        """Inicia un span de trazabilidad.

        Args:
            name: Nombre del span

        Returns:
            Span: Objeto span que puede utilizarse como contexto
        """

        class Span:
            def __enter__(self):
                """Método para iniciar el span al entrar en el contexto."""
                logger.info(f"OpenTelemetry: Starting span {name}")
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                """Método para finalizar el span al salir del contexto."""
                logger.info(f"OpenTelemetry: Ending span {name}")

            def set_attribute(self, key: str, value: Any):
                """Establece un atributo en el span.

                Args:
                    key (str): Nombre del atributo
                    value (Any): Valor del atributo
                """
                logger.info(f"OpenTelemetry: Setting attribute {key}={value}")
                # Implementación real conectaría con OpenTelemetry

        return Span()


class MonitoringService:
    """Servicio principal de monitoreo que integra métricas y trazabilidad.

    Este servicio proporciona métodos para registrar métricas de llamadas y
    crear trazas distribuidas para seguir el flujo de ejecución de las llamadas.
    """

    def __init__(self):
        """Inicializa el servicio de monitoreo con clientes para métricas y trazas."""
        self.metrics_client = MetricsClient()
        self.tracing_client = OpenTelemetryClient()

    async def record_call_metrics(self, call_id: str, metrics: dict[str, float]):
        """Registra métricas de llamada en Prometheus.

        Args:
            call_id (str): Identificador único de la llamada
            metrics (dict[str, float]): Diccionario con métricas como latencia y calidad de audio
        """
        # Registrar directamente en las métricas globales para mayor eficiencia
        CALL_LATENCY.observe(metrics["latency"])
        AUDIO_QUALITY.set(metrics["audio_quality"])
        TOTAL_CALLS.inc()

        # Si hay duración de llamada disponible, registrarla
        if "duration" in metrics:
            CALL_DURATION.observe(metrics["duration"])

        # Almacenar en caché si es necesario para análisis posterior
        METRICS_CACHE[call_id] = {
            "timestamp": time.time(),
            **metrics,
        }

    async def trace_call_flow(self, call_id: str, context: dict[str, Any]):
        """Implementa trazabilidad distribuida para seguir el flujo de una llamada.

        Args:
            call_id (str): Identificador único de la llamada
            context (dict[str, Any]): Contexto adicional para la traza, como sentimiento del usuario y duración
        """
        with self.tracing_client.start_span(f"call_{call_id}") as span:
            span.set_attribute("user_sentiment", context.get("sentiment"))
            span.set_attribute("call_duration", context.get("duration"))
