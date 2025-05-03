# Configuración de Alertas

## Visión General

El sistema de automatización de llamadas implementa un robusto sistema de alertas que permite detectar problemas y anomalías en tiempo real. Este documento describe la arquitectura del sistema de alertas, los tipos de alertas configurados, los canales de notificación y las mejores prácticas para la gestión de alertas.

## Arquitectura del Sistema de Alertas

El sistema de alertas se compone de los siguientes componentes:

1. **Recopilación de Métricas**: Instrumentación del código para recopilar métricas en tiempo real
2. **Definición de Reglas**: Reglas de alertas basadas en expresiones de Prometheus
3. **Evaluación de Alertas**: Evaluación continua de reglas por Prometheus
4. **Gestión de Alertas**: AlertManager para deduplicación, agrupación y enrutamiento
5. **Notificación**: Envío de alertas a través de diversos canales (email, Slack, etc.)
6. **Silenciamiento**: Mecanismos para silenciar alertas durante mantenimientos

### Diagrama de Arquitectura

```mermaid
graph TD
    A[Aplicación] -->|Instrumentación| B[Métricas]
    B -->|Exposición| C[Endpoint Prometheus]
    C -->|Scraping| D[Prometheus]
    D -->|Evaluación| E[Reglas de Alertas]
    E -->|Alertas| F[AlertManager]
    F -->|Deduplicación| G[Procesamiento]
    G -->|Agrupación| H[Enrutamiento]
    H -->|Notificación| I[Canales]
    I -->|Email| J[Email]
    I -->|Slack| K[Slack]
    I -->|Webhook| L[Webhook]
```

## Servicio de Alertas

El sistema implementa un `AlertService` que proporciona una interfaz programática para la gestión de alertas:

```python
class AlertService:
    """Servicio para gestionar alertas del sistema."""

    def __init__(self):
        """Inicializa el servicio de alertas."""
        self.alerts_history = []
        self.settings = {
            "MAX_LATENCY_MS": 5000,  # Latencia máxima en ms
            "MIN_AUDIO_QUALITY": 0.7,  # Calidad mínima de audio
            "MAX_ERROR_RATE": 0.05,  # Tasa máxima de error (5%)
            "ALERT_RETENTION_DAYS": 7,  # Días de retención de alertas
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
```

## Tipos de Alertas

El sistema define varios tipos de alertas basadas en diferentes métricas y umbrales:

### 1. Alertas de Rendimiento

#### Alta Latencia de Llamadas

```yaml
alert: HighCallLatency
expr: histogram_quantile(0.95, sum(rate(call_latency_seconds_bucket[5m])) by (le)) > 10
for: 5m
labels:
  severity: warning
  category: performance
annotations:
  summary: "Alta latencia en llamadas"
  description: "El percentil 95 de latencia de llamadas es {{ $value }} segundos, superando el umbral de 10 segundos"
  dashboard: "https://grafana.example.com/d/calls/call-performance"
```

#### Tiempo de Respuesta de IA Elevado

```yaml
alert: HighAIResponseTime
expr: histogram_quantile(0.95, sum(rate(ai_response_time_seconds_bucket[5m])) by (le)) > 3
for: 5m
labels:
  severity: warning
  category: performance
annotations:
  summary: "Tiempo de respuesta de IA elevado"
  description: "El percentil 95 de tiempo de respuesta de IA es {{ $value }} segundos, superando el umbral de 3 segundos"
  dashboard: "https://grafana.example.com/d/ai/ai-performance"
```

### 2. Alertas de Calidad

#### Baja Calidad de Audio

```yaml
alert: LowAudioQuality
expr: avg(audio_quality_score) < 0.7
for: 5m
labels:
  severity: warning
  category: quality
annotations:
  summary: "Baja calidad de audio"
  description: "La calidad promedio del audio es {{ $value }}, por debajo del umbral de 0.7"
  dashboard: "https://grafana.example.com/d/audio/audio-quality"
```

#### Sentimiento Negativo en Conversaciones

```yaml
alert: NegativeSentiment
expr: avg(ai_sentiment_score) < -0.3
for: 10m
labels:
  severity: warning
  category: quality
annotations:
  summary: "Sentimiento negativo en conversaciones"
  description: "El sentimiento promedio es {{ $value }}, indicando conversaciones negativas"
  dashboard: "https://grafana.example.com/d/sentiment/conversation-sentiment"
```

### 3. Alertas de Errores

#### Alta Tasa de Error en Llamadas

```yaml
alert: HighCallErrorRate
expr: sum(rate(total_calls{status="failed"}[5m])) / sum(rate(total_calls[5m])) > 0.05
for: 5m
labels:
  severity: critical
  category: errors
annotations:
  summary: "Alta tasa de error en llamadas"
  description: "La tasa de error es {{ $value | humanizePercentage }}, superando el umbral del 5%"
  dashboard: "https://grafana.example.com/d/errors/error-rates"
```

#### Errores de ElevenLabs

```yaml
alert: ElevenLabsErrors
expr: sum(rate(elevenlabs_errors_total[5m])) > 1
for: 5m
labels:
  severity: warning
  category: errors
annotations:
  summary: "Errores en la API de ElevenLabs"
  description: "Se están produciendo {{ $value }} errores por minuto en la API de ElevenLabs"
  dashboard: "https://grafana.example.com/d/integrations/elevenlabs-integration"
```

### 4. Alertas de Recursos

#### Alto Uso de CPU

```yaml
alert: HighCPUUsage
expr: rate(process_cpu_seconds_total[1m]) > 0.8
for: 5m
labels:
  severity: warning
  category: resources
annotations:
  summary: "Alto uso de CPU"
  description: "El uso de CPU es {{ $value | humanizePercentage }}, superando el umbral del 80%"
  dashboard: "https://grafana.example.com/d/system/system-resources"
```

#### Alto Uso de Memoria

```yaml
alert: HighMemoryUsage
expr: process_resident_memory_bytes / 1024 / 1024 / 1024 > 2
for: 10m
labels:
  severity: warning
  category: resources
annotations:
  summary: "Alto uso de memoria"
  description: "El uso de memoria es {{ $value | humanize }}GB, superando el umbral de 2GB"
  dashboard: "https://grafana.example.com/d/system/system-resources"
```

### 5. Alertas de Disponibilidad

#### Servicio Caído

```yaml
alert: ServiceDown
expr: up{job="call-automation"} == 0
for: 1m
labels:
  severity: critical
  category: availability
annotations:
  summary: "Servicio caído"
  description: "El servicio call-automation está caído"
  dashboard: "https://grafana.example.com/d/system/system-overview"
```

#### Endpoint Inaccesible

```yaml
alert: EndpointDown
expr: probe_success{job="call-automation-blackbox"} == 0
for: 2m
labels:
  severity: critical
  category: availability
annotations:
  summary: "Endpoint inaccesible"
  description: "El endpoint {{ $labels.instance }} está inaccesible"
  dashboard: "https://grafana.example.com/d/system/system-overview"
```

## Niveles de Severidad

El sistema define los siguientes niveles de severidad para las alertas:

| Nivel | Descripción | Tiempo de Respuesta | Notificación |
|-------|-------------|---------------------|--------------|
| **critical** | Problemas que requieren atención inmediata | < 15 minutos | Email, SMS, Slack, PagerDuty |
| **warning** | Problemas que requieren atención pronto | < 4 horas | Email, Slack |
| **info** | Información que no requiere acción inmediata | N/A | Slack (canal específico) |

## Canales de Notificación

### Email

Configuración para notificaciones por email:

```yaml
receivers:
- name: 'email'
  email_configs:
  - to: 'alerts@example.com'
    from: 'alertmanager@example.com'
    smarthost: 'smtp.example.com:587'
    auth_username: 'alertmanager'
    auth_password: 'password'
    send_resolved: true
```

### Slack

Configuración para notificaciones por Slack:

```yaml
receivers:
- name: 'slack'
  slack_configs:
  - api_url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
    channel: '#alerts'
    send_resolved: true
    title: '{{ template "slack.default.title" . }}'
    text: '{{ template "slack.default.text" . }}'
```

### PagerDuty

Configuración para notificaciones por PagerDuty:

```yaml
receivers:
- name: 'pagerduty'
  pagerduty_configs:
  - service_key: '1234567890abcdef1234567890abcdef'
    send_resolved: true
    description: '{{ template "pagerduty.default.description" . }}'
    details:
      severity: '{{ .CommonLabels.severity }}'
      summary: '{{ .CommonAnnotations.summary }}'
      description: '{{ .CommonAnnotations.description }}'
```

## Enrutamiento de Alertas

Configuración de enrutamiento basada en severidad y categoría:

```yaml
route:
  receiver: 'default'
  group_by: ['alertname', 'category']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
  - match:
      severity: critical
    receiver: 'pagerduty'
    continue: true
  - match:
      severity: critical
    receiver: 'slack-critical'
    continue: true
  - match:
      severity: warning
    receiver: 'slack-warnings'
    continue: true
  - match_re:
      category: availability|errors
    receiver: 'email'
```

## Silenciamiento de Alertas

Durante mantenimientos programados o cuando se están investigando problemas conocidos, se pueden silenciar alertas para evitar ruido innecesario:

```yaml
# Silenciar todas las alertas durante un mantenimiento
- matchers:
  - name: instance
    value: app-server-01
  startsAt: "2023-06-01T10:00:00Z"
  endsAt: "2023-06-01T12:00:00Z"
  createdBy: "admin"
  comment: "Mantenimiento programado"

# Silenciar alertas específicas
- matchers:
  - name: alertname
    value: HighMemoryUsage
  startsAt: "2023-06-01T00:00:00Z"
  endsAt: "2023-06-02T00:00:00Z"
  createdBy: "admin"
  comment: "Problema conocido, en investigación"
```

## Implementación Programática

Ejemplo de cómo utilizar el `AlertService` para verificar umbrales y enviar alertas:

```python
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

    if metrics.get("audio_quality", 1.0) < self.settings["MIN_AUDIO_QUALITY"]:
        await self.send_alert(
            level="warning",
            message=f"Baja calidad de audio: {metrics['audio_quality']}",
            context=metrics,
        )
```

## Plantillas de Notificación

Personalización de plantillas para diferentes canales:

### Plantilla de Slack

```
{{ define "slack.default.title" -}}
  [{{ .Status | toUpper }}{{ if eq .Status "firing" }}:{{ .Alerts.Firing | len }}{{ end }}] {{ .CommonLabels.alertname }}
{{- end }}

{{ define "slack.default.text" -}}
  {{ range .Alerts }}
    *Alerta:* {{ .Annotations.summary }}
    *Descripción:* {{ .Annotations.description }}
    *Severidad:* {{ .Labels.severity }}
    *Inicio:* {{ .StartsAt | since }}
    {{ if .Annotations.dashboard }}*Dashboard:* {{ .Annotations.dashboard }}{{ end }}
    {{ if .Annotations.runbook }}*Runbook:* {{ .Annotations.runbook }}{{ end }}
  {{ end }}
{{- end }}
```

### Plantilla de Email

```
{{ define "email.subject" -}}
  [{{ .Status | toUpper }}] {{ .CommonLabels.alertname }}
{{- end }}

{{ define "email.html" -}}
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial, sans-serif; }
    .alert { margin-bottom: 20px; padding: 15px; border-radius: 4px; }
    .critical { background-color: #f8d7da; border: 1px solid #f5c6cb; }
    .warning { background-color: #fff3cd; border: 1px solid #ffeeba; }
    .info { background-color: #d1ecf1; border: 1px solid #bee5eb; }
  </style>
</head>
<body>
  <h2>{{ .CommonLabels.alertname }}</h2>
  <p>Estado: {{ .Status | toUpper }}</p>

  {{ range .Alerts }}
  <div class="alert {{ .Labels.severity }}">
    <h3>{{ .Annotations.summary }}</h3>
    <p>{{ .Annotations.description }}</p>
    <p><strong>Severidad:</strong> {{ .Labels.severity }}</p>
    <p><strong>Inicio:</strong> {{ .StartsAt }}</p>
    {{ if .Annotations.dashboard }}<p><strong>Dashboard:</strong> <a href="{{ .Annotations.dashboard }}">Ver dashboard</a></p>{{ end }}
    {{ if .Annotations.runbook }}<p><strong>Runbook:</strong> <a href="{{ .Annotations.runbook }}">Ver runbook</a></p>{{ end }}
  </div>
  {{ end }}
</body>
</html>
{{- end }}
```

## Gestión de Incidentes

Cuando se dispara una alerta crítica, se debe seguir el siguiente proceso de gestión de incidentes:

1. **Reconocimiento**: Reconocer la alerta en el sistema
2. **Investigación**: Investigar la causa raíz del problema
3. **Mitigación**: Implementar medidas para mitigar el impacto
4. **Resolución**: Resolver el problema
5. **Postmortem**: Realizar un análisis postmortem para evitar recurrencias

### Ejemplo de Runbook para Alta Tasa de Error

```markdown
# Runbook: Alta Tasa de Error en Llamadas

## Descripción
Esta alerta se dispara cuando la tasa de error en llamadas supera el 5% durante 5 minutos.

## Pasos de Investigación
1. Verificar logs de errores en Kibana
2. Comprobar estado de servicios externos (Twilio, ElevenLabs)
3. Verificar métricas de recursos (CPU, memoria)
4. Comprobar cambios recientes en el código

## Pasos de Mitigación
1. Si es un problema con un servicio externo, activar el modo de fallback
2. Si es un problema de recursos, escalar horizontalmente
3. Si es un problema de código, revertir el último despliegue

## Contactos
- Equipo de Guardia: +1-234-567-8900
- Responsable de Twilio: alice@example.com
- Responsable de ElevenLabs: bob@example.com
```

## Mejores Prácticas

1. **Reducir el Ruido**: Configurar umbrales adecuados para evitar falsos positivos
2. **Agrupar Alertas**: Agrupar alertas relacionadas para reducir la fatiga de alertas
3. **Priorizar por Severidad**: Establecer niveles de severidad claros y responder según la prioridad
4. **Documentar Runbooks**: Crear runbooks para cada tipo de alerta
5. **Revisar Regularmente**: Revisar y ajustar las alertas periódicamente
6. **Pruebas de Alertas**: Probar el sistema de alertas regularmente
7. **Métricas de Alertas**: Monitorear la efectividad del sistema de alertas (falsos positivos, tiempo de respuesta, etc.)
8. **Rotación de Guardia**: Establecer un sistema de rotación para evitar la fatiga

## Configuración de AlertManager

Ejemplo completo de configuración de AlertManager:

```yaml
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.example.com:587'
  smtp_from: 'alertmanager@example.com'
  smtp_auth_username: 'alertmanager'
  smtp_auth_password: 'password'
  slack_api_url: 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  receiver: 'default'
  group_by: ['alertname', 'category']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
  - match:
      severity: critical
    receiver: 'pagerduty'
    continue: true
  - match:
      severity: critical
    receiver: 'slack-critical'
    continue: true
  - match:
      severity: warning
    receiver: 'slack-warnings'
    continue: true
  - match_re:
      category: availability|errors
    receiver: 'email'

receivers:
- name: 'default'
  slack_configs:
  - channel: '#alerts'
    send_resolved: true
    title: '{{ template "slack.default.title" . }}'
    text: '{{ template "slack.default.text" . }}'

- name: 'slack-critical'
  slack_configs:
  - channel: '#alerts-critical'
    send_resolved: true
    title: '{{ template "slack.default.title" . }}'
    text: '{{ template "slack.default.text" . }}'

- name: 'slack-warnings'
  slack_configs:
  - channel: '#alerts-warnings'
    send_resolved: true
    title: '{{ template "slack.default.title" . }}'
    text: '{{ template "slack.default.text" . }}'

- name: 'email'
  email_configs:
  - to: 'alerts@example.com'
    send_resolved: true
    html: '{{ template "email.html" . }}'
    headers:
      Subject: '{{ template "email.subject" . }}'

- name: 'pagerduty'
  pagerduty_configs:
  - service_key: '1234567890abcdef1234567890abcdef'
    send_resolved: true
    description: '{{ template "pagerduty.default.description" . }}'
    details:
      severity: '{{ .CommonLabels.severity }}'
      summary: '{{ .CommonAnnotations.summary }}'
      description: '{{ .CommonAnnotations.description }}'

inhibit_rules:
- source_match:
    severity: 'critical'
  target_match:
    severity: 'warning'
  equal: ['alertname']
```

## Referencias

- [Prometheus Alerting Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [AlertManager Configuration](https://prometheus.io/docs/alerting/latest/configuration/)
- [AlertManager Templates](https://prometheus.io/docs/alerting/latest/notification_examples/)
- [Google SRE Book: Practical Alerting](https://sre.google/sre-book/practical-alerting/)
- [PagerDuty Incident Response](https://response.pagerduty.com/)
