# Script para ejecutar la verificación de encabezados de seguridad
# Uso: .\scripts\run_security_headers_check.ps1 [--urls "https://example.com,https://example.org"]

param (
    [string]$urls = "https://localhost,https://localhost:443"
)

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando encabezados de seguridad HTTP..." -ForegroundColor $Cyan

# Crear directorio para el informe si no existe
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" -Force | Out-Null
}

# Ejecutar el script
$command = "python scripts\check_security_headers.py --urls=$urls --output=reports\security_headers_results.json --report=reports\security_headers_report.md"
Write-Host "Ejecutando: $command" -ForegroundColor $Yellow
Invoke-Expression $command
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Verificación de encabezados de seguridad completada. No se encontraron problemas graves." -ForegroundColor $Green
    Write-Host "Consulte reports\security_headers_report.md para más detalles." -ForegroundColor $Green
    exit 0
}
else {
    Write-Host "Se encontraron problemas en los encabezados de seguridad." -ForegroundColor $Red
    Write-Host "Consulte reports\security_headers_report.md para más detalles." -ForegroundColor $Red
    
    Write-Host "Recomendaciones:" -ForegroundColor $Yellow
    Write-Host "1. Revise la configuración de nginx en nginx\conf.d\default.conf" -ForegroundColor $Yellow
    Write-Host "2. Asegúrese de que todos los encabezados de seguridad recomendados estén presentes" -ForegroundColor $Yellow
    Write-Host "3. Verifique que los valores de los encabezados sean seguros" -ForegroundColor $Yellow
    
    exit 1
}
