# Servicio de Caché

## Visión General

El `CacheService` es un componente fundamental del sistema de automatización de llamadas que proporciona una capa de caché para mejorar el rendimiento y reducir la carga en la base de datos. Implementa estrategias avanzadas de caché, incluyendo sincronización con Supabase, gestión de TTL (Time-To-Live) adaptativa y optimización basada en patrones de uso.

## Funcionalidades Principales

### 1. Gestión de Caché

- **Almacenamiento y recuperación**: Interfaz para almacenar y recuperar datos en caché
- **Invalidación**: Mecanismos para invalidar entradas de caché obsoletas
- **Gestión de TTL**: Configuración de tiempo de vida para diferentes tipos de datos
- **Compresión**: Compresión opcional de datos para reducir el uso de memoria

### 2. Sincronización con Base de Datos

- **Sincronización periódica**: Sincronización automática con Supabase a intervalos configurables
- **Sincronización bajo demanda**: Capacidad para forzar la sincronización cuando sea necesario
- **Resolución de conflictos**: Estrategias para resolver conflictos durante la sincronización

### 3. Optimización de Rendimiento

- **Caché adaptativa**: Ajuste automático de parámetros de caché según patrones de uso
- **Precarga**: Capacidad para precargar datos frecuentemente accedidos
- **Estadísticas de uso**: Recopilación y análisis de estadísticas de acceso a caché

### 4. Monitoreo y Métricas

- **Métricas de rendimiento**: Tasa de aciertos/fallos, latencia, uso de memoria
- **Alertas**: Configuración de alertas para problemas de rendimiento
- **Exportación de métricas**: Integración con Prometheus para monitoreo

## Implementación

### Clase Principal

```python
class CacheService:
    """Servicio para gestionar la caché y su sincronización con Supabase."""

    def __init__(self, sync_interval: int = 300):
        """Inicializa el servicio de caché.

        Args:
            sync_interval: Intervalo de sincronización en segundos (por defecto: 300)
        """
        self.sync_interval = sync_interval
        self.sync_task = None
        self._running = False
        self.settings = {
            "USAGE_THRESHOLD": 50,  # Umbral de uso para considerar hora pico
            "DEFAULT_TTL": 3600,  # TTL predeterminado (1 hora)
            "PEAK_TTL": 1800,  # TTL para horas pico (30 minutos)
            "DEFAULT_CACHE_SIZE": 1000,  # Tamaño predeterminado
            "PEAK_CACHE_SIZE": 2000,  # Tamaño para horas pico
        }
        self.hourly_access_stats = []  # Estadísticas de acceso por hora
```

### Métodos Principales

#### Gestión de Caché

```python
async def get(self, key: str) -> Optional[Dict]:
    """Obtiene un valor de la caché.

    Args:
        key: Clave a buscar

    Returns:
        El valor almacenado o None si no existe
    """
    return await get_from_cache(key)

async def set(self, key: str, value: Dict, ttl: Optional[int] = None) -> bool:
    """Almacena un valor en la caché.

    Args:
        key: Clave para almacenar el valor
        value: Valor a almacenar
        ttl: Tiempo de vida en segundos (opcional)

    Returns:
        True si se almacenó correctamente, False en caso contrario
    """
    # Determinar TTL basado en la hora del día y patrones de uso
    if ttl is None:
        ttl = self._get_adaptive_ttl()

    # Registrar estadística de acceso
    self._record_access(key)

    return await set_in_cache(key, value, ttl)

async def delete(self, key: str) -> bool:
    """Elimina un valor de la caché.

    Args:
        key: Clave a eliminar

    Returns:
        True si se eliminó correctamente, False en caso contrario
    """
    return await delete_from_cache(key)
```

#### Sincronización con Base de Datos

```python
async def start_sync(self) -> None:
    """Inicia la tarea de sincronización periódica con Supabase."""
    if self._running:
        return

    self._running = True
    self.sync_task = asyncio.create_task(self._sync_loop())
    logger.info(f"Iniciada sincronización de caché cada {self.sync_interval} segundos")

async def stop_sync(self) -> None:
    """Detiene la tarea de sincronización periódica."""
    if not self._running:
        return

    self._running = False
    if self.sync_task:
        self.sync_task.cancel()
        try:
            await self.sync_task
        except asyncio.CancelledError:
            pass
    logger.info("Detenida sincronización de caché")

async def _sync_loop(self) -> None:
    """Bucle de sincronización periódica con Supabase."""
    while self._running:
        try:
            await self._sync_to_supabase()
            await asyncio.sleep(self.sync_interval)
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error en sincronización de caché: {str(e)}")
            await asyncio.sleep(10)  # Esperar antes de reintentar

async def _sync_to_supabase(self) -> None:
    """Sincroniza la caché con Supabase."""
    logger.debug("Iniciando sincronización con Supabase")
    start_time = datetime.now()

    # Obtener datos a sincronizar
    keys_to_sync = await self._get_keys_to_sync()

    # Sincronizar datos
    synced_count = await sync_to_supabase(keys_to_sync)

    # Registrar métricas
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"Sincronización completada: {synced_count} elementos en {duration:.2f} segundos")
```

#### Optimización de Rendimiento

```python
def _get_adaptive_ttl(self) -> int:
    """Determina el TTL adaptativo basado en patrones de uso.

    Returns:
        TTL en segundos
    """
    current_hour = datetime.now().hour

    # Determinar si es hora pico basado en estadísticas
    is_peak_hour = self._is_peak_hour(current_hour)

    # Usar TTL más corto en horas pico para mantener datos más frescos
    if is_peak_hour:
        return self.settings["PEAK_TTL"]
    else:
        return self.settings["DEFAULT_TTL"]

def _is_peak_hour(self, hour: int) -> bool:
    """Determina si una hora es considerada hora pico.

    Args:
        hour: Hora del día (0-23)

    Returns:
        True si es hora pico, False en caso contrario
    """
    # Analizar estadísticas de acceso para determinar horas pico
    if not self.hourly_access_stats:
        # Si no hay estadísticas, usar horas de oficina como aproximación
        return 9 <= hour <= 18

    # Calcular uso promedio para la hora especificada
    hour_stats = [stat for stat in self.hourly_access_stats if stat["hour"] == hour]
    if not hour_stats:
        return False

    avg_usage = sum(stat["count"] for stat in hour_stats) / len(hour_stats)
    return avg_usage > self.settings["USAGE_THRESHOLD"]

def _record_access(self, key: str) -> None:
    """Registra un acceso a la caché para análisis de patrones.

    Args:
        key: Clave accedida
    """
    current_hour = datetime.now().hour

    # Actualizar estadísticas de la hora actual
    hour_stat = next((stat for stat in self.hourly_access_stats if stat["hour"] == current_hour), None)
    if hour_stat:
        hour_stat["count"] += 1
        hour_stat["keys"].add(key)
    else:
        self.hourly_access_stats.append({
            "hour": current_hour,
            "count": 1,
            "keys": {key},
            "date": datetime.now().date()
        })

    # Limpiar estadísticas antiguas (más de 7 días)
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    self.hourly_access_stats = [
        stat for stat in self.hourly_access_stats
        if stat["date"] >= seven_days_ago
    ]
```

#### Monitoreo y Métricas

```python
async def get_metrics(self) -> CacheMetrics:
    """Obtiene métricas de rendimiento de la caché.

    Returns:
        Objeto CacheMetrics con estadísticas de la caché
    """
    metrics = await get_cache_metrics()
    return CacheMetrics(
        hit_count=metrics["hit_count"],
        miss_count=metrics["miss_count"],
        hit_rate=metrics["hit_rate"],
        memory_usage_bytes=metrics["memory_usage_bytes"],
        keys_count=metrics["keys_count"],
        last_sync=metrics["last_sync"]
    )

async def clear(self, pattern: str = "*") -> int:
    """Limpia la caché según un patrón.

    Args:
        pattern: Patrón de claves a eliminar (por defecto: "*" para todas)

    Returns:
        Número de claves eliminadas
    """
    return await clear_cache(pattern)
```

## Configuración

El servicio de caché se configura a través de variables de entorno:

```env
# Redis Configuration
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=your-redis-password
REDIS_CACHE_TTL=3600
REDIS_MAX_CONNECTIONS=10
REDIS_POOL_TIMEOUT=30
REDIS_SYNC_INTERVAL=300
```

## Uso

### Inicialización

```python
# En app/main.py
from app.services.cache_service import CacheService

cache_service = CacheService()

@app.on_event("startup")
async def startup_event():
    # Iniciar sincronización de caché
    await cache_service.start_sync()

@app.on_event("shutdown")
async def shutdown_event():
    # Detener sincronización de caché
    await cache_service.stop_sync()
```

### Uso en Servicios

```python
# En otro servicio
from app.services.cache_service import CacheService

class CampaignService:
    def __init__(self, supabase_client, cache_service: CacheService):
        self.supabase = supabase_client
        self.cache_service = cache_service
        self.cache_prefix = "campaign:"

    async def get_campaign(self, campaign_id: str) -> Campaign:
        # Intentar obtener de caché primero
        cache_key = f"{self.cache_prefix}{campaign_id}"
        cached_data = await self.cache_service.get(cache_key)

        if cached_data:
            return Campaign(**cached_data)

        # Si no está en caché, obtener de base de datos
        result = self.supabase.from_table("campaigns").select("*").eq("id", campaign_id).execute()

        if not result.data:
            raise HTTPException(status_code=404, detail="Campaign not found")

        campaign = Campaign(**result.data[0])

        # Almacenar en caché para futuras consultas
        await self.cache_service.set(cache_key, campaign.dict())

        return campaign
```

## Consideraciones de Rendimiento

- **Tamaño de caché**: Monitorear el uso de memoria de Redis y ajustar según sea necesario
- **TTL**: Configurar TTL adecuados según la frecuencia de cambio de los datos
- **Patrones de invalidación**: Implementar invalidación selectiva en lugar de limpiar toda la caché
- **Compresión**: Considerar la compresión para datos grandes
- **Serialización**: Optimizar la serialización/deserialización para mejorar el rendimiento

## Consideraciones de Seguridad

- **Autenticación**: Configurar Redis con autenticación
- **Cifrado**: Considerar el cifrado para datos sensibles
- **Aislamiento**: Utilizar bases de datos Redis separadas para diferentes entornos
- **Validación**: Validar datos antes de almacenarlos en caché
- **Límites**: Configurar límites de memoria y políticas de evicción

## Solución de Problemas

### Problemas Comunes

1. **Alta tasa de fallos de caché**:
   - Verificar TTL configurado
   - Comprobar patrones de invalidación
   - Analizar patrones de acceso

2. **Uso excesivo de memoria**:
   - Revisar tamaño de datos almacenados
   - Ajustar políticas de evicción
   - Considerar compresión

3. **Latencia alta**:
   - Verificar conexión a Redis
   - Comprobar carga del servidor Redis
   - Optimizar consultas

4. **Errores de sincronización**:
   - Verificar conexión a Supabase
   - Comprobar permisos
   - Revisar logs para errores específicos

### Comandos Útiles

```bash
# Monitorear Redis
redis-cli monitor

# Obtener estadísticas
redis-cli info

# Limpiar caché
redis-cli flushdb

# Ver claves
redis-cli keys "*"
```

## Referencias

- [Redis Documentation](https://redis.io/documentation)
- [FastAPI Caching Strategies](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.io/docs)
