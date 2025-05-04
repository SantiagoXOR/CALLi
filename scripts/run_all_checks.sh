#!/bin/bash

# Script maestro para ejecutar todas las verificaciones de seguridad
# Uso: ./scripts/run_all_checks.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Ejecutando todas las verificaciones de seguridad...${NC}"

# Crear directorio para informes
mkdir -p reports

# Función para ejecutar un script y mostrar su resultado
run_script() {
    local script_name=$1
    local description=$2
    shift 2
    local arguments=("$@")

    echo
    echo -e "${CYAN}=== $description ===${NC}"

    "$script_name" "${arguments[@]}"
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✓ $description completado con éxito${NC}"
    else
        echo -e "${RED}✗ $description completado con errores${NC}"
    fi

    return $exit_code
}

# Verificar Node.js
node_result=$(run_script "./scripts/check_nodejs.sh" "Verificación de Node.js")

# Ejecutar verificaciones
declare -A results

# Verificación de formato con Ruff
run_script "./scripts/run_ruff.sh" "Verificación de formato con Ruff"
results["Verificación de formato con Ruff"]=$?

# Verificación de tipos con MyPy
run_script "./scripts/run_mypy.sh" "Verificación de tipos con MyPy"
results["Verificación de tipos con MyPy"]=$?

# Verificación de docstrings
run_script "./scripts/run_docstring_check.sh" "Verificación de docstrings"
results["Verificación de docstrings"]=$?

# Verificación de documentación RST
run_script "./scripts/run_rst_check.sh" "Verificación de documentación RST"
results["Verificación de documentación RST"]=$?

# Verificar dependencias JavaScript solo si Node.js está instalado
if command -v node &> /dev/null && command -v npm &> /dev/null; then
    run_script "./scripts/check_js_dependencies.sh" "Verificación de dependencias JavaScript"
    results["Verificación de dependencias JavaScript"]=$?
fi

# Ejecutar verificación de seguridad
run_script "python" "Verificación de seguridad" "scripts/security_check_local.py"
results["Verificación de seguridad"]=$?

# Revisar falsos positivos
run_script "./scripts/run_false_positives_review.sh" "Revisión de falsos positivos"
results["Revisión de falsos positivos"]=$?

# Generar informe final
echo
echo -e "${CYAN}=== Resumen de Verificaciones ===${NC}"
echo

all_passed=true
for name in "${!results[@]}"; do
    if [ ${results[$name]} -eq 0 ]; then
        echo -e "${GREEN}✓ $name: Éxito${NC}"
    else
        echo -e "${RED}✗ $name: Error${NC}"
        all_passed=false
    fi
done

echo
if $all_passed; then
    echo -e "${GREEN}✓ Todas las verificaciones completadas con éxito${NC}"
else
    echo -e "${RED}✗ Algunas verificaciones fallaron. Revise los informes para más detalles.${NC}"
fi

# Generar informe en Markdown
cat > "reports/verification_summary.md" << EOF
# Informe de Verificaciones de Seguridad

## Resumen

Fecha: $(date '+%Y-%m-%d %H:%M:%S')

| Verificación | Resultado |
|--------------|-----------|
EOF

for name in "${!results[@]}"; do
    if [ ${results[$name]} -eq 0 ]; then
        status="✅ Éxito"
    else
        status="❌ Error"
    fi
    echo "| $name | $status |" >> "reports/verification_summary.md"
done

cat >> "reports/verification_summary.md" << EOF

## Detalles

Para ver los detalles de cada verificación, consulte los informes individuales en el directorio \`reports/\`.

## Próximos Pasos

EOF

if $all_passed; then
    cat >> "reports/verification_summary.md" << EOF
- Continuar con el desarrollo normal
- Considerar implementar pruebas adicionales
- Revisar periódicamente las dependencias para mantenerlas actualizadas
EOF
else
    cat >> "reports/verification_summary.md" << EOF
- Corregir los problemas identificados en los informes
- Volver a ejecutar las verificaciones para confirmar que los problemas se han resuelto
- Considerar automatizar estas verificaciones en el flujo de trabajo de CI/CD
EOF
fi

echo -e "${CYAN}Informe guardado en reports/verification_summary.md${NC}"

# Devolver código de salida
if $all_passed; then
    exit 0
else
    exit 1
fi
