#!/bin/bash

# Script para revisar falsos positivos en informes de seguridad
# Uso: ./scripts/run_false_positives_review.sh [--report <ruta_informe>]

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Revisando falsos positivos en informes de seguridad...${NC}"

# Procesar argumentos
REPORT=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --report)
            REPORT="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Argumento desconocido: $1${NC}"
            exit 1
            ;;
    esac
done

# Crear directorio para informes
mkdir -p reports

# Si no se especificó un informe, buscar el más reciente
if [ -z "$REPORT" ]; then
    echo -e "${YELLOW}No se especificó un informe. Buscando el más reciente...${NC}"

    SECURITY_REPORTS=$(find security-reports -name "*.json" -type f 2>/dev/null)

    if [ -z "$SECURITY_REPORTS" ]; then
        echo -e "${YELLOW}No se encontraron informes de seguridad. Ejecutando verificación de seguridad...${NC}"

        # Ejecutar verificación de seguridad
        python scripts/security_check_local.py

        # Buscar nuevamente
        SECURITY_REPORTS=$(find security-reports -name "*.json" -type f 2>/dev/null)
    fi

    if [ -n "$SECURITY_REPORTS" ]; then
        REPORT=$(ls -t $SECURITY_REPORTS | head -n 1)
        echo -e "${YELLOW}Se utilizará el informe más reciente: $REPORT${NC}"
    else
        echo -e "${RED}No se encontraron informes de seguridad. Por favor, ejecute una verificación de seguridad primero.${NC}"
        exit 1
    fi
fi

# Ejecutar el script de revisión de falsos positivos
echo -e "${YELLOW}Ejecutando revisión de falsos positivos...${NC}"
python scripts/review_false_positives.py --report "$REPORT" --output reports/false_positives_report.md
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Revisión completada con éxito. No se encontraron verdaderos positivos.${NC}"
else
    echo -e "${YELLOW}Se encontraron verdaderos positivos. Consulte reports/false_positives_report.md para más detalles.${NC}"
fi

exit $EXIT_CODE
