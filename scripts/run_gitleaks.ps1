# Script para ejecutar gitleaks manualmente
# Uso: .\scripts\run_gitleaks.ps1 [--install]

param (
    [switch]$install = $false
)

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando secretos en el código con gitleaks..." -ForegroundColor $Cyan

# Verificar si gitleaks está instalado
$gitleaksInstalled = $false
try {
    $gitleaksVersion = gitleaks version
    $gitleaksInstalled = $true
    Write-Host "gitleaks está instalado: $gitleaksVersion" -ForegroundColor $Green
}
catch {
    Write-Host "gitleaks no está instalado" -ForegroundColor $Yellow

    if ($install) {
        Write-Host "Instalando gitleaks..." -ForegroundColor $Yellow

        # Verificar si existe el script de instalación
        if (Test-Path ".\scripts\install_gitleaks.ps1") {
            & .\scripts\install_gitleaks.ps1
            try {
                $gitleaksVersion = gitleaks version
                $gitleaksInstalled = $true
                Write-Host "gitleaks instalado correctamente: $gitleaksVersion" -ForegroundColor $Green
            }
            catch {
                Write-Host "No se pudo instalar gitleaks. Ejecute .\scripts\install_gitleaks.ps1 manualmente." -ForegroundColor $Red
                exit 1
            }
        }
        else {
            Write-Host "No se encontró el script de instalación de gitleaks. Ejecute .\scripts\install_gitleaks.ps1 manualmente." -ForegroundColor $Red
            exit 1
        }
    }
    else {
        Write-Host "Para instalar gitleaks, ejecute este script con el parámetro --install o ejecute .\scripts\install_gitleaks.ps1 manualmente." -ForegroundColor $Yellow
        exit 1
    }
}

# Crear directorio para el informe si no existe
if (-not (Test-Path "security-reports")) {
    New-Item -ItemType Directory -Path "security-reports" -Force | Out-Null
}

# Ejecutar gitleaks
Write-Host "Ejecutando gitleaks para detectar secretos..." -ForegroundColor $Yellow
gitleaks detect --source . --report-format json --report-path security-reports\gitleaks_report.json
$gitleaksExitCode = $LASTEXITCODE

if ($gitleaksExitCode -eq 0) {
    Write-Host "No se encontraron secretos en el código con gitleaks" -ForegroundColor $Green
    exit 0
}
else {
    Write-Host "Se encontraron posibles secretos en el código con gitleaks. Consulte security-reports\gitleaks_report.json para más detalles." -ForegroundColor $Red

    # Intentar leer el informe JSON
    try {
        $report = Get-Content -Path security-reports\gitleaks_report.json -Raw | ConvertFrom-Json
        $secretCount = $report.Count

        Write-Host "Se encontraron $secretCount posibles secretos:" -ForegroundColor $Red

        foreach ($finding in $report) {
            Write-Host "  - Archivo: $($finding.File)" -ForegroundColor $Red
            Write-Host "    Línea: $($finding.StartLine)" -ForegroundColor $Red
            Write-Host "    Descripción: $($finding.Description)" -ForegroundColor $Red
            Write-Host "    Regla: $($finding.RuleID)" -ForegroundColor $Red
            Write-Host ""
        }

        Write-Host "Recomendaciones:" -ForegroundColor $Yellow
        Write-Host "1. Revise los secretos encontrados y elimínelos del código" -ForegroundColor $Yellow
        Write-Host "2. Utilice variables de entorno o servicios de gestión de secretos como Vault" -ForegroundColor $Yellow
        Write-Host "3. Rote cualquier secreto que haya sido expuesto" -ForegroundColor $Yellow
        Write-Host "4. Considere usar la función secure_mask_secret de scripts\improved_security_utils.py para enmascarar secretos en logs" -ForegroundColor $Yellow
    }
    catch {
        Write-Host "No se pudo leer el informe de gitleaks. Verifique el archivo security-reports\gitleaks_report.json manualmente." -ForegroundColor $Red
    }

    exit 1
}
