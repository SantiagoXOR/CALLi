"""Servicio de alertas para monitorear y notificar problemas en el sistema de llamadas automatizadas."""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class AlertService:
    """Servicio para gestionar alertas y notificaciones del sistema.

    Este servicio se encarga de detectar problemas, enviar alertas y correlacionar
    eventos para identificar patrones de fallos en el sistema de llamadas.

    Attributes:
        alerts_history (List): Historial de alertas enviadas
        settings (Dict): Configuración de umbrales y parámetros para las alertas
    """

    def __init__(self):
        self.alerts_history = []
        self.settings = {
            "MAX_LATENCY_MS": 500,  # Umbral máximo de latencia en ms
            "MAX_ERROR_RATE": 5.0,  # Tasa máxima de error en porcentaje
            "ERROR_WINDOW_MINUTES": 5,  # Ventana de tiempo para calcular tasa de error
        }

    async def send_alert(self, level: str, message: str, context: Dict[str, Any] = None):
        """
        Envía una alerta al sistema de monitoreo

        Args:
            level: Nivel de alerta (info, warning, critical)
            message: Mensaje de alerta
            context: Contexto adicional para la alerta
        """
        alert = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "context": context or {},
        }

        # Registrar alerta en el historial
        self.alerts_history.append(alert)

        # Registrar en logs según nivel
        if level == "critical":
            logger.critical(f"ALERTA CRÍTICA: {message}")
        elif level == "warning":
            logger.warning(f"ALERTA: {message}")
        else:
            logger.info(f"INFO: {message}")

        # En un entorno real, aquí se enviaría la alerta a un sistema externo
        # como PagerDuty, Slack, correo electrónico, etc.

    async def correlate_alerts(self, window_minutes: int = 5) -> List[Dict]:
        """
        Correlaciona alertas para detectar patrones

        Args:
            window_minutes: Ventana de tiempo en minutos

        Returns:
            List[Dict]: Lista de patrones detectados
        """
        recent_alerts = [
            alert
            for alert in self.alerts_history
            if (datetime.now() - datetime.fromisoformat(alert["timestamp"])).total_seconds()
            < window_minutes * 60
        ]

        patterns = []
        if len([a for a in recent_alerts if "latencia" in a["message"]]) > 3:
            patterns.append(
                {
                    "type": "persistent_latency",
                    "severity": "high",
                    "affected_calls": self._get_affected_calls(recent_alerts),
                }
            )

        return patterns

    def _get_affected_calls(self, alerts: List[Dict]) -> List[str]:
        """
        Extrae los IDs de llamadas afectadas de las alertas

        Args:
            alerts: Lista de alertas a analizar

        Returns:
            List[str]: Lista de IDs de llamadas afectadas
        """
        call_ids = []
        for alert in alerts:
            context = alert.get("context", {})
            if "call_id" in context and context["call_id"] not in call_ids:
                call_ids.append(context["call_id"])
        return call_ids

    async def check_quality_thresholds(self, metrics: Dict[str, float]):
        """
        Verifica umbrales de calidad y envía alertas

        Args:
            metrics: Métricas a verificar
        """
        if metrics.get("latency", 0) > self.settings["MAX_LATENCY_MS"]:
            # Correlacionar alertas para determinar severidad
            patterns = await self.correlate_alerts()
            severity = "critical" if patterns else "warning"

            await self.send_alert(
                level=severity,
                message=f"Alta latencia detectada: {metrics['latency']}ms",
                context={"patterns": patterns, **metrics},
            )

        if metrics.get("audio_quality", 1.0) < 0.5:
            await self.send_alert(
                level="warning",
                message=f"Baja calidad de audio: {metrics['audio_quality']}",
                context=metrics,
            )

    async def calculate_error_rate(self, window_minutes: int = 5) -> float:
        """
        Calcula la tasa de error en una ventana de tiempo

        Args:
            window_minutes: Ventana de tiempo en minutos

        Returns:
            float: Tasa de error en porcentaje
        """
        # En un entorno real, esto consultaría una base de datos o sistema de métricas
        # Por ahora, simulamos un cálculo basado en el historial de alertas

        window_start = datetime.now() - timedelta(minutes=window_minutes)

        # Contar errores en la ventana de tiempo
        error_count = sum(
            1
            for alert in self.alerts_history
            if alert["level"] in ["warning", "critical"]
            and datetime.fromisoformat(alert["timestamp"]) >= window_start
        )

        # Simular un total de solicitudes (en un entorno real vendría de métricas)
        total_requests = 100  # Valor simulado

        # Calcular tasa de error
        if total_requests > 0:
            return (error_count / total_requests) * 100.0
        return 0.0

    async def monitor_error_rates(self, window_minutes: int = 5):
        """
        Monitorea tasas de error y alerta si superan umbrales

        Args:
            window_minutes: Ventana de tiempo en minutos
        """
        error_rate = await self.calculate_error_rate(window_minutes)

        if error_rate > self.settings["MAX_ERROR_RATE"]:
            await self.send_alert(
                level="critical",
                message=f"Alta tasa de error: {error_rate}%",
                context={"window_minutes": window_minutes, "error_rate": error_rate},
            )

        # Registrar métrica para seguimiento
        logger.info(f"Tasa de error actual: {error_rate}% (ventana: {window_minutes} min)")
