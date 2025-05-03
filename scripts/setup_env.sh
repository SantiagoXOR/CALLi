#!/bin/bash
# Script para configurar el entorno de desarrollo en Linux/macOS

# Obtener el directorio raíz del proyecto
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Configurar PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT:$PROJECT_ROOT/backend-call-automation"
echo "PYTHONPATH configurado: $PYTHONPATH"

# Verificar si existe el archivo .env
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    if [ -f "$PROJECT_ROOT/.env.example" ]; then
        echo "Archivo .env no encontrado. Creando desde .env.example..."
        cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
        echo "Por favor, edita el archivo .env con tus configuraciones específicas."
    else
        echo "ADVERTENCIA: No se encontró ni .env ni .env.example. Crea un archivo .env manualmente."
    fi
fi

# Verificar entorno virtual
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Entorno virtual no encontrado. ¿Deseas crear uno? (s/n)"
    read -r create_venv
    if [ "$create_venv" = "s" ] || [ "$create_venv" = "S" ]; then
        echo "Creando entorno virtual..."
        python3 -m venv "$PROJECT_ROOT/venv"
        echo "Entorno virtual creado. Activalo con: source venv/bin/activate"
    fi
fi

# Verificar si el entorno virtual está activado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "ADVERTENCIA: El entorno virtual no está activado."
    echo "Actívalo con: source venv/bin/activate"
else
    echo "Entorno virtual activado: $VIRTUAL_ENV"
fi

# Verificar dependencias
if [ -f "$PROJECT_ROOT/backend-call-automation/requirements.txt" ]; then
    echo "¿Deseas instalar/actualizar las dependencias? (s/n)"
    read -r install_deps
    if [ "$install_deps" = "s" ] || [ "$install_deps" = "S" ]; then
        echo "Instalando dependencias..."
        pip install -r "$PROJECT_ROOT/backend-call-automation/requirements.txt"
        echo "Dependencias instaladas."
    fi
else
    echo "ADVERTENCIA: No se encontró el archivo requirements.txt."
fi

# Instalar el paquete en modo desarrollo
echo "¿Deseas instalar el paquete en modo desarrollo? (s/n)"
read -r install_dev
if [ "$install_dev" = "s" ] || [ "$install_dev" = "S" ]; then
    echo "Instalando paquete en modo desarrollo..."
    pip install -e "$PROJECT_ROOT/backend-call-automation"
    echo "Paquete instalado en modo desarrollo."
fi

echo "Configuración del entorno completada."
echo "Para ejecutar la aplicación: cd backend-call-automation && uvicorn app.main:app --reload"
echo "Para ejecutar las pruebas: cd backend-call-automation && python -m pytest tests/"
