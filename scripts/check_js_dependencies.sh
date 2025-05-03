#!/bin/bash

# Script para verificar dependencias JavaScript
# Uso: ./scripts/check_js_dependencies.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Verificando dependencias JavaScript...${NC}"

# Verificar si Node.js está instalado
if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
    echo -e "${RED}Node.js no está instalado o no está en el PATH.${NC}"
    echo -e "${YELLOW}Por favor, ejecute ./scripts/check_nodejs.sh para instalar Node.js${NC}"
    exit 1
fi

# Crear directorio para informes
mkdir -p reports

# Verificar si existe el directorio frontend-call-automation
if [ ! -d "frontend-call-automation" ]; then
    echo -e "${RED}No se encontró el directorio frontend-call-automation${NC}"
    exit 1
fi

# Verificar si existe package.json
if [ ! -f "frontend-call-automation/package.json" ]; then
    echo -e "${RED}No se encontró el archivo package.json en frontend-call-automation${NC}"
    exit 1
fi

# Ejecutar npm audit
echo -e "${YELLOW}Ejecutando npm audit...${NC}"
CURRENT_DIR=$(pwd)
cd frontend-call-automation

# Ejecutar npm audit y guardar la salida
NPM_OUTPUT=$(npm audit --json 2>&1)
NPM_EXIT_CODE=$?

# Guardar la salida en un archivo
echo "$NPM_OUTPUT" > "../reports/npm_audit.json"

# Contar vulnerabilidades por severidad
CRITICAL_COUNT=$(echo "$NPM_OUTPUT" | grep -o '"severity":"critical"' | wc -l)
HIGH_COUNT=$(echo "$NPM_OUTPUT" | grep -o '"severity":"high"' | wc -l)
MODERATE_COUNT=$(echo "$NPM_OUTPUT" | grep -o '"severity":"moderate"' | wc -l)
LOW_COUNT=$(echo "$NPM_OUTPUT" | grep -o '"severity":"low"' | wc -l)
INFO_COUNT=$(echo "$NPM_OUTPUT" | grep -o '"severity":"info"' | wc -l)

# Mostrar resumen
echo -e "${YELLOW}Resumen de vulnerabilidades:${NC}"
if [ $CRITICAL_COUNT -gt 0 ]; then
    echo -e "${RED}- Críticas: $CRITICAL_COUNT${NC}"
else
    echo -e "${GREEN}- Críticas: $CRITICAL_COUNT${NC}"
fi

if [ $HIGH_COUNT -gt 0 ]; then
    echo -e "${RED}- Altas: $HIGH_COUNT${NC}"
else
    echo -e "${GREEN}- Altas: $HIGH_COUNT${NC}"
fi

if [ $MODERATE_COUNT -gt 0 ]; then
    echo -e "${YELLOW}- Moderadas: $MODERATE_COUNT${NC}"
else
    echo -e "${GREEN}- Moderadas: $MODERATE_COUNT${NC}"
fi

if [ $LOW_COUNT -gt 0 ]; then
    echo -e "${YELLOW}- Bajas: $LOW_COUNT${NC}"
else
    echo -e "${GREEN}- Bajas: $LOW_COUNT${NC}"
fi

echo -e "${GREEN}- Informativas: $INFO_COUNT${NC}"

# Generar informe en formato legible
cat > "../reports/npm_audit_report.md" << EOF
# Informe de Seguridad de Dependencias JavaScript

## Resumen

- **Críticas**: $CRITICAL_COUNT
- **Altas**: $HIGH_COUNT
- **Moderadas**: $MODERATE_COUNT
- **Bajas**: $LOW_COUNT
- **Informativas**: $INFO_COUNT

## Detalles

Para ver los detalles completos, ejecute:
\`\`\`
cd frontend-call-automation && npm audit
\`\`\`
EOF

# Determinar el código de salida basado en la presencia de vulnerabilidades críticas o altas
if [ $CRITICAL_COUNT -gt 0 ] || [ $HIGH_COUNT -gt 0 ]; then
    echo -e "${RED}Se encontraron vulnerabilidades críticas o altas. Por favor, actualice las dependencias.${NC}"
    EXIT_CODE=1
else
    echo -e "${GREEN}No se encontraron vulnerabilidades críticas o altas.${NC}"
    EXIT_CODE=0
fi

# Volver al directorio original
cd "$CURRENT_DIR"

# Sugerir soluciones
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${YELLOW}Recomendaciones:${NC}"
    echo -e "${YELLOW}1. Ejecute 'cd frontend-call-automation && npm audit fix' para intentar corregir automáticamente las vulnerabilidades${NC}"
    echo -e "${YELLOW}2. Para vulnerabilidades que no se pueden corregir automáticamente, actualice manualmente las dependencias${NC}"
    echo -e "${YELLOW}3. Consulte reports/npm_audit_report.md para más detalles${NC}"
fi

exit $EXIT_CODE
