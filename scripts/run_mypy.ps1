# Script para ejecutar MyPy en todo el proyecto
# Uso: .\scripts\run_mypy.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Ejecutando MyPy en el proyecto CALLi..." -ForegroundColor $Cyan

# Verificar si mypy está instalado
$mypyInstalled = $null
try {
    $mypyInstalled = mypy --version 2>$null
}
catch {
    $mypyInstalled = $null
}

if (-not $mypyInstalled) {
    Write-Host "MyPy no está instalado. Instalando..." -ForegroundColor $Yellow
    pip install mypy
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al instalar MyPy. Por favor, instálelo manualmente con 'pip install mypy'" -ForegroundColor $Red
        exit 1
    }
}

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Ejecutar MyPy en el backend con las opciones correctas para resolver el problema de módulos duplicados
Write-Host "Ejecutando MyPy en el backend..." -ForegroundColor $Yellow
mypy --follow-imports=skip --namespace-packages --explicit-package-bases backend-call-automation > reports\mypy_report.txt
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "MyPy completado con éxito. No se encontraron problemas de tipos." -ForegroundColor $Green
}
else {
    Write-Host "MyPy encontró problemas de tipos. Consulte reports\mypy_report.txt para más detalles." -ForegroundColor $Yellow

    # Contar errores por categoría
    $report = Get-Content reports\mypy_report.txt
    $errorCount = $report.Count
    $annotationMissing = ($report | Select-String "Missing type annotation").Count
    $incompatibleType = ($report | Select-String "Incompatible type").Count
    $nameError = ($report | Select-String "Name").Count

    Write-Host "Resumen de errores:" -ForegroundColor $Yellow
    Write-Host "- Total de errores: $errorCount" -ForegroundColor $Yellow
    Write-Host "- Anotaciones faltantes: $annotationMissing" -ForegroundColor $Yellow
    Write-Host "- Tipos incompatibles: $incompatibleType" -ForegroundColor $Yellow
    Write-Host "- Errores de nombres: $nameError" -ForegroundColor $Yellow
}

exit $exitCode
