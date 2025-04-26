# Script para ejecutar verificaciones de seguridad localmente en Windows
# Uso: .\scripts\security_check.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow

Write-Host "Iniciando verificaciones de seguridad..." -ForegroundColor $Yellow
Write-Host ""

# Verificar frontend
Write-Host "Verificando dependencias del frontend..." -ForegroundColor $Yellow
Set-Location -Path frontend-call-automation

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "Error: npm no está instalado" -ForegroundColor $Red
    exit 1
}

Write-Host "Ejecutando npm audit..."
$npmAuditResult = npm audit --json 2>$null | ConvertFrom-Json
$highCritical = 0

if ($npmAuditResult.vulnerabilities) {
    foreach ($vuln in $npmAuditResult.vulnerabilities.PSObject.Properties.Value) {
        if ($vuln.severity -eq "high" -or $vuln.severity -eq "critical") {
            $highCritical++
        }
    }
}

if ($highCritical -gt 0) {
    Write-Host "Se encontraron $highCritical vulnerabilidades de alta o crítica severidad" -ForegroundColor $Red
    Write-Host "Ejecute 'cd frontend-call-automation && npm audit' para más detalles"
} else {
    Write-Host "No se encontraron vulnerabilidades de alta o crítica severidad en el frontend" -ForegroundColor $Green
}

# Volver al directorio raíz
Set-Location -Path ..

# Verificar backend
Write-Host ""
Write-Host "Verificando dependencias del backend..." -ForegroundColor $Yellow
Set-Location -Path backend-call-automation

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: python no está instalado" -ForegroundColor $Red
    exit 1
}

$safetyInstalled = python -m pip show safety 2>$null
if (-not $safetyInstalled) {
    Write-Host "Instalando safety..."
    python -m pip install safety
}

Write-Host "Ejecutando safety check..."
$safetyResult = python -m safety check --json 2>$null | ConvertFrom-Json
$vulnerabilities = 0

if ($safetyResult) {
    $vulnerabilities = $safetyResult.Count
}

if ($vulnerabilities -gt 0) {
    Write-Host "Se encontraron $vulnerabilities vulnerabilidades" -ForegroundColor $Red
    Write-Host "Ejecute 'cd backend-call-automation && python -m safety check' para más detalles"
} else {
    Write-Host "No se encontraron vulnerabilidades en el backend" -ForegroundColor $Green
}

# Volver al directorio raíz
Set-Location -Path ..

Write-Host ""
Write-Host "Verificaciones de seguridad completadas" -ForegroundColor $Yellow

if ($highCritical -gt 0 -or $vulnerabilities -gt 0) {
    Write-Host "Se encontraron vulnerabilidades. Por favor, revise los detalles y actualice las dependencias afectadas." -ForegroundColor $Red
    exit 1
} else {
    Write-Host "No se encontraron vulnerabilidades críticas o altas." -ForegroundColor $Green
    exit 0
}
