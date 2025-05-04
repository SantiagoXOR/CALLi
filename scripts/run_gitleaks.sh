#!/bin/bash
# Script para ejecutar gitleaks manualmente
# Uso: ./scripts/run_gitleaks.sh [--install]

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

install=false

# Procesar argumentos
for arg in "$@"; do
    case $arg in
        --install)
            install=true
            shift
            ;;
    esac
done

echo -e "${CYAN}Verificando secretos en el código con gitleaks...${NC}"

# Verificar si gitleaks está instalado
if ! command -v gitleaks &> /dev/null; then
    echo -e "${YELLOW}gitleaks no está instalado${NC}"

    if [ "$install" = true ]; then
        echo -e "${YELLOW}Instalando gitleaks...${NC}"

        # Verificar el sistema operativo
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install gitleaks
            else
                echo -e "${RED}Homebrew no está instalado. Instale Homebrew o gitleaks manualmente.${NC}"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt-get &> /dev/null; then
                # Debian/Ubuntu
                sudo apt-get update
                sudo apt-get install -y gitleaks
            elif command -v dnf &> /dev/null; then
                # Fedora
                sudo dnf install -y gitleaks
            elif command -v yum &> /dev/null; then
                # CentOS/RHEL
                sudo yum install -y gitleaks
            else
                echo -e "${RED}No se pudo determinar el gestor de paquetes. Instale gitleaks manualmente.${NC}"
                exit 1
            fi
        else
            echo -e "${RED}Sistema operativo no soportado. Instale gitleaks manualmente.${NC}"
            exit 1
        fi

        # Verificar si la instalación fue exitosa
        if ! command -v gitleaks &> /dev/null; then
            echo -e "${RED}No se pudo instalar gitleaks. Instálelo manualmente.${NC}"
            exit 1
        else
            echo -e "${GREEN}gitleaks instalado correctamente: $(gitleaks version)${NC}"
        fi
    else
        echo -e "${YELLOW}Para instalar gitleaks, ejecute este script con el parámetro --install o instálelo manualmente.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}gitleaks está instalado: $(gitleaks version)${NC}"
fi

# Crear directorio para el informe si no existe
mkdir -p security-reports

# Ejecutar gitleaks
echo -e "${YELLOW}Ejecutando gitleaks para detectar secretos...${NC}"
gitleaks detect --source . --report-format json --report-path security-reports/gitleaks_report.json
gitleaks_exit_code=$?

if [ $gitleaks_exit_code -eq 0 ]; then
    echo -e "${GREEN}No se encontraron secretos en el código con gitleaks${NC}"
    exit 0
else
    echo -e "${RED}Se encontraron posibles secretos en el código con gitleaks. Consulte security-reports/gitleaks_report.json para más detalles.${NC}"

    # Intentar leer el informe JSON
    if [ -f "security-reports/gitleaks_report.json" ]; then
        if command -v jq &> /dev/null; then
            secret_count=$(jq length security-reports/gitleaks_report.json)
            echo -e "${RED}Se encontraron $secret_count posibles secretos:${NC}"

            jq -c '.[]' security-reports/gitleaks_report.json | while read -r finding; do
                file=$(echo $finding | jq -r '.File')
                line=$(echo $finding | jq -r '.StartLine')
                description=$(echo $finding | jq -r '.Description')
                rule_id=$(echo $finding | jq -r '.RuleID')

                echo -e "${RED}  - Archivo: $file${NC}"
                echo -e "${RED}    Línea: $line${NC}"
                echo -e "${RED}    Descripción: $description${NC}"
                echo -e "${RED}    Regla: $rule_id${NC}"
                echo ""
            done
        else
            echo -e "${YELLOW}Instale jq para ver un resumen detallado del informe.${NC}"
        fi

        echo -e "${YELLOW}Recomendaciones:${NC}"
        echo -e "${YELLOW}1. Revise los secretos encontrados y elimínelos del código${NC}"
        echo -e "${YELLOW}2. Utilice variables de entorno o servicios de gestión de secretos como Vault${NC}"
        echo -e "${YELLOW}3. Rote cualquier secreto que haya sido expuesto${NC}"
        echo -e "${YELLOW}4. Considere usar la función secure_mask_secret de scripts/improved_security_utils.py para enmascarar secretos en logs${NC}"
    else
        echo -e "${RED}No se pudo generar el informe de gitleaks.${NC}"
    fi

    exit 1
fi
