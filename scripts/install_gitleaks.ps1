# Script para instalar gitleaks en Windows
# Uso: .\scripts\install_gitleaks.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Instalando gitleaks..." -ForegroundColor $Cyan

# Verificar si gitleaks ya está instalado
try {
    $gitleaksVersion = gitleaks version
    Write-Host "gitleaks ya está instalado: $gitleaksVersion" -ForegroundColor $Green
    exit 0
} catch {
    Write-Host "gitleaks no está instalado. Procediendo con la instalación..." -ForegroundColor $Yellow
}

# Crear directorio temporal
$tempDir = Join-Path $env:TEMP "gitleaks_install"
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir | Out-Null
}

# Descargar la última versión de gitleaks
$version = "8.18.1"
$url = "https://github.com/gitleaks/gitleaks/releases/download/v$version/gitleaks_$($version)_windows_x64.zip"
$zipFile = Join-Path $tempDir "gitleaks.zip"

try {
    Write-Host "Descargando gitleaks v$version..." -ForegroundColor $Yellow
    Invoke-WebRequest -Uri $url -OutFile $zipFile
} catch {
    Write-Host "Error al descargar gitleaks: $_" -ForegroundColor $Red
    exit 1
}

# Extraer el archivo ZIP
try {
    Write-Host "Extrayendo archivos..." -ForegroundColor $Yellow
    Expand-Archive -Path $zipFile -DestinationPath $tempDir -Force
} catch {
    Write-Host "Error al extraer el archivo ZIP: $_" -ForegroundColor $Red
    exit 1
}

# Crear directorio para binarios si no existe
$binDir = Join-Path $env:USERPROFILE ".local\bin"
if (-not (Test-Path $binDir)) {
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
}

# Mover el ejecutable al directorio de binarios
try {
    $gitleaksExe = Join-Path $tempDir "gitleaks.exe"
    $destPath = Join-Path $binDir "gitleaks.exe"
    Copy-Item -Path $gitleaksExe -Destination $destPath -Force
    Write-Host "gitleaks instalado en $destPath" -ForegroundColor $Green
} catch {
    Write-Host "Error al mover el ejecutable: $_" -ForegroundColor $Red
    exit 1
}

# Agregar el directorio al PATH si no está ya
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (-not $currentPath.Contains($binDir)) {
    try {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$binDir", "User")
        Write-Host "Directorio $binDir agregado al PATH" -ForegroundColor $Green
        Write-Host "IMPORTANTE: Es posible que necesites reiniciar tu terminal para que los cambios surtan efecto." -ForegroundColor $Yellow
    } catch {
        Write-Host "Error al agregar el directorio al PATH: $_" -ForegroundColor $Red
        Write-Host "Por favor, agrega manualmente $binDir a tu variable de entorno PATH." -ForegroundColor $Yellow
    }
}

# Limpiar archivos temporales
try {
    Remove-Item -Path $tempDir -Recurse -Force
    Write-Host "Archivos temporales eliminados" -ForegroundColor $Green
} catch {
    Write-Host "Error al eliminar archivos temporales: $_" -ForegroundColor $Red
}

Write-Host "Instalación de gitleaks completada. Reinicia tu terminal para usar gitleaks." -ForegroundColor $Green
