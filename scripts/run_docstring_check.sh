#!/bin/bash

# Script para verificar docstrings en el proyecto
# Uso: ./scripts/run_docstring_check.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Verificando docstrings en el proyecto CALLi...${NC}"

# Crear directorio para informes
mkdir -p reports

# Ejecutar el script de verificación de docstrings
echo -e "${YELLOW}Ejecutando verificación de docstrings...${NC}"
python scripts/check_docstrings.py --directory backend-call-automation --output reports/docstrings_report.txt
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Verificación completada con éxito. No se encontraron problemas de documentación.${NC}"
else
    echo -e "${YELLOW}Se encontraron elementos sin docstrings. Consulte reports/docstrings_report.txt para más detalles.${NC}"
fi

exit $EXIT_CODE
