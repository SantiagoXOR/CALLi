#!/bin/bash
# Script para ejecutar pruebas en el proyecto CALLi

set -e  # Salir inmediatamente si algún comando falla

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Ejecutando pruebas para CALLi ===${NC}"

# Verificar entorno
if [ ! -d "backend-call-automation" ] || [ ! -d "frontend-call-automation" ]; then
    echo -e "${RED}Error: Directorio de backend o frontend no encontrado.${NC}"
    echo "Este script debe ejecutarse desde el directorio raíz del proyecto."
    exit 1
fi

# Configurar entorno para pruebas
export TESTING=1
export APP_ENV=testing
export ENVIRONMENT=testing

# Función para ejecutar pruebas del backend
run_backend_tests() {
    echo -e "${YELLOW}\n=== Ejecutando pruebas del backend ===${NC}"
    cd backend-call-automation

    # Verificar si existe el directorio de pruebas
    if [ ! -d "tests" ]; then
        echo -e "${RED}Error: Directorio de pruebas no encontrado en el backend.${NC}"
        return 1
    fi

    # Verificar entorno virtual de Python
    if [ -d "venv" ] || [ -d ".venv" ]; then
        # Activar entorno virtual si existe
        if [ -d "venv" ]; then
            source venv/bin/activate
        else
            source .venv/bin/activate
        fi
        echo "Entorno virtual activado."
    else
        echo "Advertencia: No se encontró un entorno virtual. Usando Python del sistema."
    fi

    # Instalar dependencias si es necesario
    if [ ! -f ".test_deps_installed" ]; then
        echo "Instalando dependencias de prueba..."
        pip install pytest pytest-cov pytest-asyncio
        touch .test_deps_installed
    fi

    # Asegurarse de que el directorio de logs existe
    mkdir -p logs

    # Crear archivo de log si no existe
    touch logs/app.log

    # Ejecutar pruebas básicas primero
    echo "Ejecutando pruebas básicas..."
    if pytest tests/test_basic.py -v; then
        echo -e "${GREEN}✓ Pruebas básicas exitosas${NC}"
    else
        echo -e "${RED}✗ Pruebas básicas fallaron${NC}"
        return 1
    fi

    # Ejecutar todas las pruebas con cobertura
    echo "Ejecutando todas las pruebas con cobertura..."
    if pytest tests/ --cov=app -v; then
        echo -e "${GREEN}✓ Todas las pruebas del backend exitosas${NC}"
    else
        echo -e "${RED}✗ Algunas pruebas del backend fallaron${NC}"
        return 1
    fi

    # Desactivar entorno virtual si fue activado
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    fi

    cd ..
    return 0
}

# Función para ejecutar pruebas del frontend
run_frontend_tests() {
    echo -e "${YELLOW}\n=== Ejecutando pruebas del frontend ===${NC}"
    cd frontend-call-automation

    # Verificar si existe package.json
    if [ ! -f "package.json" ]; then
        echo -e "${RED}Error: No se encontró package.json en el frontend.${NC}"
        return 1
    fi

    # Verificar si el script de pruebas está definido
    if ! grep -q "\"test\":" "package.json"; then
        echo -e "${RED}Error: No se encontró el script de pruebas en package.json.${NC}"
        return 1
    fi

    # Ejecutar pruebas
    echo "Ejecutando pruebas del frontend..."
    if npm test -- --passWithNoTests; then
        echo -e "${GREEN}✓ Pruebas del frontend exitosas${NC}"
    else
        echo -e "${RED}✗ Pruebas del frontend fallaron${NC}"
        return 1
    fi

    cd ..
    return 0
}

# Ejecutar pruebas
backend_success=false
frontend_success=false

# Ejecutar pruebas del backend
if run_backend_tests; then
    backend_success=true
else
    echo -e "${RED}Las pruebas del backend fallaron.${NC}"
fi

# Ejecutar pruebas del frontend
if run_frontend_tests; then
    frontend_success=true
else
    echo -e "${RED}Las pruebas del frontend fallaron.${NC}"
fi

# Resumen
echo -e "${YELLOW}\n=== Resumen de pruebas ===${NC}"
if $backend_success; then
    echo -e "${GREEN}✓ Backend: Pruebas exitosas${NC}"
else
    echo -e "${RED}✗ Backend: Pruebas fallidas${NC}"
fi

if $frontend_success; then
    echo -e "${GREEN}✓ Frontend: Pruebas exitosas${NC}"
else
    echo -e "${RED}✗ Frontend: Pruebas fallidas${NC}"
fi

# Salir con código de error si alguna prueba falló
if $backend_success && $frontend_success; then
    echo -e "${GREEN}\n✓ Todas las pruebas pasaron exitosamente${NC}"
    exit 0
else
    echo -e "${RED}\n✗ Algunas pruebas fallaron${NC}"
    exit 1
fi
