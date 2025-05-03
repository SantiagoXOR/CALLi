# Script para instalar KICS (Keeping Infrastructure as Code Secure) en Windows
# Uso: .\scripts\install_kics.ps1

# Versión de KICS a instalar
$KICS_VERSION = "1.6.1"

# Determinar la arquitectura del sistema
$ARCH = "amd64"
if ([Environment]::Is64BitOperatingSystem -eq $false) {
    $ARCH = "386"
}

# URL de descarga para Windows
$DOWNLOAD_URL = "https://github.com/Checkmarx/kics/releases/download/v${KICS_VERSION}/kics_${KICS_VERSION}_windows_${ARCH}.zip"

# Directorio de instalación
$INSTALL_DIR = "$env:USERPROFILE\.kics"
if (-not (Test-Path $INSTALL_DIR)) {
    New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
}

# Archivo temporal para la descarga
$TEMP_FILE = "$env:TEMP\kics.zip"

Write-Host "Descargando KICS desde $DOWNLOAD_URL..."
try {
    Invoke-WebRequest -Uri $DOWNLOAD_URL -OutFile $TEMP_FILE
} catch {
    Write-Host "Error al descargar KICS: $_" -ForegroundColor Red
    exit 1
}

# Verificar que el archivo se descargó correctamente
if (-not (Test-Path $TEMP_FILE)) {
    Write-Host "Error: No se pudo descargar KICS" -ForegroundColor Red
    exit 1
}

# Extraer el archivo ZIP
Write-Host "Extrayendo KICS..."
try {
    Expand-Archive -Path $TEMP_FILE -DestinationPath $INSTALL_DIR -Force
} catch {
    Write-Host "Error al extraer KICS: $_" -ForegroundColor Red
    exit 1
}

# Verificar que el ejecutable existe
if (-not (Test-Path "$INSTALL_DIR\kics.exe")) {
    Write-Host "Error: No se encontró el ejecutable de KICS después de la extracción" -ForegroundColor Red
    exit 1
}

# Agregar al PATH si no está
$USER_PATH = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not $USER_PATH.Contains($INSTALL_DIR)) {
    Write-Host "Agregando KICS al PATH del usuario..."
    [Environment]::SetEnvironmentVariable("PATH", "$USER_PATH;$INSTALL_DIR", "User")
    $env:PATH = "$env:PATH;$INSTALL_DIR"
}

# Limpiar archivos temporales
Remove-Item $TEMP_FILE -Force

# Verificar la instalación
try {
    $KICS_VERSION_OUTPUT = & "$INSTALL_DIR\kics.exe" version
    Write-Host "KICS instalado correctamente:" -ForegroundColor Green
    Write-Host $KICS_VERSION_OUTPUT
    Write-Host "Ubicación: $INSTALL_DIR\kics.exe"
} catch {
    Write-Host "Error al verificar la instalación de KICS: $_" -ForegroundColor Red
    exit 1
}

Write-Host "Para usar KICS, reinicie su terminal o ejecute: `$env:PATH = `"`$env:PATH;$INSTALL_DIR`"" -ForegroundColor Yellow
