# Referencia de Métricas

## Visión General

Este documento proporciona una referencia detallada de todas las métricas recopiladas por el sistema de automatización de llamadas. Las métricas están organizadas por categoría y se proporciona información sobre su tipo, unidades, etiquetas y uso recomendado.

## Tipos de Métricas

El sistema utiliza cuatro tipos principales de métricas de Prometheus:

1. **Counter**: Valor acumulativo que solo puede aumentar (o reiniciarse a cero)
2. **Gauge**: Valor que puede aumentar o disminuir
3. **Histogram**: Muestras de observaciones y su distribución en buckets configurables
4. **Summary**: Similar a Histogram, pero calcula cuantiles configurables durante un período de tiempo

## Métricas de Llamadas

### call_latency_seconds

**Tipo**: Histogram
**Descripción**: Latencia de las llamadas en segundos
**Unidades**: Segundos
**Etiquetas**:
- `status`: Estado de la llamada (completed, failed, etc.)

**Buckets**: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0, 120.0]

**Uso**:
- Monitorear la latencia de las llamadas
- Identificar llamadas lentas
- Establecer SLOs de rendimiento

**Consultas de ejemplo**:
```
# Latencia promedio de llamadas
rate(call_latency_seconds_sum[5m]) / rate(call_latency_seconds_count[5m])

# Percentil 95 de latencia
histogram_quantile(0.95, sum(rate(call_latency_seconds_bucket[5m])) by (le))
```

### audio_quality_score

**Tipo**: Gauge
**Descripción**: Puntuación de calidad del audio
**Unidades**: Puntuación (0-1)
**Etiquetas**:
- `voice`: ID de la voz utilizada

**Uso**:
- Monitorear la calidad del audio generado
- Identificar problemas de calidad
- Comparar diferentes voces

**Consultas de ejemplo**:
```
# Calidad de audio promedio
avg(audio_quality_score)

# Calidad de audio por voz
avg(audio_quality_score) by (voice)
```

### total_calls

**Tipo**: Counter
**Descripción**: Número total de llamadas realizadas
**Unidades**: Llamadas
**Etiquetas**:
- `status`: Estado de la llamada (completed, failed, etc.)
- `campaign_id`: ID de la campaña

**Uso**:
- Monitorear el volumen de llamadas
- Calcular tasas de éxito/fallo
- Analizar tendencias de uso

**Consultas de ejemplo**:
```
# Tasa de llamadas por minuto
rate(total_calls[1m])

# Tasa de llamadas por campaña
sum(rate(total_calls[5m])) by (campaign_id)

# Tasa de éxito
sum(rate(total_calls{status="completed"}[5m])) / sum(rate(total_calls[5m]))
```

### call_duration_seconds

**Tipo**: Histogram
**Descripción**: Duración de las llamadas en segundos
**Unidades**: Segundos
**Etiquetas**:
- `campaign_id`: ID de la campaña

**Buckets**: [10, 30, 60, 120, 300, 600, 1200, 1800]

**Uso**:
- Analizar la duración de las llamadas
- Identificar llamadas anormalmente largas o cortas
- Optimizar scripts de llamadas

**Consultas de ejemplo**:
```
# Duración promedio de llamadas
rate(call_duration_seconds_sum[5m]) / rate(call_duration_seconds_count[5m])

# Percentil 95 de duración
histogram_quantile(0.95, sum(rate(call_duration_seconds_bucket[5m])) by (le))
```

## Métricas de IA

### ai_response_time_seconds

**Tipo**: Histogram
**Descripción**: Tiempo de respuesta de la IA en segundos
**Unidades**: Segundos
**Etiquetas**:
- `model`: Modelo de IA utilizado

**Buckets**: [0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0]

**Uso**:
- Monitorear el rendimiento de la IA
- Identificar respuestas lentas
- Comparar diferentes modelos

**Consultas de ejemplo**:
```
# Tiempo de respuesta promedio
rate(ai_response_time_seconds_sum[5m]) / rate(ai_response_time_seconds_count[5m])

# Percentil 95 por modelo
histogram_quantile(0.95, sum(rate(ai_response_time_seconds_bucket[5m])) by (le, model))
```

### ai_requests_total

**Tipo**: Counter
**Descripción**: Número total de solicitudes a la IA
**Unidades**: Solicitudes
**Etiquetas**:
- `model`: Modelo de IA utilizado
- `status`: Estado de la solicitud (success, error)

**Uso**:
- Monitorear el volumen de solicitudes a la IA
- Calcular tasas de error
- Analizar uso por modelo

**Consultas de ejemplo**:
```
# Tasa de solicitudes por minuto
rate(ai_requests_total[1m])

# Tasa de error
sum(rate(ai_requests_total{status="error"}[5m])) / sum(rate(ai_requests_total[5m]))
```

### ai_errors_total

**Tipo**: Counter
**Descripción**: Número total de errores de la IA
**Unidades**: Errores
**Etiquetas**:
- `model`: Modelo de IA utilizado
- `error_type`: Tipo de error

**Uso**:
- Monitorear errores de la IA
- Identificar tipos de errores comunes
- Alertar sobre tasas de error elevadas

**Consultas de ejemplo**:
```
# Tasa de errores por minuto
rate(ai_errors_total[1m])

# Errores por tipo
sum(rate(ai_errors_total[5m])) by (error_type)
```

### ai_sentiment_score

**Tipo**: Gauge
**Descripción**: Puntuación de sentimiento detectado por la IA
**Unidades**: Puntuación (-1 a 1)
**Etiquetas**:
- `campaign_id`: ID de la campaña

**Uso**:
- Monitorear el sentimiento de las conversaciones
- Identificar campañas con sentimiento negativo
- Analizar tendencias de sentimiento

**Consultas de ejemplo**:
```
# Sentimiento promedio
avg(ai_sentiment_score)

# Sentimiento por campaña
avg(ai_sentiment_score) by (campaign_id)
```

### ai_tokens_used

**Tipo**: Summary
**Descripción**: Número de tokens utilizados en solicitudes de IA
**Unidades**: Tokens
**Etiquetas**:
- `model`: Modelo de IA utilizado

**Uso**:
- Monitorear el uso de tokens
- Estimar costos
- Optimizar prompts

**Consultas de ejemplo**:
```
# Tokens promedio por solicitud
rate(ai_tokens_used_sum[5m]) / rate(ai_tokens_used_count[5m])

# Total de tokens por modelo
sum(rate(ai_tokens_used_sum[1h])) by (model)
```

## Métricas de ElevenLabs

### elevenlabs_requests_total

**Tipo**: Counter
**Descripción**: Número total de solicitudes a ElevenLabs
**Unidades**: Solicitudes
**Etiquetas**:
- `method`: Método de la API llamado
- `status`: Estado de la solicitud (success, error)

**Uso**:
- Monitorear el volumen de solicitudes a ElevenLabs
- Calcular tasas de error
- Analizar uso por método

**Consultas de ejemplo**:
```
# Tasa de solicitudes por minuto
rate(elevenlabs_requests_total[1m])

# Tasa de error
sum(rate(elevenlabs_requests_total{status="error"}[5m])) / sum(rate(elevenlabs_requests_total[5m]))
```

### elevenlabs_request_duration_seconds

**Tipo**: Histogram
**Descripción**: Latencia de solicitudes a ElevenLabs
**Unidades**: Segundos
**Etiquetas**:
- `method`: Método de la API llamado

**Buckets**: [0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]

**Uso**:
- Monitorear la latencia de las solicitudes a ElevenLabs
- Identificar métodos lentos
- Establecer SLOs de rendimiento

**Consultas de ejemplo**:
```
# Latencia promedio
rate(elevenlabs_request_duration_seconds_sum[5m]) / rate(elevenlabs_request_duration_seconds_count[5m])

# Percentil 95 por método
histogram_quantile(0.95, sum(rate(elevenlabs_request_duration_seconds_bucket[5m])) by (le, method))
```

### elevenlabs_pool_connections_active

**Tipo**: Gauge
**Descripción**: Número de conexiones activas en el pool
**Unidades**: Conexiones

**Uso**:
- Monitorear el uso del pool de conexiones
- Identificar posibles fugas de conexiones
- Optimizar el tamaño del pool

**Consultas de ejemplo**:
```
# Conexiones activas
elevenlabs_pool_connections_active

# Porcentaje de uso del pool
elevenlabs_pool_connections_active / elevenlabs_pool_size * 100
```

### elevenlabs_pool_size

**Tipo**: Gauge
**Descripción**: Tamaño configurado del pool de conexiones
**Unidades**: Conexiones

**Uso**:
- Referencia para el tamaño máximo del pool
- Calcular porcentaje de uso

**Consultas de ejemplo**:
```
# Tamaño del pool
elevenlabs_pool_size
```

### elevenlabs_errors_total

**Tipo**: Counter
**Descripción**: Número total de errores específicos
**Unidades**: Errores
**Etiquetas**:
- `error_type`: Tipo de error

**Uso**:
- Monitorear errores de ElevenLabs
- Identificar tipos de errores comunes
- Alertar sobre tasas de error elevadas

**Consultas de ejemplo**:
```
# Tasa de errores por minuto
rate(elevenlabs_errors_total[1m])

# Errores por tipo
sum(rate(elevenlabs_errors_total[5m])) by (error_type)
```

### elevenlabs_generation_duration_seconds

**Tipo**: Histogram
**Descripción**: Duración de la generación de audio
**Unidades**: Segundos
**Etiquetas**:
- `voice`: Voz utilizada

**Buckets**: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]

**Uso**:
- Monitorear el tiempo de generación de audio
- Comparar rendimiento entre voces
- Identificar generaciones lentas

**Consultas de ejemplo**:
```
# Tiempo promedio de generación
rate(elevenlabs_generation_duration_seconds_sum[5m]) / rate(elevenlabs_generation_duration_seconds_count[5m])

# Tiempo promedio por voz
sum(rate(elevenlabs_generation_duration_seconds_sum[5m])) by (voice) / sum(rate(elevenlabs_generation_duration_seconds_count[5m])) by (voice)
```

### elevenlabs_audio_quality_score

**Tipo**: Histogram
**Descripción**: Calidad del audio generado
**Unidades**: Puntuación (0-1)

**Buckets**: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

**Uso**:
- Monitorear la calidad del audio generado
- Identificar problemas de calidad
- Establecer umbrales de calidad mínima

**Consultas de ejemplo**:
```
# Calidad promedio
rate(elevenlabs_audio_quality_score_sum[5m]) / rate(elevenlabs_audio_quality_score_count[5m])

# Porcentaje de audio con calidad < 0.7
sum(rate(elevenlabs_audio_quality_score_bucket{le="0.7"}[5m])) / sum(rate(elevenlabs_audio_quality_score_count[5m]))
```

## Métricas del Sistema

### http_requests_total

**Tipo**: Counter
**Descripción**: Número total de solicitudes HTTP
**Unidades**: Solicitudes
**Etiquetas**:
- `method`: Método HTTP (GET, POST, etc.)
- `path`: Ruta de la solicitud
- `status`: Código de estado HTTP

**Uso**:
- Monitorear el tráfico de la API
- Calcular tasas de error
- Identificar endpoints populares

**Consultas de ejemplo**:
```
# Tasa de solicitudes por minuto
rate(http_requests_total[1m])

# Tasa de error HTTP
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# Top 5 endpoints por tráfico
topk(5, sum(rate(http_requests_total[5m])) by (path))
```

### http_request_duration_seconds

**Tipo**: Histogram
**Descripción**: Duración de las solicitudes HTTP
**Unidades**: Segundos
**Etiquetas**:
- `method`: Método HTTP
- `path`: Ruta de la solicitud

**Buckets**: [0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]

**Uso**:
- Monitorear la latencia de la API
- Identificar endpoints lentos
- Establecer SLOs de rendimiento

**Consultas de ejemplo**:
```
# Latencia promedio
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Percentil 95 por endpoint
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path))

# Endpoints más lentos (p95)
topk(5, histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, path)))
```

### process_cpu_seconds_total

**Tipo**: Counter
**Descripción**: Tiempo total de CPU utilizado
**Unidades**: Segundos

**Uso**:
- Monitorear el uso de CPU
- Identificar picos de uso
- Planificar capacidad

**Consultas de ejemplo**:
```
# Uso de CPU por segundo
rate(process_cpu_seconds_total[1m])
```

### process_resident_memory_bytes

**Tipo**: Gauge
**Descripción**: Memoria residente utilizada
**Unidades**: Bytes

**Uso**:
- Monitorear el uso de memoria
- Identificar fugas de memoria
- Planificar capacidad

**Consultas de ejemplo**:
```
# Uso de memoria en MB
process_resident_memory_bytes / 1024 / 1024

# Tendencia de uso de memoria
rate(process_resident_memory_bytes[1h])
```

## Métricas de Caché

### cache_hits_total

**Tipo**: Counter
**Descripción**: Número total de aciertos de caché
**Unidades**: Aciertos
**Etiquetas**:
- `cache`: Tipo de caché (redis, memory, etc.)

**Uso**:
- Monitorear la efectividad de la caché
- Calcular tasa de aciertos
- Optimizar estrategias de caché

**Consultas de ejemplo**:
```
# Tasa de aciertos por minuto
rate(cache_hits_total[1m])

# Tasa de aciertos por tipo de caché
sum(rate(cache_hits_total[5m])) by (cache)
```

### cache_misses_total

**Tipo**: Counter
**Descripción**: Número total de fallos de caché
**Unidades**: Fallos
**Etiquetas**:
- `cache`: Tipo de caché (redis, memory, etc.)

**Uso**:
- Monitorear fallos de caché
- Calcular tasa de fallos
- Identificar oportunidades de mejora

**Consultas de ejemplo**:
```
# Tasa de fallos por minuto
rate(cache_misses_total[1m])

# Ratio de aciertos/fallos
sum(rate(cache_hits_total[5m])) / (sum(rate(cache_hits_total[5m])) + sum(rate(cache_misses_total[5m])))
```

### cache_size_bytes

**Tipo**: Gauge
**Descripción**: Tamaño de la caché en bytes
**Unidades**: Bytes
**Etiquetas**:
- `cache`: Tipo de caché (redis, memory, etc.)

**Uso**:
- Monitorear el uso de memoria de la caché
- Planificar capacidad
- Optimizar tamaño de caché

**Consultas de ejemplo**:
```
# Tamaño de caché en MB
cache_size_bytes / 1024 / 1024

# Tamaño por tipo de caché
sum(cache_size_bytes) by (cache) / 1024 / 1024
```

## Configuración de Alertas

A continuación se presentan ejemplos de reglas de alertas basadas en las métricas descritas:

### Latencia de Llamadas

```yaml
alert: HighCallLatency
expr: histogram_quantile(0.95, sum(rate(call_latency_seconds_bucket[5m])) by (le)) > 10
for: 5m
labels:
  severity: warning
annotations:
  summary: "Alta latencia en llamadas"
  description: "El percentil 95 de latencia de llamadas es {{ $value }} segundos, superando el umbral de 10 segundos"
```

### Calidad de Audio

```yaml
alert: LowAudioQuality
expr: avg(audio_quality_score) < 0.7
for: 5m
labels:
  severity: warning
annotations:
  summary: "Baja calidad de audio"
  description: "La calidad promedio del audio es {{ $value }}, por debajo del umbral de 0.7"
```

### Tasa de Error

```yaml
alert: HighErrorRate
expr: sum(rate(total_calls{status="failed"}[5m])) / sum(rate(total_calls[5m])) > 0.05
for: 5m
labels:
  severity: critical
annotations:
  summary: "Alta tasa de error en llamadas"
  description: "La tasa de error es {{ $value | humanizePercentage }}, superando el umbral del 5%"
```

### Uso de Memoria

```yaml
alert: HighMemoryUsage
expr: process_resident_memory_bytes / 1024 / 1024 / 1024 > 2
for: 10m
labels:
  severity: warning
annotations:
  summary: "Alto uso de memoria"
  description: "El uso de memoria es {{ $value | humanize }}GB, superando el umbral de 2GB"
```

## Integración con Grafana

### Variables de Dashboard

Para crear dashboards dinámicos en Grafana, se recomienda utilizar las siguientes variables:

- `$campaign`: Filtrar por ID de campaña
- `$status`: Filtrar por estado de llamada
- `$interval`: Intervalo de tiempo para agregaciones (1m, 5m, 1h)
- `$percentile`: Percentil para histogramas (0.5, 0.9, 0.95, 0.99)

### Paneles Recomendados

1. **Tasa de Llamadas**:
   ```
   sum(rate(total_calls[$interval])) by (status)
   ```

2. **Latencia de Llamadas (p95)**:
   ```
   histogram_quantile(0.95, sum(rate(call_latency_seconds_bucket[$interval])) by (le))
   ```

3. **Calidad de Audio por Voz**:
   ```
   avg(audio_quality_score) by (voice)
   ```

4. **Tasa de Error por Campaña**:
   ```
   sum(rate(total_calls{status="failed",campaign_id=~"$campaign"}[$interval])) / sum(rate(total_calls{campaign_id=~"$campaign"}[$interval]))
   ```

5. **Uso de Recursos**:
   ```
   # CPU
   rate(process_cpu_seconds_total[$interval])

   # Memoria
   process_resident_memory_bytes / 1024 / 1024
   ```

## Referencias

- [Prometheus Metric Types](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus Query Functions](https://prometheus.io/docs/prometheus/latest/querying/functions/)
- [Grafana Prometheus Data Source](https://grafana.com/docs/grafana/latest/datasources/prometheus/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
