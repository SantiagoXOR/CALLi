@echo off
REM Script para ejecutar los tests con el PYTHONPATH configurado correctamente

REM Configurar PYTHONPATH para incluir el directorio raíz y backend-call-automation
set "PYTHONPATH=%CD%;%CD%\backend-call-automation"
echo PYTHONPATH configurado: %PYTHONPATH%

REM Ejecutar los tests
cd backend-call-automation
python -m pytest tests -v

REM Volver al directorio original
cd ..
