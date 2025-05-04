#!/bin/bash

# Script para ejecutar MyPy en todo el proyecto
# Uso: ./scripts/run_mypy.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Ejecutando MyPy en el proyecto CALLi...${NC}"

# Verificar si mypy está instalado
if ! command -v mypy &> /dev/null; then
    echo -e "${YELLOW}MyPy no está instalado. Instalando...${NC}"
    pip install mypy
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error al instalar MyPy. Por favor, instálelo manualmente con 'pip install mypy'${NC}"
        exit 1
    fi
fi

# Crear directorio para informes
mkdir -p reports

# Ejecutar MyPy en el backend
echo -e "${YELLOW}Ejecutando MyPy en el backend...${NC}"
mypy backend-call-automation > reports/mypy_report.txt
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}MyPy completado con éxito. No se encontraron problemas de tipos.${NC}"
else
    echo -e "${YELLOW}MyPy encontró problemas de tipos. Consulte reports/mypy_report.txt para más detalles.${NC}"
    
    # Contar errores por categoría
    ERROR_COUNT=$(wc -l < reports/mypy_report.txt)
    ANNOTATION_MISSING=$(grep -c "Missing type annotation" reports/mypy_report.txt)
    INCOMPATIBLE_TYPE=$(grep -c "Incompatible type" reports/mypy_report.txt)
    NAME_ERROR=$(grep -c "Name" reports/mypy_report.txt)
    
    echo -e "${YELLOW}Resumen de errores:${NC}"
    echo -e "${YELLOW}- Total de errores: $ERROR_COUNT${NC}"
    echo -e "${YELLOW}- Anotaciones faltantes: $ANNOTATION_MISSING${NC}"
    echo -e "${YELLOW}- Tipos incompatibles: $INCOMPATIBLE_TYPE${NC}"
    echo -e "${YELLOW}- Errores de nombres: $NAME_ERROR${NC}"
fi

exit $EXIT_CODE
