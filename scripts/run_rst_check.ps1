# Script para verificar archivos RST en el proyecto
# Uso: .\scripts\run_rst_check.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando archivos RST en el proyecto CALLi..." -ForegroundColor $Cyan

# Verificar si docutils está instalado
$docutilsInstalled = $null
try {
    $docutilsInstalled = python -c "import docutils" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $docutilsInstalled = $null
    }
} catch {
    $docutilsInstalled = $null
}

if (-not $docutilsInstalled) {
    Write-Host "docutils no está instalado. Instalando..." -ForegroundColor $Yellow
    pip install docutils
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error al instalar docutils. Por favor, instálelo manualmente con 'pip install docutils'" -ForegroundColor $Red
        exit 1
    }
}

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Ejecutar el script de verificación de RST
Write-Host "Ejecutando verificación de archivos RST..." -ForegroundColor $Yellow
python scripts\check_rst.py --directory backend-call-automation\docs --output reports\rst_report.txt
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Verificación completada con éxito. No se encontraron problemas en los archivos RST." -ForegroundColor $Green
} else {
    Write-Host "Se encontraron problemas en los archivos RST. Consulte reports\rst_report.txt para más detalles." -ForegroundColor $Yellow
}

exit $exitCode
