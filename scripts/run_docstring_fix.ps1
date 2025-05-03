# Script para verificar y corregir docstrings en el proyecto
# Uso: .\scripts\run_docstring_fix.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando y corrigiendo docstrings en el proyecto CALLi..." -ForegroundColor $Cyan

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Ejecutar el script de verificación y corrección de docstrings
Write-Host "Ejecutando verificación de docstrings..." -ForegroundColor $Yellow
python scripts\fix_docstrings.py --directory backend-call-automation --output reports\docstrings_fix_report.txt --fix
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Verificación completada con éxito. No se encontraron problemas de documentación." -ForegroundColor $Green
} else {
    Write-Host "Se encontraron elementos sin docstrings. Consulte reports\docstrings_fix_report.txt para más detalles y sugerencias de corrección." -ForegroundColor $Yellow
}

exit $exitCode
