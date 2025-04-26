# Requisitos Técnicos para Despliegue de MVP

Este documento detalla los requisitos técnicos necesarios para el despliegue del MVP del Sistema de Automatización de Llamadas.

## Infraestructura

### Requisitos de Servidor

| Componente | Especificación | Notas |
|------------|----------------|-------|
| CPU | 4 vCPUs mínimo | 8 vCPUs recomendado para mejor rendimiento |
| RAM | 8 GB mínimo | 16 GB recomendado para mejor rendimiento |
| Almacenamiento | 50 GB SSD | Considerar expansión según volumen de llamadas |
| Sistema Operativo | Ubuntu 22.04 LTS | Otras distribuciones Linux también son compatibles |
| Ancho de Banda | 100 Mbps mínimo | Para manejar múltiples llamadas simultáneas |

### Servicios en la Nube

| Servicio | Propósito | Tier Recomendado |
|----------|-----------|------------------|
| AWS/GCP/Azure | Hosting de aplicación | Instancia t3.medium (AWS) o equivalente |
| Supabase | Base de datos y autenticación | Plan Pro ($25/mes) |
| Redis | Caché | Instancia dedicada o servicio gestionado |
| Twilio | Telefonía | Plan de pago por uso |
| ElevenLabs | Síntesis de voz | Plan Creator ($22/mes) |
| OpenAI/Google AI | Servicio de IA | GPT-4 o Gemini Pro |

## Requisitos de Software

### Backend

| Componente | Versión | Notas |
|------------|---------|-------|
| Python | 3.9+ | 3.11 recomendado para mejor rendimiento |
| FastAPI | 0.100.0+ | |
| SQLAlchemy | 2.0.0+ | |
| Pydantic | 2.0.0+ | |
| Uvicorn | 0.22.0+ | Servidor ASGI |
| Redis-py | 4.5.0+ | Cliente Redis |
| Twilio SDK | 8.0.0+ | |
| ElevenLabs SDK | Última versión | |
| LangChain | 0.0.267+ | Para integración con IA |

### Frontend

| Componente | Versión | Notas |
|------------|---------|-------|
| Node.js | 18.0.0+ | 20.0.0+ recomendado |
| Next.js | 14.0.0+ | Con App Router |
| React | 18.0.0+ | |
| TypeScript | 5.0.0+ | |
| Tailwind CSS | 3.3.0+ | |
| Shadcn/ui | Última versión | |
| Axios | 1.4.0+ | |
| React Hook Form | 7.45.0+ | |
| Zod | 3.21.0+ | |
| TanStack Query | 4.29.0+ | |

### DevOps

| Componente | Versión | Notas |
|------------|---------|-------|
| Docker | 24.0.0+ | |
| Docker Compose | 2.18.0+ | |
| GitHub Actions | N/A | Para CI/CD |
| Nginx | 1.24.0+ | Como proxy inverso |
| Certbot | Última versión | Para certificados SSL |
| Prometheus | 2.45.0+ | Para monitoreo (opcional) |
| Grafana | 10.0.0+ | Para visualización de métricas (opcional) |

## Configuración de Red

### Puertos Requeridos

| Puerto | Propósito | Notas |
|--------|-----------|-------|
| 80 | HTTP | Redirigir a HTTPS |
| 443 | HTTPS | Tráfico web seguro |
| 5432 | PostgreSQL | Solo accesible internamente |
| 6379 | Redis | Solo accesible internamente |
| 8000 | API Backend | Detrás de proxy |
| 3000 | Frontend Dev | Solo en desarrollo |

### Dominios y DNS

- Configurar dominio principal para la aplicación
- Configurar subdominios para:
  - API (`api.ejemplo.com`)
  - Documentación (`docs.ejemplo.com`)
  - Admin (`admin.ejemplo.com`)

### Seguridad de Red

- Implementar firewall para limitar acceso
- Configurar CORS adecuadamente
- Implementar rate limiting
- Configurar HTTPS con certificados válidos
- Implementar headers de seguridad (CSP, HSTS, etc.)

## Cuentas de Servicio

### Twilio

- Cuenta de Twilio con saldo suficiente
- Número de teléfono configurado
- Webhooks configurados para:
  - Eventos de llamada
  - Grabaciones
  - Transcripciones

### ElevenLabs

- Cuenta con plan adecuado para volumen esperado
- Voces configuradas para diferentes tipos de campaña
- API key con permisos adecuados

### Supabase

- Proyecto configurado
- Base de datos inicializada con esquema
- Autenticación configurada
- Políticas RLS implementadas
- Backups automáticos habilitados

### OpenAI/Google AI

- Cuenta con acceso a modelos necesarios
- API key con límites adecuados
- Monitoreo de uso configurado

## Variables de Entorno

### Backend

```
# Servidor
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=https://ejemplo.com,https://www.ejemplo.com

# Base de Datos
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJxxxxx
SUPABASE_JWT_SECRET=your-jwt-secret

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_DB=0

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_CALLBACK_URL=https://api.ejemplo.com/webhooks/twilio

# ElevenLabs
ELEVENLABS_API_KEY=your-api-key
ELEVENLABS_VOICE_ID_DEFAULT=voice-id
ELEVENLABS_VOICE_ID_SALES=voice-id-sales
ELEVENLABS_VOICE_ID_SUPPORT=voice-id-support

# IA
OPENAI_API_KEY=your-openai-key
GOOGLE_AI_API_KEY=your-google-ai-key
AI_PROVIDER=openai  # o google
AI_MODEL=gpt-4  # o gemini-pro
```

### Frontend

```
# API
NEXT_PUBLIC_API_URL=https://api.ejemplo.com
NEXT_PUBLIC_ENVIRONMENT=production

# Autenticación
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxxxx

# Analíticas (opcional)
NEXT_PUBLIC_ANALYTICS_ID=UA-XXXXX-Y
```

## Procedimiento de Despliegue

1. **Preparación**
   - Verificar que todas las variables de entorno están configuradas
   - Asegurar que todas las dependencias están actualizadas
   - Ejecutar pruebas automatizadas

2. **Base de Datos**
   - Ejecutar migraciones de base de datos
   - Verificar integridad de datos
   - Crear índices necesarios

3. **Backend**
   - Construir imagen Docker
   - Desplegar contenedor
   - Verificar logs y estado

4. **Frontend**
   - Construir aplicación Next.js
   - Desplegar archivos estáticos
   - Configurar caché y CDN

5. **Configuración de Proxy**
   - Configurar Nginx como proxy inverso
   - Configurar certificados SSL
   - Configurar compresión y caché

6. **Verificación**
   - Probar endpoints críticos
   - Verificar flujos principales
   - Comprobar integraciones externas

## Monitoreo y Mantenimiento

### Monitoreo

- Configurar alertas para:
  - Errores de servidor (5xx)
  - Latencia elevada
  - Uso excesivo de recursos
  - Fallos en integraciones externas

- Implementar logging para:
  - Errores de aplicación
  - Eventos de autenticación
  - Operaciones críticas
  - Rendimiento de API

### Backups

- Configurar backups diarios de base de datos
- Almacenar backups en ubicación segura
- Probar restauración periódicamente

### Mantenimiento

- Programar ventanas de mantenimiento
- Implementar estrategia de actualización
- Documentar procedimientos de rollback

## Escalabilidad

Para escalar el MVP en el futuro:

- Implementar balanceo de carga
- Configurar auto-scaling
- Optimizar consultas de base de datos
- Implementar sharding si es necesario
- Mejorar estrategias de caché

## Documentación Adicional

- [Guía de Despliegue Detallada](./deployment-guide.md)
- [Procedimientos de Backup y Recuperación](./backup-recovery.md)
- [Guía de Troubleshooting](./troubleshooting-guide.md)
- [Procedimientos de Escalado](./scaling-procedures.md)
