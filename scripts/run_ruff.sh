#!/bin/bash

# Script para ejecutar Ruff en todo el proyecto
# Uso: ./scripts/run_ruff.sh [--fix]

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Ejecutando Ruff en el proyecto CALLi...${NC}"

# Verificar si se pasó el argumento --fix
FIX=false
if [ "$1" == "--fix" ]; then
    FIX=true
fi

# Verificar si ruff está instalado
if ! command -v ruff &> /dev/null; then
    echo -e "${YELLOW}Ruff no está instalado. Instalando...${NC}"
    pip install ruff
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error al instalar Ruff. Por favor, instálelo manualmente con 'pip install ruff'${NC}"
        exit 1
    fi
fi

# Crear directorio para informes
mkdir -p reports

# Ejecutar Ruff
if [ "$FIX" = true ]; then
    echo -e "${YELLOW}Ejecutando Ruff con corrección automática...${NC}"
    ruff check --fix .
    EXIT_CODE=$?

    # Ejecutar el formateador de Ruff
    echo -e "${YELLOW}Ejecutando el formateador de Ruff...${NC}"
    ruff format .
    FORMAT_EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ] && [ $FORMAT_EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}Ruff completado con éxito. Se han corregido los problemas de formato.${NC}"
    else
        echo -e "${YELLOW}Ruff completado con errores. Algunos problemas pueden requerir corrección manual.${NC}"
    fi
else
    echo -e "${YELLOW}Ejecutando Ruff en modo verificación...${NC}"
    ruff check . > reports/ruff_report.txt
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo -e "${GREEN}Ruff completado con éxito. No se encontraron problemas de formato.${NC}"
    else
        echo -e "${YELLOW}Ruff encontró problemas de formato. Consulte reports/ruff_report.txt para más detalles.${NC}"
        echo -e "${YELLOW}Para corregir automáticamente los problemas, ejecute ./scripts/run_ruff.sh --fix${NC}"
    fi
fi

exit $EXIT_CODE
