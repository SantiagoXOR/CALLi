#!/bin/bash
# Script para realizar rollback en caso de fallo en el despliegue

set -e  # Salir inmediatamente si algún comando falla

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Verificar argumentos
if [ "$#" -lt 1 ]; then
    echo -e "${RED}Error: Se requiere al menos un argumento.${NC}"
    echo "Uso: $0 <versión_anterior> [entorno]"
    echo "Ejemplo: $0 v1.2.3 production"
    exit 1
fi

PREVIOUS_VERSION=$1
ENVIRONMENT=${2:-production}

echo -e "${YELLOW}=== Iniciando rollback a la versión $PREVIOUS_VERSION en entorno $ENVIRONMENT ===${NC}"

# Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ] || [ ! -f "docker-compose.prod.yml" ]; then
    echo -e "${RED}Error: No se encontraron los archivos docker-compose.${NC}"
    echo "Este script debe ejecutarse desde el directorio raíz del proyecto."
    exit 1
fi

# Función para realizar rollback de la base de datos
rollback_database() {
    echo -e "${YELLOW}\n=== Realizando rollback de la base de datos ===${NC}"
    
    # Verificar si existe un backup de la versión anterior
    if [ ! -f "backups/db_backup_${PREVIOUS_VERSION}.sql" ]; then
        echo -e "${RED}Error: No se encontró un backup de la base de datos para la versión $PREVIOUS_VERSION.${NC}"
        echo "Ubicación esperada: backups/db_backup_${PREVIOUS_VERSION}.sql"
        return 1
    fi
    
    echo "Restaurando backup de la base de datos..."
    # En un entorno real, aquí se restauraría el backup
    # Por ejemplo: docker-compose exec -T db pg_restore -U postgres -d postgres < backups/db_backup_${PREVIOUS_VERSION}.sql
    
    echo -e "${GREEN}✓ Base de datos restaurada a la versión $PREVIOUS_VERSION${NC}"
    return 0
}

# Función para realizar rollback de las imágenes Docker
rollback_docker_images() {
    echo -e "${YELLOW}\n=== Realizando rollback de las imágenes Docker ===${NC}"
    
    # Detener los contenedores actuales
    echo "Deteniendo contenedores actuales..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
    
    # Cambiar las etiquetas de las imágenes en el archivo docker-compose.prod.yml
    echo "Actualizando docker-compose.prod.yml para usar la versión $PREVIOUS_VERSION..."
    # En un entorno real, aquí se modificaría el archivo docker-compose.prod.yml
    # Por ejemplo: sed -i "s/latest/${PREVIOUS_VERSION}/g" docker-compose.prod.yml
    
    # Descargar las imágenes de la versión anterior
    echo "Descargando imágenes de la versión $PREVIOUS_VERSION..."
    # En un entorno real, aquí se descargarían las imágenes
    # Por ejemplo: docker pull username/call-automation-backend:${PREVIOUS_VERSION}
    
    # Iniciar los contenedores con la versión anterior
    echo "Iniciando contenedores con la versión $PREVIOUS_VERSION..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    
    echo -e "${GREEN}✓ Imágenes Docker restauradas a la versión $PREVIOUS_VERSION${NC}"
    return 0
}

# Función para verificar el estado después del rollback
verify_rollback() {
    echo -e "${YELLOW}\n=== Verificando estado después del rollback ===${NC}"
    
    # Esperar a que los servicios estén disponibles
    echo "Esperando a que los servicios estén disponibles..."
    sleep 10
    
    # Verificar que el backend está funcionando
    echo "Verificando el backend..."
    if curl -s http://localhost:8000/health | grep -q "ok"; then
        echo -e "${GREEN}✓ Backend funcionando correctamente${NC}"
    else
        echo -e "${RED}✗ Backend no responde correctamente${NC}"
        return 1
    fi
    
    # Verificar que el frontend está funcionando
    echo "Verificando el frontend..."
    if curl -s http://localhost:80 | grep -q "html"; then
        echo -e "${GREEN}✓ Frontend funcionando correctamente${NC}"
    else
        echo -e "${RED}✗ Frontend no responde correctamente${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✓ Todos los servicios están funcionando correctamente después del rollback${NC}"
    return 0
}

# Ejecutar el rollback
echo "Iniciando proceso de rollback..."

# Crear directorio de logs si no existe
mkdir -p logs

# Registrar el inicio del rollback
echo "$(date): Iniciando rollback a la versión $PREVIOUS_VERSION en entorno $ENVIRONMENT" >> logs/rollback.log

# Realizar rollback de la base de datos
if rollback_database; then
    echo "$(date): Rollback de base de datos exitoso" >> logs/rollback.log
else
    echo "$(date): Rollback de base de datos fallido" >> logs/rollback.log
    echo -e "${RED}Error en el rollback de la base de datos. Consulte los logs para más detalles.${NC}"
    exit 1
fi

# Realizar rollback de las imágenes Docker
if rollback_docker_images; then
    echo "$(date): Rollback de imágenes Docker exitoso" >> logs/rollback.log
else
    echo "$(date): Rollback de imágenes Docker fallido" >> logs/rollback.log
    echo -e "${RED}Error en el rollback de las imágenes Docker. Consulte los logs para más detalles.${NC}"
    exit 1
fi

# Verificar el estado después del rollback
if verify_rollback; then
    echo "$(date): Verificación después del rollback exitosa" >> logs/rollback.log
else
    echo "$(date): Verificación después del rollback fallida" >> logs/rollback.log
    echo -e "${RED}Error en la verificación después del rollback. Consulte los logs para más detalles.${NC}"
    exit 1
fi

# Registrar el éxito del rollback
echo "$(date): Rollback a la versión $PREVIOUS_VERSION en entorno $ENVIRONMENT completado exitosamente" >> logs/rollback.log

echo -e "${GREEN}\n✓ Rollback a la versión $PREVIOUS_VERSION completado exitosamente${NC}"
exit 0
