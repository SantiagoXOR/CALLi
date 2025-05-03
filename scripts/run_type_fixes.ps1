# Script para ejecutar correcciones automáticas de errores de tipo
# Uso: .\scripts\run_type_fixes.ps1 [--dry-run]

param (
    [switch]$dryRun = $false
)

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Ejecutando correcciones automáticas de errores de tipo en el proyecto CALLi..." -ForegroundColor $Cyan

# Verificar si el script fix_type_annotations.py existe
if (-not (Test-Path "scripts\fix_type_annotations.py")) {
    Write-Host "Error: No se encontró el script fix_type_annotations.py" -ForegroundColor $Red
    exit 1
}

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Ejecutar el script de corrección de tipos
$dryRunFlag = if ($dryRun) { "--dry-run" } else { "" }
$command = "python scripts\fix_type_annotations.py --directory backend-call-automation $dryRunFlag"

Write-Host "Ejecutando: $command" -ForegroundColor $Yellow
Invoke-Expression $command
$exitCode = $LASTEXITCODE

# Mostrar resumen
if ($exitCode -eq 0) {
    if ($dryRun) {
        Write-Host "Simulación completada. No se realizaron cambios reales." -ForegroundColor $Green
        Write-Host "Ejecute este script sin el parámetro -dryRun para aplicar las correcciones:" -ForegroundColor $Yellow
        Write-Host "  .\scripts\run_type_fixes.ps1" -ForegroundColor $Yellow
    } else {
        Write-Host "Correcciones de tipo aplicadas con éxito." -ForegroundColor $Green
    }
} else {
    Write-Host "Se encontraron problemas al aplicar las correcciones de tipo." -ForegroundColor $Red
}

# Ejecutar MyPy para verificar si quedan errores
Write-Host "`nEjecutando MyPy para verificar errores restantes..." -ForegroundColor $Yellow
& .\scripts\run_mypy.ps1
$mypyExitCode = $LASTEXITCODE

if ($mypyExitCode -eq 0) {
    Write-Host "No se encontraron errores de tipo restantes." -ForegroundColor $Green
} else {
    Write-Host "Aún quedan errores de tipo. Consulte reports\mypy_report.txt para más detalles." -ForegroundColor $Yellow

    # Contar errores por categoría
    $report = Get-Content reports\mypy_report.txt
    $errorCount = $report.Count
    $annotationMissing = ($report | Select-String "Missing type annotation").Count
    $incompatibleType = ($report | Select-String "Incompatible type").Count
    $nameError = ($report | Select-String "Name").Count
    $unionAttr = ($report | Select-String "union-attr").Count
    $returnValue = ($report | Select-String "return-value").Count

    Write-Host "Resumen de errores restantes:" -ForegroundColor $Yellow
    Write-Host "- Total de errores: $errorCount" -ForegroundColor $Yellow
    Write-Host "- Anotaciones faltantes: $annotationMissing" -ForegroundColor $Yellow
    Write-Host "- Tipos incompatibles: $incompatibleType" -ForegroundColor $Yellow
    Write-Host "- Errores de nombres: $nameError" -ForegroundColor $Yellow
    Write-Host "- Errores de atributos en uniones: $unionAttr" -ForegroundColor $Yellow
    Write-Host "- Errores de valor de retorno: $returnValue" -ForegroundColor $Yellow

    Write-Host "`nPara corregir estos errores manualmente:" -ForegroundColor $Yellow
    Write-Host "1. Revise reports\mypy_report.txt para ver los detalles de cada error" -ForegroundColor $Yellow
    Write-Host "2. Corrija los errores en los archivos correspondientes" -ForegroundColor $Yellow
    Write-Host "3. Ejecute .\scripts\run_mypy.ps1 para verificar que los errores se han corregido" -ForegroundColor $Yellow
}

exit $exitCode
