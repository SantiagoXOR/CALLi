# Script para verificar docstrings en el proyecto
# Uso: .\scripts\run_docstring_check.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando docstrings en el proyecto CALLi..." -ForegroundColor $Cyan

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Ejecutar el script de verificación de docstrings
Write-Host "Ejecutando verificación de docstrings..." -ForegroundColor $Yellow
python scripts\check_docstrings.py --directory backend-call-automation --output reports\docstrings_report.txt
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Verificación completada con éxito. No se encontraron problemas de documentación." -ForegroundColor $Green
} else {
    Write-Host "Se encontraron elementos sin docstrings. Consulte reports\docstrings_report.txt para más detalles." -ForegroundColor $Yellow
}

exit $exitCode
