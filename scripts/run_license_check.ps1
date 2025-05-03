# Script para verificar las licencias de las dependencias
# Uso: .\scripts\run_license_check.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando licencias de dependencias..." -ForegroundColor $Cyan

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Ejecutar el script de verificación de licencias
Write-Host "Ejecutando verificación de licencias..." -ForegroundColor $Yellow
python scripts\check_licenses.py > reports\license_report.txt
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Verificación completada con éxito. No se encontraron problemas de licencias." -ForegroundColor $Green
} else {
    Write-Host "Se encontraron problemas con las licencias. Consulte reports\license_report.txt para más detalles." -ForegroundColor $Yellow
}

exit $exitCode
