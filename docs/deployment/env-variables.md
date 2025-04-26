# Variables de Entorno

Este documento detalla todas las variables de entorno requeridas para el despliegue del Sistema de Automatización de Llamadas.

## Variables Comunes

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `APP_ENV` | Entorno de la aplicación | Sí | `development` | `production` |
| `APP_DEBUG` | Modo de depuración | No | `false` | `true` |
| `APP_URL` | URL base de la aplicación | Sí | - | `https://call-automation.example.com` |
| `APP_NAME` | Nombre de la aplicación | No | `Call Automation System` | `Mi Sistema de Llamadas` |

## Supabase

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `SUPABASE_URL` | URL de la instancia de Supabase | Sí | `https://abcdefghijklm.supabase.co` |
| `SUPABASE_KEY` | Clave anónima de Supabase | Sí | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `SUPABASE_SERVICE_KEY` | Clave de servicio de Supabase | Sí | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |

## Twilio

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `TWILIO_ACCOUNT_SID` | SID de la cuenta de Twilio | Sí | `your-twilio-account-sid` |
| `TWILIO_AUTH_TOKEN` | Token de autenticación de Twilio | Sí | `your-twilio-auth-token` |
| `TWILIO_PHONE_NUMBER` | Número de teléfono de Twilio | Sí | `+12345678901` |

## Redis

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `REDIS_URL` | URL de conexión a Redis | Sí | - | `redis://redis:6379` |
| `REDIS_PASSWORD` | Contraseña de Redis | No | - | `your-redis-password` |
| `REDIS_CACHE_TTL` | Tiempo de vida del caché (segundos) | No | `3600` | `7200` |
| `REDIS_L1_CACHE_SIZE` | Tamaño del caché L1 | No | `100` | `200` |
| `REDIS_L1_CACHE_TTL` | Tiempo de vida del caché L1 (segundos) | No | `300` | `600` |
| `SYNC_BATCH_SIZE` | Tamaño del lote para sincronización | No | `10` | `20` |
| `SYNC_INTERVAL` | Intervalo de sincronización (segundos) | No | `300` | `600` |

## Base de Datos

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `DATABASE_URL` | URL de conexión a la base de datos | Sí | `postgresql://user:password@host:port/dbname` |

## Seguridad

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `SECRET_KEY` | Clave secreta para tokens JWT | Sí | - | `your-secret-key-at-least-32-chars-long` |
| `ALGORITHM` | Algoritmo para tokens JWT | No | `HS256` | `HS512` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tiempo de expiración de tokens (minutos) | No | `60` | `120` |

## Servidor

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `HOST` | Host del servidor | No | `0.0.0.0` | `127.0.0.1` |
| `PORT` | Puerto del servidor | No | `8000` | `5000` |
| `DEBUG` | Modo de depuración del servidor | No | `false` | `true` |
| `ENVIRONMENT` | Entorno del servidor | No | `development` | `production` |

## ElevenLabs

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `ELEVENLABS_API_KEY` | Clave API de ElevenLabs | Sí | - | `your-elevenlabs-api-key` |
| `ELEVENLABS_DEFAULT_VOICE` | Voz predeterminada de ElevenLabs | No | `Bella` | `Rachel` |
| `ELEVENLABS_MAX_RETRIES` | Número máximo de reintentos | No | `3` | `5` |
| `ELEVENLABS_BACKOFF_FACTOR` | Factor de retroceso para reintentos | No | `2` | `1.5` |
| `ELEVENLABS_MAX_CONNECTIONS` | Máximo de conexiones simultáneas | No | `10` | `20` |
| `ELEVENLABS_POOL_TIMEOUT` | Tiempo de espera del pool (segundos) | No | `30` | `60` |
| `ELEVENLABS_CONNECTION_TIMEOUT` | Tiempo de espera de conexión (segundos) | No | `30` | `60` |

## OpenAI

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `OPENAI_API_KEY` | Clave API de OpenAI | Sí | - | `your-openai-api-key` |
| `DEFAULT_MODEL` | Modelo predeterminado de OpenAI | No | `gpt-4` | `gpt-3.5-turbo` |
| `MAX_TOKENS` | Máximo de tokens por respuesta | No | `150` | `200` |
| `TEMPERATURE` | Temperatura para generación de texto | No | `0.7` | `0.5` |

## Google Gemini (Opcional)

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `GOOGLE_API_KEY` | Clave API de Google | No | `your-google-api-key` |

## Métricas y Logging

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `ENABLE_METRICS` | Habilitar recopilación de métricas | No | `true` | `false` |
| `METRICS_PORT` | Puerto para métricas Prometheus | No | `9090` | `9091` |
| `LOG_LEVEL` | Nivel de logging | No | `info` | `debug` |
| `LOG_FILE` | Archivo de log | No | `logs/app.log` | `/var/log/app.log` |
| `LOG_FORMAT` | Formato de logs | No | `json` | `text` |
| `LOG_ROTATION` | Habilitar rotación de logs | No | `true` | `false` |
| `LOG_RETENTION_DAYS` | Días de retención de logs | No | `30` | `90` |

## Feature Flags

| Variable | Descripción | Requerida | Valor por defecto | Ejemplo |
|----------|-------------|-----------|------------------|---------|
| `ENABLE_ANALYTICS` | Habilitar análisis | No | `false` | `true` |
| `MAINTENANCE_MODE` | Modo de mantenimiento | No | `false` | `true` |

## Variables Específicas del Frontend

| Variable | Descripción | Requerida | Ejemplo |
|----------|-------------|-----------|---------|
| `NEXT_PUBLIC_API_URL` | URL de la API | Sí | `https://api.call-automation.example.com` |
| `NEXT_PUBLIC_SUPABASE_URL` | URL de Supabase para el frontend | Sí | `https://abcdefghijklm.supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Clave anónima de Supabase para el frontend | Sí | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `NEXTAUTH_URL` | URL base para NextAuth | No | `https://call-automation.example.com` |
| `NEXTAUTH_SECRET` | Secreto para NextAuth | No | `your-nextauth-secret` |

## Gestión Segura de Secretos

Para entornos de producción, se recomienda:

1. **No almacenar secretos en archivos .env**: Utilizar servicios de gestión de secretos como AWS Secrets Manager, HashiCorp Vault, o Docker Secrets.

2. **Rotación periódica**: Implementar rotación periódica de secretos, especialmente para tokens de API y contraseñas.

3. **Acceso limitado**: Restringir el acceso a los secretos solo a los servicios que los necesitan.

4. **Encriptación**: Asegurarse de que los secretos estén encriptados en reposo y en tránsito.

## Ejemplo de Configuración para Diferentes Entornos

### Desarrollo

```dotenv
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000
DEBUG=true
ENVIRONMENT=development
```

### Staging

```dotenv
APP_ENV=staging
APP_DEBUG=false
APP_URL=https://staging.call-automation.example.com
DEBUG=false
ENVIRONMENT=staging
```

### Producción

```dotenv
APP_ENV=production
APP_DEBUG=false
APP_URL=https://call-automation.example.com
DEBUG=false
ENVIRONMENT=production
```
