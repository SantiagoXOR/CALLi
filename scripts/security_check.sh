#!/bin/bash

# Script para ejecutar verificaciones de seguridad localmente
# Uso: ./scripts/security_check.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando verificaciones de seguridad...${NC}"
echo

# Verificar frontend
echo -e "${YELLOW}Verificando dependencias del frontend...${NC}"
cd frontend-call-automation

if ! command -v npm &> /dev/null; then
    echo -e "${RED}Error: npm no está instalado${NC}"
    exit 1
fi

echo "Ejecutando npm audit..."
npm_audit_result=$(npm audit --json 2>/dev/null)
high_critical=$(echo $npm_audit_result | grep -o '"severity":"high\|critical"' | wc -l)

if [ $high_critical -gt 0 ]; then
    echo -e "${RED}Se encontraron $high_critical vulnerabilidades de alta o crítica severidad${NC}"
    echo "Ejecute 'cd frontend-call-automation && npm audit' para más detalles"
else
    echo -e "${GREEN}No se encontraron vulnerabilidades de alta o crítica severidad en el frontend${NC}"
fi

# Volver al directorio raíz
cd ..

# Verificar backend
echo
echo -e "${YELLOW}Verificando dependencias del backend...${NC}"
cd backend-call-automation

if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: python no está instalado${NC}"
    exit 1
fi

if ! python -m pip show safety &> /dev/null; then
    echo "Instalando safety..."
    python -m pip install safety
fi

echo "Ejecutando safety check..."
safety_result=$(python -m safety check --json 2>/dev/null)
vulnerabilities=$(echo $safety_result | grep -o '"vulnerability_id"' | wc -l)

if [ $vulnerabilities -gt 0 ]; then
    echo -e "${RED}Se encontraron $vulnerabilities vulnerabilidades${NC}"
    echo "Ejecute 'cd backend-call-automation && python -m safety check' para más detalles"
else
    echo -e "${GREEN}No se encontraron vulnerabilidades en el backend${NC}"
fi

# Volver al directorio raíz
cd ..

echo
echo -e "${YELLOW}Verificaciones de seguridad completadas${NC}"

if [ $high_critical -gt 0 ] || [ $vulnerabilities -gt 0 ]; then
    echo -e "${RED}Se encontraron vulnerabilidades. Por favor, revise los detalles y actualice las dependencias afectadas.${NC}"
    exit 1
else
    echo -e "${GREEN}No se encontraron vulnerabilidades críticas o altas.${NC}"
    exit 0
fi
