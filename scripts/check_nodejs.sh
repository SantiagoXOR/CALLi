#!/bin/bash

# Script para verificar si Node.js está instalado
# Uso: ./scripts/check_nodejs.sh

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Verificando instalación de Node.js...${NC}"

# Verificar si Node.js está instalado
NODE_VERSION=$(node --version 2>/dev/null)
NODE_EXIT_CODE=$?

NPM_VERSION=$(npm --version 2>/dev/null)
NPM_EXIT_CODE=$?

if [ $NODE_EXIT_CODE -eq 0 ] && [ $NPM_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}Node.js está instalado correctamente:${NC}"
    echo -e "${GREEN}- Node.js: $NODE_VERSION${NC}"
    echo -e "${GREEN}- npm: $NPM_VERSION${NC}"
    exit 0
else
    echo -e "${RED}Node.js no está instalado o no está en el PATH.${NC}"
    echo -e "${YELLOW}Por favor, instale Node.js siguiendo estos pasos:${NC}"

    # Detectar el sistema operativo
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        echo -e "${YELLOW}1. Instale Node.js usando Homebrew: brew install node${NC}"
        echo -e "${YELLOW}   O descargue el instalador desde https://nodejs.org/${NC}"
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Linux
        echo -e "${YELLOW}1. Instale Node.js usando su gestor de paquetes:${NC}"
        echo -e "${YELLOW}   - Ubuntu/Debian: sudo apt install nodejs npm${NC}"
        echo -e "${YELLOW}   - Fedora: sudo dnf install nodejs${NC}"
        echo -e "${YELLOW}   - Arch Linux: sudo pacman -S nodejs npm${NC}"
        echo -e "${YELLOW}   O use NVM (Node Version Manager): https://github.com/nvm-sh/nvm${NC}"
    else
        # Windows o desconocido
        echo -e "${YELLOW}1. Descargue el instalador de Node.js desde https://nodejs.org/${NC}"
    fi

    echo -e "${YELLOW}2. Reinicie su terminal después de la instalación${NC}"
    echo -e "${YELLOW}3. Verifique la instalación ejecutando 'node --version' y 'npm --version'${NC}"

    # Preguntar si desea abrir el sitio web de Node.js
    echo -e "${YELLOW}¿Desea abrir el sitio web de Node.js ahora? (s/n)${NC}"
    read -r open_website
    if [ "$open_website" = "s" ] || [ "$open_website" = "S" ]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open "https://nodejs.org/"
        elif command -v open &> /dev/null; then
            open "https://nodejs.org/"
        else
            echo -e "${YELLOW}Visite https://nodejs.org/ para descargar Node.js${NC}"
        fi
    fi

    exit 1
fi
