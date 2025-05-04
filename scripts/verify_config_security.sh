#!/bin/bash
# Script para verificar la seguridad de la configuración localmente
# Uso: ./scripts/verify_config_security.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando verificación de seguridad de configuración...${NC}"
echo

# Verificar si KICS está instalado
if ! command -v kics &> /dev/null; then
    echo -e "${RED}KICS no está instalado o no está en el PATH${NC}"
    echo -e "${YELLOW}Instalando KICS...${NC}"

    # Verificar si el script de instalación existe
    if [ -f "./scripts/install_kics.sh" ]; then
        bash ./scripts/install_kics.sh
    else
        echo -e "${RED}No se encontró el script de instalación de KICS${NC}"
        echo -e "${YELLOW}Instalando KICS desde el repositorio oficial...${NC}"
        curl -sfL 'https://raw.githubusercontent.com/Checkmarx/kics/master/install.sh' | sh
    fi

    # Verificar nuevamente si KICS está instalado
    if ! command -v kics &> /dev/null; then
        echo -e "${RED}No se pudo instalar KICS. Por favor, instálelo manualmente.${NC}"
        exit 1
    fi
fi

# Crear directorio para informes si no existe
mkdir -p security-reports

# Ejecutar KICS
echo -e "${YELLOW}Ejecutando escaneo de seguridad con KICS...${NC}"
kics scan -p . --config .kics.config -o security-reports
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Escaneo de KICS completado sin problemas críticos${NC}"
else
    echo -e "${RED}Escaneo de KICS completado con problemas${NC}"
    echo -e "${YELLOW}Revise los informes en el directorio 'security-reports'${NC}"
fi

# Verificar archivos de seguridad
echo
echo -e "${YELLOW}Verificando archivos de seguridad requeridos...${NC}"

required_files=(
    "SECURITY.md"
    "CODE_OF_CONDUCT.md"
    ".github/CONTRIBUTING.md"
    ".github/PULL_REQUEST_TEMPLATE.md"
    ".github/ISSUE_TEMPLATE/security_issue.md"
    ".github/workflows/codeql-analysis.yml"
    ".github/dependabot.yml"
    ".github/workflows/secret-scanning.yml"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    echo -e "${RED}Faltan los siguientes archivos de seguridad:${NC}"
    for file in "${missing_files[@]}"; do
        echo -e "${RED}  - $file${NC}"
    done
else
    echo -e "${GREEN}Todos los archivos de seguridad requeridos están presentes${NC}"
fi

# Verificar encabezados de seguridad en nginx
echo
echo -e "${YELLOW}Verificando encabezados de seguridad en nginx...${NC}"

nginx_conf="nginx/conf.d/default.conf"
if [ -f "$nginx_conf" ]; then
    required_headers=(
        "Strict-Transport-Security"
        "X-Content-Type-Options"
        "X-Frame-Options"
        "Content-Security-Policy"
    )

    missing_headers=()
    for header in "${required_headers[@]}"; do
        if ! grep -q "add_header\s\+$header" "$nginx_conf"; then
            missing_headers+=("$header")
        fi
    done

    if [ ${#missing_headers[@]} -gt 0 ]; then
        echo -e "${RED}Faltan los siguientes encabezados de seguridad en nginx:${NC}"
        for header in "${missing_headers[@]}"; do
            echo -e "${RED}  - $header${NC}"
        done
    else
        echo -e "${GREEN}Todos los encabezados de seguridad requeridos están presentes en nginx${NC}"
    fi
else
    echo -e "${YELLOW}No se encontró el archivo de configuración de nginx: $nginx_conf${NC}"
fi

echo
echo -e "${YELLOW}Verificación de seguridad completada${NC}"
echo -e "${YELLOW}Revise los informes en el directorio 'security-reports' para más detalles${NC}"
