"""Servicio para gestionar la caché y su sincronización con Supabase."""

import asyncio
import logging
from datetime import datetime

from app.config.redis_client import (
    clear_cache,
    get_cache_metrics,
    sync_to_supabase,
)
from app.models.cache_metrics import CacheMetrics

logger = logging.getLogger(__name__)


class CacheService:
    """Servicio para gestionar la caché y su sincronización con Supabase."""

    def __init__(self, sync_interval: int = 300) -> None:
        """Inicializa el servicio de caché.

        Args:
            sync_interval: Intervalo de sincronización en segundos (por defecto: 300)
        """
        self.sync_interval = sync_interval
        self.sync_task: asyncio.Task | None = None
        self._running = False
        self.settings = {
            "USAGE_THRESHOLD": 50,  # Umbral de uso para considerar hora pico
            "DEFAULT_TTL": 3600,  # TTL predeterminado (1 hora)
            "PEAK_TTL": 1800,  # TTL para horas pico (30 minutos)
            "DEFAULT_CACHE_SIZE": 1000,  # Tamaño predeterminado
            "PEAK_CACHE_SIZE": 2000,  # Tamaño para horas pico
        }
        self.hourly_access_stats: list[dict[str, float]] = []  # Estadísticas de acceso por hora

    async def start_sync_task(self) -> None:
        """Inicia la tarea de sincronización periódica."""
        if self.sync_task is None or self.sync_task.done():
            self._running = True
            self.sync_task = asyncio.create_task(self._sync_loop())
            logger.info(
                f"Tarea de sincronización iniciada con intervalo de {self.sync_interval} segundos"
            )

    async def stop_sync_task(self) -> None:
        """Detiene la tarea de sincronización periódica."""
        if self.sync_task and not self.sync_task.done():
            self._running = False
            self.sync_task.cancel()
            try:
                await self.sync_task
            except asyncio.CancelledError:
                pass
            logger.info("Tarea de sincronización detenida")

    async def _sync_loop(self) -> None:
        """Bucle de sincronización periódica."""
        while self._running:
            try:
                # Sincronizar conversaciones
                await sync_to_supabase("conversation_memories", "conversation:")

                # Esperar hasta el próximo intervalo
                await asyncio.sleep(self.sync_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error en bucle de sincronización: {e!s}")
                # Esperar un poco antes de reintentar
                await asyncio.sleep(10)

    async def get_metrics(self) -> CacheMetrics:
        """Obtiene las métricas actuales de la caché.

        Returns:
            CacheMetrics: Objeto con las métricas de caché
        """
        return await get_cache_metrics()

    async def predict_usage_patterns(self) -> dict[str, float]:
        """Predice patrones de uso para optimización proactiva

        Returns:
            Dict[str, float]: Predicciones de uso por hora
        """
        hourly_stats = await self._get_hourly_access_stats()
        predictions = {}

        for hour in range(24):
            # Análisis de series temporales simple
            recent_stats = [stats.get(str(hour), 0) for stats in hourly_stats[-7:]]  # Última semana
            if recent_stats:
                predictions[str(hour)] = sum(recent_stats) / len(recent_stats)
            else:
                predictions[str(hour)] = 0.0

        return predictions

    async def _get_hourly_access_stats(self) -> list[dict[str, float]]:
        """Obtiene estadísticas de acceso por hora de los últimos días

        Returns:
            List[Dict[str, float]]: Lista de estadísticas por hora
        """
        # En un entorno real, esto consultaría una base de datos o sistema de métricas
        # Por ahora, devolvemos datos simulados para los últimos 7 días
        simulated_data = []
        for day in range(7):
            day_stats = {}
            for hour in range(24):
                # Simular mayor uso en horas laborales (9-18)
                if 9 <= hour <= 18:
                    day_stats[str(hour)] = float(50 + (day % 3) * 10)  # Valor alto para horas pico
                else:
                    day_stats[str(hour)] = float(10 + (day % 3) * 5)  # Valor bajo para horas valle
            simulated_data.append(day_stats)
        return simulated_data

    async def optimize_cache_usage(self) -> None:
        """Optimización proactiva basada en predicciones"""
        patterns = await self.predict_usage_patterns()
        current_hour = str(datetime.now().hour)

        # Ajustar TTL y tamaño de caché para horas pico
        if patterns.get(current_hour, 0) > self.settings["USAGE_THRESHOLD"]:
            await self.expand_cache_size()
            await self.reduce_ttl()
            logger.info(f"Optimizando caché para hora pico ({current_hour}h)")
        else:
            await self.normalize_cache_settings()
            logger.info(f"Normalizando configuración de caché para hora valle ({current_hour}h)")

    async def expand_cache_size(self) -> None:
        """Expande el tamaño de la caché para horas pico"""
        # En un entorno real, esto ajustaría la configuración de Redis
        logger.info(f"Expandiendo tamaño de caché a {self.settings['PEAK_CACHE_SIZE']}")

    async def reduce_ttl(self) -> None:
        """Reduce el TTL para horas pico para mantener datos más frescos"""
        # En un entorno real, esto ajustaría la configuración de TTL en Redis
        logger.info(f"Reduciendo TTL a {self.settings['PEAK_TTL']} segundos")

    async def normalize_cache_settings(self) -> None:
        """Restaura configuración normal de caché"""
        # En un entorno real, esto restauraría la configuración predeterminada
        logger.info(
            f"Restaurando configuración normal: TTL={self.settings['DEFAULT_TTL']}, tamaño={self.settings['DEFAULT_CACHE_SIZE']}"
        )

    async def force_sync(self, table_name: str, key_prefix: str | None = None) -> bool:
        """Fuerza una sincronización inmediata con Supabase.

        Args:
            table_name: Nombre de la tabla en Supabase
            key_prefix: Prefijo de claves a sincronizar (opcional)

        Returns:
            bool: True si se sincronizó correctamente, False en caso contrario
        """
        return await sync_to_supabase(table_name, key_prefix)

    async def clear_all_cache(self) -> bool:
        """Limpia toda la caché.

        Returns:
            bool: True si se limpió correctamente, False en caso contrario
        """
        return await clear_cache()

    async def preload_conversation(self, conversation_id: str) -> bool:
        """Precarga una conversación desde Supabase a la caché.

        Args:
            conversation_id: ID de la conversación a precargar

        Returns:
            bool: True si se precargó correctamente, False en caso contrario
        """
        try:
            from app.config.redis_client import generate_conversation_cache_key, set_in_cache
            from app.config.supabase import supabase_client

            # Buscar en Supabase
            result = (
                supabase_client.table("conversation_memories")
                .select("memory_data")
                .eq("conversation_id", conversation_id)
                .execute()
            )

            # Si existe, guardar en caché
            if result.data and len(result.data) > 0:
                memory_data = result.data[0]["memory_data"]
                cache_key = generate_conversation_cache_key(conversation_id)

                # Guardar en caché
                return await set_in_cache(cache_key, memory_data)

            return False
        except Exception as e:
            logger.error(f"Error al precargar conversación: {e!s}")
            return False


# Instancia global del servicio
cache_service = CacheService()
