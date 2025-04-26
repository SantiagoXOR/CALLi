# Sistema de Caché Optimizado

Este documento describe la implementación del sistema de caché optimizado para la aplicación de automatización de llamadas.

## Arquitectura de Caché por Niveles

### Nivel 1 (L1): Caché en Memoria
- Implementación basada en diccionario en memoria con política LRU
- Tiempo de acceso: <1ms
- Capacidad configurable (por defecto: 100 elementos)
- TTL configurable (por defecto: 5 minutos)

### Nivel 2 (L2): Redis
- Implementación basada en Redis
- Tiempo de acceso: 1-5ms
- Compresión adaptativa para datos grandes
- TTL configurable (por defecto: 1 hora)

### Nivel 3 (Persistencia): Supabase
- Almacenamiento persistente en Supabase
- Sincronización asíncrona desde Redis
- Batch updates para optimizar rendimiento

## Estrategias de Optimización

### Compresión Adaptativa
- Umbral configurable (por defecto: 1KB)
- Algoritmo: zlib
- Monitoreo de ratio de compresión

### Precarga Predictiva
- API para precargar conversaciones específicas
- Implementación mediante endpoint `/cache/preload/{conversation_id}`

### Sincronización Asíncrona
- Intervalo configurable (por defecto: 5 minutos)
- Procesamiento por lotes (batch size configurable)
- Sincronización forzada mediante API

## Recuperación ante Fallos

### Circuit Breaker Pattern
- Estados: CLOSED, OPEN, HALF_OPEN
- Umbral configurable de fallos consecutivos
- Timeout configurable para reintentos

### Fallback Automático
- Redirección automática a Supabase cuando Redis falla
- Reconexión inteligente con periodo de prueba

## Monitoreo y Métricas

### Métricas Disponibles
- Hit/Miss ratio
- Latencia de acceso
- Ratio de compresión
- Uso de memoria
- Frecuencia de sincronización

### API de Monitoreo
- Endpoint: `/cache/metrics`
- Formato: JSON

## Configuración

### Variables de Entorno
```
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=
REDIS_CACHE_TTL=3600
REDIS_L1_CACHE_SIZE=100
REDIS_L1_CACHE_TTL=300
SYNC_BATCH_SIZE=10
SYNC_INTERVAL=300
```

## Gestión de Recursos

### Políticas de Evicción
- L1: LRU (Least Recently Used)
- L2: Redis con TTL

### Límites de Memoria
- L1: Configurable por número de elementos
- L2: Configurable en Redis

## Seguridad

- Autenticación Redis configurable
- Datos comprimidos para mayor seguridad
- Aislamiento de datos por conversación