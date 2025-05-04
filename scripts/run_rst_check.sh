#!/bin/bash

# Script para verificar archivos RST en el proyecto
# Uso: ./scripts/run_rst_check.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Verificando archivos RST en el proyecto CALLi...${NC}"

# Verificar si docutils está instalado
if ! python -c "import docutils" &> /dev/null; then
    echo -e "${YELLOW}docutils no está instalado. Instalando...${NC}"
    pip install docutils
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error al instalar docutils. Por favor, instálelo manualmente con 'pip install docutils'${NC}"
        exit 1
    fi
fi

# Crear directorio para informes
mkdir -p reports

# Ejecutar el script de verificación de RST
echo -e "${YELLOW}Ejecutando verificación de archivos RST...${NC}"
python scripts/check_rst.py --directory backend-call-automation/docs --output reports/rst_report.txt
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Verificación completada con éxito. No se encontraron problemas en los archivos RST.${NC}"
else
    echo -e "${YELLOW}Se encontraron problemas en los archivos RST. Consulte reports/rst_report.txt para más detalles.${NC}"
fi

exit $EXIT_CODE
