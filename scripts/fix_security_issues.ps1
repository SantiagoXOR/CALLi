# Script para corregir problemas de seguridad comunes
# Uso: .\scripts\fix_security_issues.ps1 [--dry-run]

param (
    [switch]$dryRun = $false
)

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Corrigiendo problemas de seguridad comunes en el proyecto CALLi..." -ForegroundColor $Cyan

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Función para buscar y corregir problemas de seguridad en archivos
function Fix-SecurityIssues {
    param (
        [string]$Directory,
        [switch]$DryRun
    )

    $issuesFound = 0
    $issuesFixed = 0
    $report = @()

    # Buscar archivos Python
    $pythonFiles = Get-ChildItem -Path $Directory -Filter "*.py" -Recurse

    foreach ($file in $pythonFiles) {
        $content = Get-Content -Path $file.FullName -Raw
        $modified = $false
        $fileIssues = 0

        # Problema 1: Uso inseguro de subprocess con shell=True
        if ($content -match "subprocess\.(?:call|run|Popen).*shell\s*=\s*True") {
            $fileIssues++
            $issuesFound++
            $report += "Archivo: $($file.FullName)"
            $report += "  - Problema: Uso inseguro de subprocess con shell=True"
            $report += "  - Recomendación: Evitar shell=True y usar una lista de argumentos en su lugar"

            if (-not $DryRun) {
                # Intentar corregir reemplazando shell=True con shell=False
                $newContent = $content -replace "(subprocess\.(?:call|run|Popen).*shell\s*=\s*)True", '$1False'

                # Solo aplicar si hubo cambios
                if ($newContent -ne $content) {
                    Set-Content -Path $file.FullName -Value $newContent
                    $modified = $true
                    $issuesFixed++
                    $report += "  - Acción: Reemplazado shell=True con shell=False"
                } else {
                    $report += "  - Acción: No se pudo corregir automáticamente, requiere revisión manual"
                }
            } else {
                $report += "  - Acción: Se corregiría en modo real"
            }
            $report += ""
        }

        # Problema 2: Credenciales hardcodeadas
        if ($content -match "(password|api_key|secret|token|credentials)\s*=\s*['\"][^'\"]+['\"]") {
            $fileIssues++
            $issuesFound++
            $report += "Archivo: $($file.FullName)"
            $report += "  - Problema: Posibles credenciales hardcodeadas"
            $report += "  - Recomendación: Mover credenciales a variables de entorno o almacén seguro"
            $report += "  - Acción: Requiere revisión manual"
            $report += ""
        }

        # Problema 3: Uso inseguro de eval o exec
        if ($content -match "(eval|exec)\s*\(") {
            $fileIssues++
            $issuesFound++
            $report += "Archivo: $($file.FullName)"
            $report += "  - Problema: Uso inseguro de eval() o exec()"
            $report += "  - Recomendación: Evitar eval/exec y usar alternativas más seguras"
            $report += "  - Acción: Requiere revisión manual"
            $report += ""
        }

        # Problema 4: Deserialización insegura de pickle
        if ($content -match "pickle\.loads") {
            $fileIssues++
            $issuesFound++
            $report += "Archivo: $($file.FullName)"
            $report += "  - Problema: Deserialización insegura con pickle"
            $report += "  - Recomendación: Usar json u otro formato seguro en su lugar"
            $report += "  - Acción: Requiere revisión manual"
            $report += ""
        }

        # Problema 5: SQL Injection potencial
        if ($content -match "execute\(\s*f['\"]|execute\(\s*['\"].*\{\}.*['\"]\.format|execute\(\s*['\"].*%s.*['\"].*%") {
            $fileIssues++
            $issuesFound++
            $report += "Archivo: $($file.FullName)"
            $report += "  - Problema: Posible SQL Injection"
            $report += "  - Recomendación: Usar consultas parametrizadas"
            $report += "  - Acción: Requiere revisión manual"
            $report += ""
        }

        # Problema 6: Uso de algoritmos criptográficos débiles
        if ($content -match "import\s+md5|hashlib\.md5|import\s+sha1|hashlib\.sha1") {
            $fileIssues++
            $issuesFound++
            $report += "Archivo: $($file.FullName)"
            $report += "  - Problema: Uso de algoritmos criptográficos débiles (MD5/SHA1)"
            $report += "  - Recomendación: Usar SHA-256 o algoritmos más fuertes"

            if (-not $DryRun) {
                # Intentar corregir reemplazando md5/sha1 con sha256
                $newContent = $content -replace "hashlib\.md5", "hashlib.sha256"
                $newContent = $newContent -replace "hashlib\.sha1", "hashlib.sha256"

                # Solo aplicar si hubo cambios
                if ($newContent -ne $content) {
                    Set-Content -Path $file.FullName -Value $newContent
                    $modified = $true
                    $issuesFixed++
                    $report += "  - Acción: Reemplazado algoritmos débiles con SHA-256"
                } else {
                    $report += "  - Acción: No se pudo corregir automáticamente, requiere revisión manual"
                }
            } else {
                $report += "  - Acción: Se corregiría en modo real"
            }
            $report += ""
        }

        if ($fileIssues -gt 0) {
            if ($modified -and -not $DryRun) {
                Write-Host "Corregido archivo: $($file.FullName)" -ForegroundColor $Green
            } else {
                Write-Host "Problemas encontrados en: $($file.FullName)" -ForegroundColor $Yellow
            }
        }
    }

    return @{
        IssuesFound = $issuesFound
        IssuesFixed = $issuesFixed
        Report = $report
    }
}

# Ejecutar la corrección de problemas de seguridad
$result = Fix-SecurityIssues -Directory "backend-call-automation" -DryRun:$dryRun

# Guardar el informe
$reportContent = "# Informe de Problemas de Seguridad`n`n"
$reportContent += "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
$reportContent += "Modo: $(if ($dryRun) { 'Simulación' } else { 'Corrección' })`n`n"

if ($result.IssuesFound -eq 0) {
    $reportContent += "No se encontraron problemas de seguridad.`n"
} else {
    $reportContent += "## Resumen`n`n"
    $reportContent += "- Problemas encontrados: $($result.IssuesFound)`n"
    $reportContent += "- Problemas corregidos: $($result.IssuesFixed)`n`n"
    $reportContent += "## Detalles`n`n"
    $reportContent += $result.Report -join "`n"
}

$reportPath = "reports\security_issues_report.md"
Set-Content -Path $reportPath -Value $reportContent

# Mostrar resumen
Write-Host "`nResumen:" -ForegroundColor $Cyan
Write-Host "- Problemas encontrados: $($result.IssuesFound)" -ForegroundColor $(if ($result.IssuesFound -eq 0) { $Green } else { $Yellow })
Write-Host "- Problemas corregidos: $($result.IssuesFixed)" -ForegroundColor $(if ($result.IssuesFixed -eq $result.IssuesFound) { $Green } else { $Yellow })

if ($result.IssuesFound -gt 0) {
    Write-Host "`nSe ha generado un informe detallado en: $reportPath" -ForegroundColor $Cyan

    if ($dryRun) {
        Write-Host "`nEste fue un análisis en modo simulación. Para aplicar las correcciones, ejecute:" -ForegroundColor $Yellow
        Write-Host "  .\scripts\fix_security_issues.ps1" -ForegroundColor $Yellow
    } elseif ($result.IssuesFixed -lt $result.IssuesFound) {
        Write-Host "`nAlgunos problemas requieren revisión manual. Consulte el informe para más detalles." -ForegroundColor $Yellow
    }
} else {
    Write-Host "`n✓ No se encontraron problemas de seguridad." -ForegroundColor $Green
}

# Ejecutar verificación de seguridad completa
Write-Host "`nEjecutando verificación de seguridad completa..." -ForegroundColor $Cyan
& .\scripts\run_security_checks.ps1
$securityExitCode = $LASTEXITCODE

if ($securityExitCode -eq 0) {
    Write-Host "✓ Verificación de seguridad completada con éxito." -ForegroundColor $Green
} else {
    Write-Host "⚠ Se encontraron problemas de seguridad adicionales. Consulte los informes para más detalles." -ForegroundColor $Yellow
}

exit $(if ($result.IssuesFound -eq 0) { 0 } else { 1 })
