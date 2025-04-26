#!/bin/bash
# Script para automatizar verificaciones de despliegue

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo "=== Sistema de Automatización de Llamadas - Verificación de Despliegue ==="
echo "Ejecutando verificaciones pre-despliegue..."

# Verificar que estamos en la rama principal
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    echo -e "${RED}[ERROR] No estás en la rama principal. Estás en: $CURRENT_BRANCH${NC}"
    echo "Por favor, cambia a la rama principal antes de continuar."
    exit 1
else
    echo -e "${GREEN}[OK] Estás en la rama principal: $CURRENT_BRANCH${NC}"
fi

# Verificar que no hay cambios sin commitear
if [ -n "$(git status --porcelain)" ]; then
    echo -e "${RED}[ERROR] Hay cambios sin commitear en el repositorio.${NC}"
    git status --short
    echo "Por favor, haz commit de los cambios o descártalos antes de continuar."
    exit 1
else
    echo -e "${GREEN}[OK] No hay cambios sin commitear.${NC}"
fi

# Verificar que CHANGELOG.md existe y está actualizado
if [ ! -f "CHANGELOG.md" ]; then
    echo -e "${RED}[ERROR] No se encontró el archivo CHANGELOG.md${NC}"
    echo "Por favor, crea el archivo CHANGELOG.md antes de continuar."
    exit 1
else
    LAST_MODIFIED=$(git log -1 --format="%ar" -- CHANGELOG.md)
    echo -e "${GREEN}[OK] CHANGELOG.md existe. Última modificación: $LAST_MODIFIED${NC}"
fi

# Verificar que las pruebas unitarias pasan
echo "Ejecutando pruebas unitarias del backend..."
cd backend-call-automation
if ! pytest -xvs; then
    echo -e "${RED}[ERROR] Las pruebas unitarias del backend han fallado.${NC}"
    exit 1
else
    echo -e "${GREEN}[OK] Las pruebas unitarias del backend han pasado.${NC}"
fi

# Volver al directorio raíz
cd ..

# Verificar que las pruebas unitarias del frontend pasan
echo "Ejecutando pruebas unitarias del frontend..."
cd frontend-call-automation
if ! npm test; then
    echo -e "${RED}[ERROR] Las pruebas unitarias del frontend han fallado.${NC}"
    exit 1
else
    echo -e "${GREEN}[OK] Las pruebas unitarias del frontend han pasado.${NC}"
fi

# Volver al directorio raíz
cd ..

# Verificar que las variables de entorno están configuradas
if [ ! -f ".env.production" ]; then
    echo -e "${RED}[ERROR] No se encontró el archivo .env.production${NC}"
    echo "Por favor, crea el archivo .env.production antes de continuar."
    exit 1
else
    echo -e "${GREEN}[OK] Archivo .env.production encontrado.${NC}"
    
    # Verificar variables críticas
    REQUIRED_VARS=("SUPABASE_URL" "SUPABASE_KEY" "TWILIO_ACCOUNT_SID" "TWILIO_AUTH_TOKEN" "REDIS_PASSWORD" "SECRET_KEY" "ELEVENLABS_API_KEY" "OPENAI_API_KEY")
    MISSING_VARS=0
    
    for VAR in "${REQUIRED_VARS[@]}"; do
        if ! grep -q "^$VAR=" .env.production; then
            echo -e "${RED}[ERROR] Variable de entorno requerida no encontrada: $VAR${NC}"
            MISSING_VARS=$((MISSING_VARS+1))
        fi
    done
    
    if [ $MISSING_VARS -gt 0 ]; then
        echo -e "${RED}[ERROR] Faltan $MISSING_VARS variables de entorno requeridas.${NC}"
        exit 1
    else
        echo -e "${GREEN}[OK] Todas las variables de entorno requeridas están configuradas.${NC}"
    fi
fi

# Verificar que Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker no está instalado.${NC}"
    exit 1
else
    echo -e "${GREEN}[OK] Docker está instalado: $(docker --version)${NC}"
fi

# Verificar que Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}[ERROR] Docker Compose no está instalado.${NC}"
    exit 1
else
    echo -e "${GREEN}[OK] Docker Compose está instalado: $(docker-compose --version)${NC}"
fi

# Verificar que los archivos Docker existen
if [ ! -f "docker-compose.yml" ] || [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}[ERROR] Faltan archivos Docker Compose.${NC}"
    [ ! -f "docker-compose.yml" ] && echo "Falta: docker-compose.yml"
    [ ! -f "docker-compose.prod.yml" ] && echo "Falta: docker-compose.prod.yml"
    exit 1
else
    echo -e "${GREEN}[OK] Archivos Docker Compose encontrados.${NC}"
fi

# Verificar que los Dockerfiles existen
if [ ! -f "backend-call-automation/Dockerfile" ] || [ ! -f "frontend-call-automation/Dockerfile.prod" ]; then
    echo -e "${RED}[ERROR] Faltan Dockerfiles.${NC}"
    [ ! -f "backend-call-automation/Dockerfile" ] && echo "Falta: backend-call-automation/Dockerfile"
    [ ! -f "frontend-call-automation/Dockerfile.prod" ] && echo "Falta: frontend-call-automation/Dockerfile.prod"
    exit 1
else
    echo -e "${GREEN}[OK] Dockerfiles encontrados.${NC}"
fi

# Verificar configuración de Nginx
if [ ! -d "nginx/conf.d" ] || [ ! -f "nginx/conf.d/default.conf" ]; then
    echo -e "${YELLOW}[ADVERTENCIA] Configuración de Nginx no encontrada o incompleta.${NC}"
    echo "Se recomienda configurar Nginx para producción."
else
    echo -e "${GREEN}[OK] Configuración de Nginx encontrada.${NC}"
fi

# Verificar configuración de monitoreo
if [ ! -f "prometheus.yml" ] || [ ! -f "alert_rules.yml" ] || [ ! -f "docker-compose.monitoring.yml" ]; then
    echo -e "${YELLOW}[ADVERTENCIA] Configuración de monitoreo no encontrada o incompleta.${NC}"
    echo "Se recomienda configurar el monitoreo antes del despliegue."
else
    echo -e "${GREEN}[OK] Configuración de monitoreo encontrada.${NC}"
fi

# Verificar plan de pruebas de usuario
if [ ! -f "docs/testing/user-testing-plan.md" ] || [ ! -f "docs/testing/user-feedback-form.md" ]; then
    echo -e "${YELLOW}[ADVERTENCIA] Plan de pruebas de usuario no encontrado o incompleto.${NC}"
    echo "Se recomienda preparar el plan de pruebas de usuario antes del despliegue."
else
    echo -e "${GREEN}[OK] Plan de pruebas de usuario encontrado.${NC}"
fi

# Verificar checklist de despliegue
if [ ! -f "docs/deployment/deployment-checklist.md" ]; then
    echo -e "${YELLOW}[ADVERTENCIA] Checklist de despliegue no encontrado.${NC}"
    echo "Se recomienda preparar el checklist de despliegue antes de continuar."
else
    echo -e "${GREEN}[OK] Checklist de despliegue encontrado.${NC}"
fi

echo ""
echo "=== Resumen de Verificación ==="
echo -e "${GREEN}Verificaciones completadas. El sistema está listo para el despliegue.${NC}"
echo "Por favor, revisa cualquier advertencia antes de proceder."
echo "Ejecuta el siguiente comando para iniciar el despliegue:"
echo -e "${YELLOW}docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d${NC}"
echo ""
echo "Recuerda seguir el checklist de despliegue completo en docs/deployment/deployment-checklist.md"
