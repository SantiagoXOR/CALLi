# Script para ejecutar todas las verificaciones de seguridad
# Uso: .\scripts\run_security_checks.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "====================================================" -ForegroundColor $Cyan
Write-Host "      Verificación de Seguridad Completa CALLi      " -ForegroundColor $Cyan
Write-Host "====================================================" -ForegroundColor $Cyan
Write-Host ""

# Crear directorio para informes si no existe
if (-not (Test-Path "security-reports")) {
    New-Item -ItemType Directory -Path "security-reports" -Force | Out-Null
}

# 1. Verificar configuración de seguridad
Write-Host "1. Verificando configuración de seguridad..." -ForegroundColor $Cyan
if (Test-Path ".\scripts\verify_config_security.ps1") {
    & .\scripts\verify_config_security.ps1
}
else {
    Write-Host "No se encontró el script de verificación de configuración" -ForegroundColor $Red
    Write-Host "Ejecutando verificación de seguridad local alternativa..." -ForegroundColor $Yellow
    if (Test-Path ".\scripts\security_check_local.py") {
        python .\scripts\security_check_local.py
    }
    else {
        Write-Host "No se encontró ningún script de verificación de seguridad" -ForegroundColor $Red
    }
}

# 2. Verificar dependencias de Python
Write-Host ""
Write-Host "2. Verificando dependencias de Python..." -ForegroundColor $Cyan
$requirementsFile = "backend-call-automation/requirements.txt"
if (Test-Path $requirementsFile) {
    try {
        # Verificar si safety está instalado
        $safetyInstalled = $null
        try {
            $safetyInstalled = python -m pip show safety 2>$null
        }
        catch {
            $safetyInstalled = $null
        }

        if (-not $safetyInstalled) {
            Write-Host "Instalando safety..." -ForegroundColor $Yellow
            python -m pip install safety
        }

        # Ejecutar safety check
        Write-Host "Ejecutando safety check..." -ForegroundColor $Yellow
        $safetyOutput = python -m safety check -r $requirementsFile 2>&1
        $safetyExitCode = $LASTEXITCODE

        if ($safetyExitCode -ne 0) {
            Write-Host "Se encontraron vulnerabilidades en dependencias Python:" -ForegroundColor $Red
            Write-Host $safetyOutput
        }
        else {
            Write-Host "No se encontraron vulnerabilidades en dependencias Python" -ForegroundColor $Green
        }

        # Guardar resultados
        $safetyOutput | Out-File -FilePath "security-reports/python-dependencies.txt"
    }
    catch {
        Write-Host "Error al verificar dependencias Python: $_" -ForegroundColor $Red
    }
}
else {
    Write-Host "No se encontró el archivo de requisitos de Python: $requirementsFile" -ForegroundColor $Yellow
}

# 3. Verificar dependencias de JavaScript
Write-Host ""
Write-Host "3. Verificando dependencias de JavaScript..." -ForegroundColor $Cyan
$packageJsonFile = "frontend-call-automation/package.json"
if (Test-Path $packageJsonFile) {
    try {
        # Verificar si npm está instalado
        $npmInstalled = $null
        try {
            $npmInstalled = npm --version 2>$null
        }
        catch {
            $npmInstalled = $null
        }

        if (-not $npmInstalled) {
            Write-Host "npm no está instalado o no está en el PATH" -ForegroundColor $Red
        }
        else {
            # Ejecutar npm audit
            Write-Host "Ejecutando npm audit..." -ForegroundColor $Yellow
            $currentDir = Get-Location
            Set-Location -Path "frontend-call-automation"
            $npmOutput = npm audit --json 2>&1
            $npmExitCode = $LASTEXITCODE
            Set-Location -Path $currentDir

            if ($npmExitCode -ne 0) {
                try {
                    $auditData = $npmOutput | ConvertFrom-Json
                    $vulnerabilities = $auditData.vulnerabilities
                    $highCritical = 0

                    foreach ($vuln in $vulnerabilities.PSObject.Properties) {
                        if ($vuln.Value.severity -in @("high", "critical")) {
                            $highCritical++
                        }
                    }

                    if ($highCritical -gt 0) {
                        Write-Host "Se encontraron $highCritical vulnerabilidades de alta o crítica severidad" -ForegroundColor $Red
                    }
                    else {
                        Write-Host "Se encontraron vulnerabilidades de baja severidad" -ForegroundColor $Yellow
                    }
                }
                catch {
                    Write-Host "Se encontraron vulnerabilidades pero no se pudo analizar el resultado" -ForegroundColor $Red
                }
            }
            else {
                Write-Host "No se encontraron vulnerabilidades en dependencias JavaScript" -ForegroundColor $Green
            }

            # Guardar resultados
            $npmOutput | Out-File -FilePath "security-reports/js-dependencies.json"
        }
    }
    catch {
        Write-Host "Error al verificar dependencias JavaScript: $_" -ForegroundColor $Red
    }
}
else {
    Write-Host "No se encontró el archivo package.json: $packageJsonFile" -ForegroundColor $Yellow
}

# 4. Buscar secretos en el código
Write-Host ""
Write-Host "4. Buscando secretos en el código..." -ForegroundColor $Cyan

# Verificar si gitleaks está instalado
$gitleaksInstalled = $false
try {
    $gitleaksVersion = gitleaks version
    $gitleaksInstalled = $true
    Write-Host "gitleaks está instalado: $gitleaksVersion" -ForegroundColor $Green
}
catch {
    Write-Host "gitleaks no está instalado. Instalando..." -ForegroundColor $Yellow

    # Verificar si existe el script de instalación
    if (Test-Path ".\scripts\install_gitleaks.ps1") {
        & .\scripts\install_gitleaks.ps1
        try {
            $gitleaksVersion = gitleaks version
            $gitleaksInstalled = $true
            Write-Host "gitleaks instalado correctamente: $gitleaksVersion" -ForegroundColor $Green
        }
        catch {
            Write-Host "No se pudo instalar gitleaks. Continuando con métodos alternativos." -ForegroundColor $Yellow
        }
    }
    else {
        Write-Host "No se encontró el script de instalación de gitleaks. Continuando con métodos alternativos." -ForegroundColor $Yellow
    }
}

# Usar gitleaks si está disponible
if ($gitleaksInstalled) {
    Write-Host "Ejecutando gitleaks para detectar secretos..." -ForegroundColor $Yellow

    # Crear directorio para el informe si no existe
    if (-not (Test-Path "security-reports")) {
        New-Item -ItemType Directory -Path "security-reports" -Force | Out-Null
    }

    # Ejecutar gitleaks
    gitleaks detect --source . --report-format json --report-path security-reports\gitleaks_report.json
    $gitleaksExitCode = $LASTEXITCODE

    if ($gitleaksExitCode -eq 0) {
        Write-Host "No se encontraron secretos en el código con gitleaks" -ForegroundColor $Green
    }
    else {
        Write-Host "Se encontraron posibles secretos en el código con gitleaks. Consulte security-reports\gitleaks_report.json para más detalles." -ForegroundColor $Red
    }
}
else {
    # Usar métodos alternativos si gitleaks no está disponible
    if (Test-Path ".\scripts\improved_security_utils.py") {
        try {
            $secretsOutput = python -c "from scripts.improved_security_utils import find_secrets; status, secrets = find_secrets(); print(f'Secretos encontrados: {len(secrets)}'); [print(s) for s in secrets[:10]]; print(f'... y {len(secrets) - 10} más') if len(secrets) > 10 else None"

            if ($secretsOutput -match "Secretos encontrados: 0") {
                Write-Host "No se encontraron secretos en el código" -ForegroundColor $Green
            }
            else {
                Write-Host "Se encontraron posibles secretos en el código:" -ForegroundColor $Red
                Write-Host $secretsOutput
            }
        }
        catch {
            Write-Host "Error al buscar secretos: $_" -ForegroundColor $Red
            Write-Host "Ejecutando verificación de secretos alternativa..." -ForegroundColor $Yellow
            python .\scripts\security_check_local.py
        }
    }
    else {
        Write-Host "No se encontró el módulo mejorado de seguridad" -ForegroundColor $Yellow
        Write-Host "Ejecutando verificación de secretos alternativa..." -ForegroundColor $Yellow
        python .\scripts\security_check_local.py
    }
}

# 5. Verificar encabezados de seguridad
Write-Host ""
Write-Host "5. Verificando encabezados de seguridad..." -ForegroundColor $Cyan
$nginxConf = "nginx/conf.d/default.conf"
if (Test-Path $nginxConf) {
    $content = Get-Content $nginxConf -Raw

    $requiredHeaders = @(
        "Strict-Transport-Security",
        "X-Content-Type-Options",
        "X-Frame-Options",
        "Content-Security-Policy"
    )

    $missingHeaders = @()
    foreach ($header in $requiredHeaders) {
        if ($content -notmatch "add_header\s+$header") {
            $missingHeaders += $header
        }
    }

    if ($missingHeaders.Count -gt 0) {
        Write-Host "Faltan los siguientes encabezados de seguridad en nginx:" -ForegroundColor $Red
        foreach ($header in $missingHeaders) {
            Write-Host "  - $header" -ForegroundColor $Red
        }
    }
    else {
        Write-Host "Todos los encabezados de seguridad requeridos están presentes en nginx" -ForegroundColor $Green
    }
}
else {
    Write-Host "No se encontró el archivo de configuración de nginx: $nginxConf" -ForegroundColor $Yellow
}

# Resumen final
Write-Host ""
Write-Host "====================================================" -ForegroundColor $Cyan
Write-Host "            Resumen de Verificaciones              " -ForegroundColor $Cyan
Write-Host "====================================================" -ForegroundColor $Cyan
Write-Host "Los informes detallados se han guardado en el directorio 'security-reports'" -ForegroundColor $Yellow
Write-Host "Para una verificación más completa, ejecute los siguientes comandos:" -ForegroundColor $Yellow
Write-Host "  - python .\scripts\security_check_local.py" -ForegroundColor $Yellow
Write-Host "  - .\scripts\verify_config_security.ps1" -ForegroundColor $Yellow
Write-Host "  - python .\scripts\improved_security_utils.py" -ForegroundColor $Yellow
if ($gitleaksInstalled) {
    Write-Host "  - gitleaks detect --source ." -ForegroundColor $Yellow
}
else {
    Write-Host "  - Instale gitleaks con .\scripts\install_gitleaks.ps1" -ForegroundColor $Yellow
}
Write-Host ""
Write-Host "Verificación de seguridad completada" -ForegroundColor $Cyan
