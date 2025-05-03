"""Modelo para las métricas de caché."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CacheMetrics(BaseModel):
    """Modelo que representa las métricas de caché."""

    total_keys: int = Field(default=0, description="Total de claves en caché")
    memory_used: str = Field(default="0", description="Memoria utilizada por Redis")
    hit_rate: float = Field(default=0.0, description="Ratio de aciertos (hits/total)")
    uptime: int = Field(default=0, description="Tiempo de actividad en segundos")

    # Campos adicionales para métricas detalladas
    total_requests: int = Field(default=0, description="Total de solicitudes a la caché")
    hits: int = Field(default=0, description="Número de aciertos en caché")
    misses: int = Field(default=0, description="Número de fallos en caché")
    hit_ratio: float = Field(default=0.0, description="Ratio de aciertos (hits/total_requests)")
    avg_latency_ms: float = Field(
        default=0.0, description="Latencia promedio de acceso a caché en ms"
    )
    memory_usage_bytes: int = Field(default=0, description="Uso de memoria en bytes")
    compression_ratio: float = Field(default=1.0, description="Ratio de compresión promedio")
    sync_count: int = Field(default=0, description="Número de sincronizaciones con Supabase")
    last_sync: datetime | None = Field(
        default=None, description="Última sincronización con Supabase"
    )

    model_config = ConfigDict(from_attributes=True)
