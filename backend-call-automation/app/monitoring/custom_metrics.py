"""
Módulo para definir métricas personalizadas de Prometheus.

Este módulo contiene clases y funciones para crear y gestionar métricas
personalizadas de Prometheus, incluyendo colectores personalizados.
"""

import logging
from collections.abc import Iterable

from prometheus_client import Counter, Gauge, Histogram
from prometheus_client.metrics_core import Metric
from prometheus_client.registry import REGISTRY, Collector, CollectorRegistry

# Configurar logger
logger = logging.getLogger(__name__)

# Métricas básicas
api_requests_total = Counter(
    "api_requests_total", "Total number of API requests", ["method", "endpoint", "status"]
)

api_request_duration_seconds = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
)

active_users = Gauge("active_users", "Number of active users")


class CustomCollector(Collector):
    """
    Colector personalizado para métricas específicas de la aplicación.

    Este colector permite definir métricas personalizadas que no se pueden
    crear fácilmente con los tipos estándar de Prometheus.
    """

    def __init__(self, registry: CollectorRegistry | None = REGISTRY):
        """
        Inicializa el colector personalizado.

        Args:
            registry: Registro de Prometheus donde registrar el colector
        """
        self._metrics: list[Metric] = []
        if registry:
            try:
                registry.register(self)
                logger.info("CustomCollector registered successfully")
            except Exception as e:
                logger.error(f"Error registering CustomCollector: {e}")

    def collect(self) -> Iterable[Metric]:
        """
        Recopila las métricas personalizadas.

        Returns:
            Iterable de métricas
        """
        return self._metrics

    def add_metric(self, metric: Metric) -> None:
        """
        Añade una métrica al colector.

        Args:
            metric: Métrica a añadir
        """
        self._metrics.append(metric)


# Crear una instancia del colector personalizado
custom_collector = CustomCollector()
