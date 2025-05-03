@echo off
REM Script para configurar el entorno de desarrollo en Windows

REM Obtener el directorio raíz del proyecto
set "PROJECT_ROOT=%~dp0.."
cd %PROJECT_ROOT%

REM Configurar PYTHONPATH
set "PYTHONPATH=%PROJECT_ROOT%;%PROJECT_ROOT%\backend-call-automation"
echo PYTHONPATH configurado: %PYTHONPATH%

REM Verificar si existe el archivo .env
if not exist "%PROJECT_ROOT%\.env" (
    if exist "%PROJECT_ROOT%\.env.example" (
        echo Archivo .env no encontrado. Creando desde .env.example...
        copy "%PROJECT_ROOT%\.env.example" "%PROJECT_ROOT%\.env"
        echo Por favor, edita el archivo .env con tus configuraciones específicas.
    ) else (
        echo ADVERTENCIA: No se encontró ni .env ni .env.example. Crea un archivo .env manualmente.
    )
)

REM Verificar entorno virtual
if not exist "%PROJECT_ROOT%\venv" (
    echo Entorno virtual no encontrado. ¿Deseas crear uno? (s/n)
    set /p create_venv=
    if /i "%create_venv%"=="s" (
        echo Creando entorno virtual...
        python -m venv "%PROJECT_ROOT%\venv"
        echo Entorno virtual creado. Activalo con: venv\Scripts\activate
    )
)

REM Verificar si el entorno virtual está activado
if "%VIRTUAL_ENV%"=="" (
    echo ADVERTENCIA: El entorno virtual no está activado.
    echo Actívalo con: venv\Scripts\activate
) else (
    echo Entorno virtual activado: %VIRTUAL_ENV%
)

REM Verificar dependencias
if exist "%PROJECT_ROOT%\backend-call-automation\requirements.txt" (
    echo ¿Deseas instalar/actualizar las dependencias? (s/n)
    set /p install_deps=
    if /i "%install_deps%"=="s" (
        echo Instalando dependencias...
        pip install -r "%PROJECT_ROOT%\backend-call-automation\requirements.txt"
        echo Dependencias instaladas.
    )
) else (
    echo ADVERTENCIA: No se encontró el archivo requirements.txt.
)

REM Instalar el paquete en modo desarrollo
echo ¿Deseas instalar el paquete en modo desarrollo? (s/n)
set /p install_dev=
if /i "%install_dev%"=="s" (
    echo Instalando paquete en modo desarrollo...
    pip install -e "%PROJECT_ROOT%\backend-call-automation"
    echo Paquete instalado en modo desarrollo.
)

echo Configuración del entorno completada.
echo Para ejecutar la aplicación: cd backend-call-automation ^&^& uvicorn app.main:app --reload
echo Para ejecutar las pruebas: cd backend-call-automation ^&^& python -m pytest tests/

pause
