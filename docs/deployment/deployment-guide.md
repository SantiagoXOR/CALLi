# Guía de Despliegue

## Visión General

Esta guía describe el proceso de despliegue del sistema de automatización de llamadas. El sistema está compuesto por varios componentes que se despliegan utilizando Docker y Docker Compose para garantizar la consistencia entre entornos.

## Requisitos Previos

- [Docker](https://www.docker.com/get-started) (versión 20.10.0 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) (versión 2.0.0 o superior)
- Acceso a las siguientes cuentas de servicio:
  - [Supabase](https://supabase.io/)
  - [Twilio](https://www.twilio.com/)
  - [ElevenLabs](https://elevenlabs.io/)
  - [OpenAI](https://openai.com/) (para el servicio de conversación con IA)

## Arquitectura de Despliegue

El sistema se compone de los siguientes servicios:

1. **Backend (FastAPI)**: API REST que gestiona la lógica de negocio
2. **Frontend (Next.js)**: Interfaz de usuario
3. **Redis**: Sistema de caché para mejorar el rendimiento
4. **Supabase (PostgreSQL)**: Base de datos y autenticación (servicio externo)
5. **Twilio**: Servicio de telefonía (servicio externo)
6. **ElevenLabs**: Servicio de síntesis de voz (servicio externo)

## Entornos de Despliegue

### Desarrollo Local

Para desarrollo local, se recomienda utilizar Docker Compose:

```bash
# Clonar el repositorio
git clone https://github.com/your-organization/call-automation-project.git
cd call-automation-project

# Configurar variables de entorno
cp .env.example .env
# Editar .env con las credenciales adecuadas

# Iniciar los servicios
docker-compose up -d
```

### Staging

El entorno de staging es una réplica del entorno de producción utilizado para pruebas:

```bash
# Desplegar en staging
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

### Producción

Para producción, se recomienda utilizar un orquestador de contenedores como Kubernetes o un servicio gestionado como AWS ECS:

```bash
# Construir imágenes para producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml build

# Desplegar en producción (ejemplo con docker-compose)
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Configuración de Variables de Entorno

### Variables Comunes

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key

# Twilio Configuration
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Redis Configuration
REDIS_URL=redis://redis:6379
REDIS_PASSWORD=your-redis-password
REDIS_CACHE_TTL=3600

# Application Configuration
APP_NAME=Call Automation System
APP_ENV=production
APP_DEBUG=false
APP_URL=https://your-production-domain.com
```

### Variables Específicas del Backend

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# Security Configuration
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false
ENVIRONMENT=production

# ElevenLabs Configuration
ELEVENLABS_API_KEY=your-elevenlabs-api-key
ELEVENLABS_DEFAULT_VOICE=Bella
ELEVENLABS_MAX_RETRIES=3

# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key
DEFAULT_MODEL=gpt-4
MAX_TOKENS=150
TEMPERATURE=0.7
```

### Variables Específicas del Frontend

```env
# Next.js Configuration
NEXT_PUBLIC_API_URL=https://api.your-production-domain.com
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

## Proceso de Despliegue

### 1. Preparación

```bash
# Validar el código
./scripts/validate.sh

# Asegurarse de que todas las pruebas pasan
cd backend-call-automation && pytest
cd frontend-call-automation && npm run test
```

### 2. Construcción de Imágenes

```bash
# Construir todas las imágenes
docker-compose build

# Construir una imagen específica
docker-compose build backend
docker-compose build frontend
```

### 3. Despliegue

```bash
# Desplegar todos los servicios
docker-compose up -d

# Desplegar un servicio específico
docker-compose up -d backend
docker-compose up -d frontend
```

### 4. Verificación

```bash
# Verificar que los servicios están funcionando
docker-compose ps

# Verificar logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Verificar la API
curl http://localhost:8000/health
```

## Actualizaciones y Rollbacks

### Actualización

```bash
# Actualizar el código
git pull

# Reconstruir las imágenes
docker-compose build

# Reiniciar los servicios
docker-compose up -d
```

### Rollback

En caso de problemas, se puede realizar un rollback a una versión anterior:

```bash
# Detener los servicios
docker-compose down

# Volver a una versión anterior
git checkout v1.0.0

# Reconstruir las imágenes
docker-compose build

# Reiniciar los servicios
docker-compose up -d
```

También se puede utilizar el script de rollback automatizado:

```bash
# Ejecutar rollback
python backend-call-automation/scripts/rollback.py --version v1.0.0
```

## Monitoreo y Logs

### Monitoreo

El sistema expone métricas en formato Prometheus en el endpoint `/metrics`:

```bash
# Acceder a las métricas
curl http://localhost:8000/metrics
```

### Logs

Los logs se envían a la salida estándar y pueden ser recolectados por herramientas como ELK Stack o Datadog:

```bash
# Ver logs en tiempo real
docker-compose logs -f
```

## Respaldo y Recuperación

### Respaldo de Base de Datos

```bash
# Crear un respaldo de la base de datos
pg_dump -h localhost -p 54322 -U postgres -d postgres -F c -f backup.dump
```

### Recuperación de Base de Datos

```bash
# Restaurar un respaldo de la base de datos
pg_restore -h localhost -p 54322 -U postgres -d postgres -c backup.dump
```

## Consideraciones de Seguridad

1. **Secretos**: Utilizar servicios de gestión de secretos como AWS Secrets Manager o HashiCorp Vault
2. **Certificados SSL**: Configurar HTTPS para todas las comunicaciones
3. **Firewall**: Limitar el acceso a los puertos necesarios
4. **Actualizaciones**: Mantener las imágenes de Docker actualizadas
5. **Escaneo de Vulnerabilidades**: Utilizar herramientas como Snyk o Trivy para escanear las imágenes

## Solución de Problemas

### Problemas Comunes

1. **Servicios que no inician**: Verificar logs con `docker-compose logs -f`
2. **Problemas de conexión a la base de datos**: Verificar credenciales y disponibilidad
3. **Errores de API**: Verificar logs del backend y configuración de variables de entorno
4. **Problemas de frontend**: Verificar logs del frontend y configuración de variables de entorno

### Comandos Útiles

```bash
# Reiniciar un servicio
docker-compose restart backend

# Ver logs de un servicio
docker-compose logs -f backend

# Entrar en un contenedor
docker-compose exec backend bash

# Verificar el estado de los servicios
docker-compose ps
```

## Integración Continua y Despliegue Continuo (CI/CD)

El proyecto utiliza GitHub Actions para CI/CD:

1. **Validación**: Ejecuta pruebas y verificaciones de código en cada pull request
2. **Construcción**: Construye imágenes de Docker en cada merge a main
3. **Despliegue**: Despliega automáticamente en staging y, tras aprobación, en producción
4. **Documentación**: Genera y publica la documentación en GitHub Pages

## Referencias

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Supabase Documentation](https://supabase.io/docs)
- [Twilio Documentation](https://www.twilio.com/docs)
- [ElevenLabs Documentation](https://elevenlabs.io/docs)
