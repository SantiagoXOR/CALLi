# Runbook: Monitoreo y Rollback Integración ElevenLabs

## Resumen
Este documento detalla los procedimientos para monitorear, diagnosticar y ejecutar rollback de la integración con ElevenLabs API.

## Monitoreo

### Métricas Clave (Prometheus)
```
elevenlabs_requests_total{calls}          # Total de requests a la API
elevenlabs_errors_total{calls}            # Errores en requests
elevenlabs_request_duration_seconds       # Latencia de requests
elevenlabs_generation_duration_seconds    # Tiempo de generación de audio
elevenlabs_pool_connections_active        # Conexiones activas
elevenlabs_audio_quality_score            # Calidad de audio (0-1)
```

### Alertas Configuradas
```yaml
# Ver alert_rules.yml para detalles completos
- alert: ElevenLabsHighErrorRate
  expr: rate(elevenlabs_errors_total[5m]) / rate(elevenlabs_requests_total[5m]) > 0.1
  for: 5m

- alert: ElevenLabsHighLatency
  expr: histogram_quantile(0.95, sum(rate(elevenlabs_request_duration_seconds[5m]))) > 3
```

## Diagnóstico

### Problemas Comunes
1. **Errores 429 (Rate Limit)**
   - Verificar métrica `elevenlabs_errors_total{status="429"}`
   - Revisar logs para mensajes "Rate limit exceeded"

2. **Latencia alta**
   - Consultar `elevenlabs_request_duration_seconds`
   - Verificar conexiones activas `elevenlabs_pool_connections_active`

### Herramientas
```
# Consultar logs del servicio
journalctl -u elevenlabs_integration -n 100 --no-pager

# Probar conexión API directamente
curl -X POST https://api.elevenlabs.io/v1/text-to-speech \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -d '{"text": "test"}'
```

## Procedimiento de Rollback

### Criterios para Rollback
- Error rate > 30% por más de 10 minutos
- Latencia > 10s en percentil 95
- Problemas críticos de calidad de audio

### Pasos:

1. **Preparación**
   ```bash
   # Tomar snapshot de configuración
   python scripts/rollback.py --take-snapshot
   ```

2. **Simular Rollback (Dry Run)**
   ```bash
   python scripts/rollback.py --dry-run
   ```

3. **Ejecutar Rollback**
   ```bash
   python scripts/rollback.py
   ```

4. **Verificación**
   - Confirmar métricas reseteadas
   - Verificar logs de ejecución
   - Validar estado del servicio

## Contactos
- Equipo DevOps: devops@example.com
- Soporte ElevenLabs: support@elevenlabs.io

## Historial de Pruebas
| Fecha       | Realizado por | Escenario | Resultado | Observaciones |
|-------------|---------------|-----------|-----------|---------------|
| 2025-03-31 | Equipo DevOps | Rollback completo | Éxito | Todos los componentes se restauraron correctamente |
