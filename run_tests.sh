#!/bin/bash
# Script para ejecutar los tests con el PYTHONPATH configurado correctamente

# Configurar PYTHONPATH para incluir el directorio raíz y backend-call-automation
export PYTHONPATH="$PWD:$PWD/backend-call-automation"
echo "PYTHONPATH configurado: $PYTHONPATH"

# Ejecutar los tests
cd backend-call-automation
python -m pytest tests -v

# Volver al directorio original
cd ..
