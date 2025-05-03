# Script para verificar dependencias JavaScript
# Uso: .\scripts\check_js_dependencies.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando dependencias JavaScript..." -ForegroundColor $Cyan

# Verificar si Node.js está instalado
$nodeInstalled = $null
try {
    $nodeInstalled = node --version 2>$null
} catch {
    $nodeInstalled = $null
}

$npmInstalled = $null
try {
    $npmInstalled = npm --version 2>$null
} catch {
    $npmInstalled = $null
}

if (-not $nodeInstalled -or -not $npmInstalled) {
    Write-Host "Node.js no está instalado o no está en el PATH." -ForegroundColor $Red
    Write-Host "Por favor, ejecute .\scripts\check_nodejs.ps1 para instalar Node.js" -ForegroundColor $Yellow
    exit 1
}

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Verificar si existe el directorio frontend-call-automation
if (-not (Test-Path "frontend-call-automation")) {
    Write-Host "No se encontró el directorio frontend-call-automation" -ForegroundColor $Red
    exit 1
}

# Verificar si existe package.json
if (-not (Test-Path "frontend-call-automation\package.json")) {
    Write-Host "No se encontró el archivo package.json en frontend-call-automation" -ForegroundColor $Red
    exit 1
}

# Ejecutar npm audit
Write-Host "Ejecutando npm audit..." -ForegroundColor $Yellow
$currentDir = Get-Location
Set-Location -Path "frontend-call-automation"

try {
    # Ejecutar npm audit y guardar la salida
    $npmOutput = npm audit --json 2>&1
    $npmExitCode = $LASTEXITCODE

    # Guardar la salida en un archivo
    $npmOutput | Out-File -FilePath "..\reports\npm_audit.json"

    # Intentar analizar la salida JSON
    try {
        $auditData = $npmOutput | ConvertFrom-Json

        # Contar vulnerabilidades por severidad
        $vulnerabilities = @{
            "critical" = 0
            "high" = 0
            "moderate" = 0
            "low" = 0
            "info" = 0
        }

        if ($auditData.vulnerabilities) {
            foreach ($vuln in $auditData.vulnerabilities.PSObject.Properties) {
                $severity = $vuln.Value.severity
                if ($vulnerabilities.ContainsKey($severity)) {
                    $vulnerabilities[$severity]++
                }
            }
        }

        # Mostrar resumen
        Write-Host "Resumen de vulnerabilidades:" -ForegroundColor $Yellow
        Write-Host "- Críticas: $($vulnerabilities['critical'])" -ForegroundColor $(if ($vulnerabilities['critical'] -gt 0) { $Red } else { $Green })
        Write-Host "- Altas: $($vulnerabilities['high'])" -ForegroundColor $(if ($vulnerabilities['high'] -gt 0) { $Red } else { $Green })
        Write-Host "- Moderadas: $($vulnerabilities['moderate'])" -ForegroundColor $(if ($vulnerabilities['moderate'] -gt 0) { $Yellow } else { $Green })
        Write-Host "- Bajas: $($vulnerabilities['low'])" -ForegroundColor $(if ($vulnerabilities['low'] -gt 0) { $Yellow } else { $Green })
        Write-Host "- Informativas: $($vulnerabilities['info'])" -ForegroundColor $Green

        # Generar informe en formato legible
        $reportContent = @"
# Informe de Seguridad de Dependencias JavaScript

## Resumen

- **Críticas**: $($vulnerabilities['critical'])
- **Altas**: $($vulnerabilities['high'])
- **Moderadas**: $($vulnerabilities['moderate'])
- **Bajas**: $($vulnerabilities['low'])
- **Informativas**: $($vulnerabilities['info'])

## Detalles

"@

        if ($auditData.vulnerabilities) {
            foreach ($vuln in $auditData.vulnerabilities.PSObject.Properties) {
                $reportContent += @"

### $($vuln.Name)

- **Severidad**: $($vuln.Value.severity)
- **Vía**: $($vuln.Value.via -join ", ")
- **Efectos**: $($vuln.Value.effects -join ", ")
- **Rango**: $($vuln.Value.range)
- **Dependencias**: $($vuln.Value.nodes -join ", ")

"@
            }
        }

        $reportContent | Out-File -FilePath "..\reports\npm_audit_report.md"

        # Determinar el código de salida basado en la presencia de vulnerabilidades críticas o altas
        if ($vulnerabilities['critical'] -gt 0 -or $vulnerabilities['high'] -gt 0) {
            Write-Host "Se encontraron vulnerabilidades críticas o altas. Por favor, actualice las dependencias." -ForegroundColor $Red
            $exitCode = 1
        } else {
            Write-Host "No se encontraron vulnerabilidades críticas o altas." -ForegroundColor $Green
            $exitCode = 0
        }
    } catch {
        Write-Host "Error al analizar la salida de npm audit: $_" -ForegroundColor $Red
        $exitCode = 1
    }
} catch {
    Write-Host "Error al ejecutar npm audit: $_" -ForegroundColor $Red
    $exitCode = 1
} finally {
    # Volver al directorio original
    Set-Location -Path $currentDir
}

# Sugerir soluciones
if ($exitCode -ne 0) {
    Write-Host "Recomendaciones:" -ForegroundColor $Yellow
    Write-Host "1. Ejecute 'cd frontend-call-automation && npm audit fix' para intentar corregir automáticamente las vulnerabilidades" -ForegroundColor $Yellow
    Write-Host "2. Para vulnerabilidades que no se pueden corregir automáticamente, actualice manualmente las dependencias" -ForegroundColor $Yellow
    Write-Host "3. Consulte reports\npm_audit_report.md para más detalles" -ForegroundColor $Yellow
}

exit $exitCode
