#!/bin/bash
# Script para ejecutar todas las verificaciones de seguridad
# Uso: ./scripts/run_security_checks.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}      Verificación de Seguridad Completa CALLi      ${NC}"
echo -e "${CYAN}====================================================${NC}"
echo

# Crear directorio para informes si no existe
mkdir -p security-reports

# 1. Verificar configuración de seguridad
echo -e "${CYAN}1. Verificando configuración de seguridad...${NC}"
if [ -f "./scripts/verify_config_security.sh" ]; then
    bash ./scripts/verify_config_security.sh
else
    echo -e "${RED}No se encontró el script de verificación de configuración${NC}"
    echo -e "${YELLOW}Ejecutando verificación de seguridad local alternativa...${NC}"
    if [ -f "./scripts/security_check_local.py" ]; then
        python ./scripts/security_check_local.py
    else
        echo -e "${RED}No se encontró ningún script de verificación de seguridad${NC}"
    fi
fi

# 2. Verificar dependencias de Python
echo
echo -e "${CYAN}2. Verificando dependencias de Python...${NC}"
requirements_file="backend-call-automation/requirements.txt"
if [ -f "$requirements_file" ]; then
    # Verificar si safety está instalado
    if ! python -m pip show safety &> /dev/null; then
        echo -e "${YELLOW}Instalando safety...${NC}"
        python -m pip install safety
    fi

    # Ejecutar safety check
    echo -e "${YELLOW}Ejecutando safety check...${NC}"
    safety_output=$(python -m safety check -r "$requirements_file" 2>&1)
    safety_exit_code=$?

    if [ $safety_exit_code -ne 0 ]; then
        echo -e "${RED}Se encontraron vulnerabilidades en dependencias Python:${NC}"
        echo "$safety_output"
    else
        echo -e "${GREEN}No se encontraron vulnerabilidades en dependencias Python${NC}"
    fi

    # Guardar resultados
    echo "$safety_output" > security-reports/python-dependencies.txt
else
    echo -e "${YELLOW}No se encontró el archivo de requisitos de Python: $requirements_file${NC}"
fi

# 3. Verificar dependencias de JavaScript
echo
echo -e "${CYAN}3. Verificando dependencias de JavaScript...${NC}"
package_json_file="frontend-call-automation/package.json"
if [ -f "$package_json_file" ]; then
    # Verificar si npm está instalado
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}npm no está instalado o no está en el PATH${NC}"
    else
        # Ejecutar npm audit
        echo -e "${YELLOW}Ejecutando npm audit...${NC}"
        current_dir=$(pwd)
        cd frontend-call-automation
        npm_output=$(npm audit --json 2>&1)
        npm_exit_code=$?
        cd "$current_dir"

        if [ $npm_exit_code -ne 0 ]; then
            # Intentar analizar el resultado JSON
            high_critical=$(echo "$npm_output" | grep -o '"severity":"high\|critical"' | wc -l)

            if [ $high_critical -gt 0 ]; then
                echo -e "${RED}Se encontraron $high_critical vulnerabilidades de alta o crítica severidad${NC}"
            else
                echo -e "${YELLOW}Se encontraron vulnerabilidades de baja severidad${NC}"
            fi
        else
            echo -e "${GREEN}No se encontraron vulnerabilidades en dependencias JavaScript${NC}"
        fi

        # Guardar resultados
        echo "$npm_output" > security-reports/js-dependencies.json
    fi
else
    echo -e "${YELLOW}No se encontró el archivo package.json: $package_json_file${NC}"
fi

# 4. Buscar secretos en el código
echo
echo -e "${CYAN}4. Buscando secretos en el código...${NC}"
if [ -f "./scripts/improved_security_utils.py" ]; then
    secrets_output=$(python -c "from scripts.improved_security_utils import find_secrets; status, secrets = find_secrets(); print(f'Secretos encontrados: {len(secrets)}'); [print(s) for s in secrets[:10]]; print(f'... y {len(secrets) - 10} más') if len(secrets) > 10 else None" 2>&1)

    if echo "$secrets_output" | grep -q "Secretos encontrados: 0"; then
        echo -e "${GREEN}No se encontraron secretos en el código${NC}"
    else
        echo -e "${RED}Se encontraron posibles secretos en el código:${NC}"
        echo "$secrets_output"
    fi
else
    echo -e "${YELLOW}No se encontró el módulo mejorado de seguridad${NC}"
    echo -e "${YELLOW}Ejecutando verificación de secretos alternativa...${NC}"
    python ./scripts/security_check_local.py
fi

# 5. Verificar encabezados de seguridad
echo
echo -e "${CYAN}5. Verificando encabezados de seguridad...${NC}"
nginx_conf="nginx/conf.d/default.conf"
if [ -f "$nginx_conf" ]; then
    content=$(cat "$nginx_conf")

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

# Resumen final
echo
echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}            Resumen de Verificaciones              ${NC}"
echo -e "${CYAN}====================================================${NC}"
echo -e "${YELLOW}Los informes detallados se han guardado en el directorio 'security-reports'${NC}"
echo -e "${YELLOW}Para una verificación más completa, ejecute los siguientes comandos:${NC}"
echo -e "${YELLOW}  - python ./scripts/security_check_local.py${NC}"
echo -e "${YELLOW}  - bash ./scripts/verify_config_security.sh${NC}"
echo -e "${YELLOW}  - python ./scripts/improved_security_utils.py${NC}"
echo
echo -e "${CYAN}Verificación de seguridad completada${NC}"
