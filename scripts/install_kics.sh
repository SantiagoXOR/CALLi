#!/bin/bash
# Script para instalar KICS (Keeping Infrastructure as Code Secure)

# Determinar la arquitectura del sistema
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    ARCH="amd64"
elif [ "$ARCH" = "aarch64" ]; then
    ARCH="arm64"
else
    echo "Arquitectura no soportada: $ARCH"
    exit 1
fi

# Determinar el sistema operativo
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
if [ "$OS" = "darwin" ]; then
    OS="darwin"
elif [ "$OS" = "linux" ]; then
    OS="linux"
elif [[ "$OS" == *"mingw"* ]] || [[ "$OS" == *"cygwin"* ]] || [[ "$OS" == *"msys"* ]]; then
    OS="windows"
    EXT=".exe"
else
    echo "Sistema operativo no soportado: $OS"
    exit 1
fi

# Versión de KICS a instalar
KICS_VERSION="1.6.1"

# URL de descarga
DOWNLOAD_URL="https://github.com/Checkmarx/kics/releases/download/v${KICS_VERSION}/kics_${KICS_VERSION}_${OS}_${ARCH}${EXT:-}"

# Directorio de instalación
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Descargar KICS
echo "Descargando KICS desde $DOWNLOAD_URL..."
if [ "$OS" = "windows" ]; then
    curl -L "$DOWNLOAD_URL" -o "$INSTALL_DIR/kics.exe"
    chmod +x "$INSTALL_DIR/kics.exe"
else
    curl -L "$DOWNLOAD_URL" -o "$INSTALL_DIR/kics"
    chmod +x "$INSTALL_DIR/kics"
fi

# Verificar la instalación
if [ -f "$INSTALL_DIR/kics${EXT:-}" ]; then
    echo "KICS instalado correctamente en $INSTALL_DIR/kics${EXT:-}"
    echo "Asegúrate de que $INSTALL_DIR esté en tu PATH"
    
    # Agregar al PATH si no está
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo "Agregando $INSTALL_DIR a PATH"
        if [ "$OS" = "windows" ]; then
            echo "Ejecuta: setx PATH \"%PATH%;$INSTALL_DIR\""
        else
            echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> ~/.bashrc
            echo "Reinicia tu terminal o ejecuta 'source ~/.bashrc'"
        fi
    fi
    
    # Verificar versión
    "$INSTALL_DIR/kics${EXT:-}" version
else
    echo "Error al instalar KICS"
    exit 1
fi
