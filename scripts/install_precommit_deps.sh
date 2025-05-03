#!/bin/bash

# Script para instalar pre-commit y sus dependencias
# Uso: ./scripts/install_precommit_deps.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Instalando pre-commit y dependencias para el proyecto CALLi...${NC}"
echo -e "${CYAN}============================================================${NC}"

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo -e "${RED}Error: pip no está instalado o no está en el PATH.${NC}"
    echo -e "${RED}Por favor, instale Python y pip antes de continuar.${NC}"
    exit 1
fi

# Instalar pre-commit
echo -e "\n${YELLOW}Instalando pre-commit...${NC}"
pip install pre-commit
if [ $? -ne 0 ]; then
    echo -e "${RED}Error al instalar pre-commit.${NC}"
    exit 1
fi

# Instalar dependencias de Python para los hooks
echo -e "\n${YELLOW}Instalando dependencias de Python para los hooks...${NC}"
pip install mypy ruff bandit safety docutils restructuredtext-lint
if [ $? -ne 0 ]; then
    echo -e "${RED}Error al instalar dependencias de Python.${NC}"
    exit 1
fi

# Instalar gitleaks
echo -e "\n${YELLOW}Instalando gitleaks...${NC}"
./scripts/install_gitleaks.sh
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Error al instalar gitleaks. Continuando de todos modos...${NC}"
fi

# Instalar KICS
echo -e "\n${YELLOW}Instalando KICS...${NC}"
./scripts/install_kics.sh
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Error al instalar KICS. Continuando de todos modos...${NC}"
fi

# Instalar hooks de pre-commit
echo -e "\n${YELLOW}Instalando hooks de pre-commit...${NC}"
pre-commit install --install-hooks
if [ $? -ne 0 ]; then
    echo -e "${RED}Error al instalar hooks de pre-commit.${NC}"
    exit 1
fi

# Instalar hooks adicionales
echo -e "\n${YELLOW}Instalando hooks adicionales (pre-push)...${NC}"
pre-commit install --hook-type pre-push
if [ $? -ne 0 ]; then
    echo -e "${RED}Error al instalar hooks de pre-push.${NC}"
    exit 1
fi

# Ejecutar pre-commit en todos los archivos para verificar la instalación
echo -e "\n${YELLOW}Verificando la instalación de pre-commit...${NC}"
pre-commit run --all-files
PRECOMMIT_EXIT_CODE=$?

if [ $PRECOMMIT_EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}✓ Pre-commit instalado y configurado correctamente.${NC}"
else
    echo -e "\n${YELLOW}⚠ Pre-commit instalado, pero algunas verificaciones fallaron.${NC}"
    echo -e "${YELLOW}Esto es normal en la primera ejecución. Los problemas detectados deben corregirse antes de hacer commit.${NC}"
fi

echo -e "\n${CYAN}Para usar pre-commit:${NC}"
echo -e "${CYAN}1. Los hooks se ejecutarán automáticamente al hacer git commit${NC}"
echo -e "${CYAN}2. Para ejecutar manualmente: pre-commit run --all-files${NC}"
echo -e "${CYAN}3. Para omitir los hooks en un commit específico: git commit --no-verify${NC}"

exit 0
