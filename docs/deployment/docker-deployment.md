# Despliegue con Docker

## Visión General

Este documento proporciona instrucciones detalladas para desplegar el sistema de automatización de llamadas utilizando Docker y Docker Compose. Docker permite empaquetar la aplicación y sus dependencias en contenedores, garantizando la consistencia entre entornos de desarrollo, pruebas y producción.

## Requisitos Previos

- [Docker](https://www.docker.com/get-started) (versión 20.10.0 o superior)
- [Docker Compose](https://docs.docker.com/compose/install/) (versión 2.0.0 o superior)
- Git para clonar el repositorio

## Estructura de Contenedores

El sistema se compone de los siguientes contenedores:

1. **backend**: Servicio FastAPI que proporciona la API REST
2. **frontend**: Aplicación Next.js que proporciona la interfaz de usuario
3. **redis**: Servicio de caché para mejorar el rendimiento

## Archivos Dockerfile

### Backend Dockerfile

```dockerfile
# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libyaml-dev \
    plantuml \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    pydantic_settings \
    sphinx \
    sphinx-rtd-theme \
    sphinxcontrib-plantuml

# Copy the rest of the application
COPY . .

# Build documentation
RUN cd docs && make html

# Expose port 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
# Use Node.js LTS version as base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
```

## Configuración de Docker Compose

El archivo `docker-compose.yml` define los servicios, redes y volúmenes necesarios para el sistema:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend-call-automation
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - TWILIO_ACCOUNT_SID=${TWILIO_ACCOUNT_SID}
      - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=redis://redis:6379
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - REDIS_CACHE_TTL=${REDIS_CACHE_TTL}
    volumes:
      - ./backend-call-automation:/app
      - /app/venv
    depends_on:
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend-call-automation
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
      - NEXT_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_KEY}
    volumes:
      - ./frontend-call-automation:/app
      - /app/node_modules
      - /app/.next
    depends_on:
      backend:
        condition: service_healthy

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  redis_data:
    driver: local

networks:
  default:
    name: call-automation-network
```

## Configuración de Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key

# Twilio Configuration
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token

# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# Redis Configuration
REDIS_PASSWORD=your-redis-password
REDIS_CACHE_TTL=3600
```

## Proceso de Despliegue

### 1. Clonar el Repositorio

```bash
git clone https://github.com/your-organization/call-automation-project.git
cd call-automation-project
```

### 2. Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env con las credenciales adecuadas
```

### 3. Construir las Imágenes

```bash
docker-compose build
```

### 4. Iniciar los Servicios

```bash
docker-compose up -d
```

### 5. Verificar el Despliegue

```bash
# Verificar que los servicios están funcionando
docker-compose ps

# Verificar logs
docker-compose logs -f

# Verificar la API
curl http://localhost:8000/health

# Acceder a la interfaz de usuario
# Abrir http://localhost:3000 en el navegador
```

## Configuración para Diferentes Entornos

### Desarrollo

Para desarrollo, se recomienda montar los directorios locales como volúmenes para facilitar el desarrollo:

```yaml
volumes:
  - ./backend-call-automation:/app
  - /app/venv
```

### Producción

Para producción, se recomienda utilizar imágenes precompiladas y no montar volúmenes:

```bash
# Crear archivo docker-compose.prod.yml
cat > docker-compose.prod.yml << EOL
version: '3.8'

services:
  backend:
    volumes: []
    restart: always
    environment:
      - APP_ENV=production
      - DEBUG=false

  frontend:
    volumes: []
    restart: always
    environment:
      - NODE_ENV=production

  redis:
    restart: always
EOL

# Desplegar en producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Escalabilidad

Para escalar horizontalmente los servicios:

```bash
# Escalar el backend a 3 instancias
docker-compose up -d --scale backend=3

# Nota: Se requiere un balanceador de carga para distribuir el tráfico
```

## Respaldo y Persistencia

Los datos de Redis se persisten en un volumen Docker:

```yaml
volumes:
  redis_data:
    driver: local
```

Para realizar un respaldo:

```bash
# Crear un respaldo del volumen de Redis
docker run --rm -v call-automation-project_redis_data:/data -v $(pwd):/backup alpine tar -czf /backup/redis-backup.tar.gz /data
```

Para restaurar un respaldo:

```bash
# Restaurar un respaldo del volumen de Redis
docker run --rm -v call-automation-project_redis_data:/data -v $(pwd):/backup alpine sh -c "rm -rf /data/* && tar -xzf /backup/redis-backup.tar.gz -C /"
```

## Monitoreo y Logs

### Logs

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
```

### Monitoreo

Se puede integrar con herramientas de monitoreo como Prometheus y Grafana:

```yaml
# Ejemplo de configuración para Prometheus
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  depends_on:
    - backend

# Ejemplo de configuración para Grafana
grafana:
  image: grafana/grafana
  ports:
    - "3001:3000"
  depends_on:
    - prometheus
```

## Seguridad

### Redes

Docker Compose crea una red interna para los servicios:

```yaml
networks:
  default:
    name: call-automation-network
```

### Secretos

Para gestionar secretos en producción, se recomienda utilizar Docker Secrets:

```yaml
secrets:
  supabase_key:
    external: true
  twilio_auth_token:
    external: true
  redis_password:
    external: true
```

## Solución de Problemas

### Problemas Comunes

1. **Contenedores que no inician**:
   ```bash
   docker-compose logs -f <service-name>
   ```

2. **Problemas de red**:
   ```bash
   docker network inspect call-automation-network
   ```

3. **Problemas de volúmenes**:
   ```bash
   docker volume inspect call-automation-project_redis_data
   ```

### Reinicio de Servicios

```bash
# Reiniciar un servicio específico
docker-compose restart backend

# Reiniciar todos los servicios
docker-compose restart
```

## Comandos Útiles

```bash
# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Ver el uso de recursos
docker stats

# Ejecutar un comando en un contenedor
docker-compose exec backend bash
docker-compose exec redis redis-cli

# Actualizar imágenes y reiniciar servicios
docker-compose pull && docker-compose up -d
```

## Referencias

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Networking](https://docs.docker.com/network/)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)
