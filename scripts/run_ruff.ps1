# Script para ejecutar Ruff en todo el proyecto
# Uso: .\scripts\run_ruff.ps1 [--fix]

param (
    [switch]$fix = $false
)

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Ejecutando Ruff en el proyecto CALLi..." -ForegroundColor $Cyan

# Verificar si ruff está instalado
$ruffInstalled = $null
try {
    $ruffInstalled = ruff --version 2>$null
} catch {
    $ruffInstalled = $null
}

if (-not $ruffInstalled) {
    Write-Host "Ruff no está instalado. Instalando..." -ForegroundColor $Yellow
    pip install ruff
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al instalar Ruff. Por favor, instálelo manualmente con 'pip install ruff'" -ForegroundColor $Red
        exit 1
    }
}

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Ejecutar Ruff
if ($fix) {
    Write-Host "Ejecutando Ruff con corrección automática..." -ForegroundColor $Yellow
    ruff check --fix .
    $exitCode = $LASTEXITCODE

    # Ejecutar el formateador de Ruff
    Write-Host "Ejecutando el formateador de Ruff..." -ForegroundColor $Yellow
    ruff format .
    $formatExitCode = $LASTEXITCODE

    if ($exitCode -eq 0 -and $formatExitCode -eq 0) {
        Write-Host "Ruff completado con éxito. Se han corregido los problemas de formato." -ForegroundColor $Green
    } else {
        Write-Host "Ruff completado con errores. Algunos problemas pueden requerir corrección manual." -ForegroundColor $Yellow
    }
} else {
    Write-Host "Ejecutando Ruff en modo verificación..." -ForegroundColor $Yellow
    ruff check . > reports\ruff_report.txt
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host "Ruff completado con éxito. No se encontraron problemas de formato." -ForegroundColor $Green
    } else {
        Write-Host "Ruff encontró problemas de formato. Consulte reports\ruff_report.txt para más detalles." -ForegroundColor $Yellow
        Write-Host "Para corregir automáticamente los problemas, ejecute .\scripts\run_ruff.ps1 --fix" -ForegroundColor $Yellow
    }
}

exit $exitCode
