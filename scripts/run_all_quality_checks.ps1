# Script para ejecutar todas las verificaciones de calidad del código
# Uso: .\scripts\run_all_quality_checks.ps1 [--fix]

param (
    [switch]$fix = $false
)

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan
$Magenta = [ConsoleColor]::Magenta

Write-Host "Ejecutando verificaciones de calidad en el proyecto CALLi..." -ForegroundColor $Cyan
Write-Host "============================================================" -ForegroundColor $Cyan

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Función para ejecutar un comando y mostrar su resultado
function Run-Command {
    param (
        [string]$Name,
        [string]$Command,
        [string]$SuccessMessage,
        [string]$FailureMessage
    )

    Write-Host "`n>> Ejecutando $Name..." -ForegroundColor $Magenta

    Invoke-Expression $Command
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host $SuccessMessage -ForegroundColor $Green
    }
    else {
        Write-Host $FailureMessage -ForegroundColor $Yellow
    }

    return $exitCode
}

# Verificar formato con Ruff
$ruffCommand = if ($fix) { ".\scripts\run_ruff.ps1 -fix" } else { ".\scripts\run_ruff.ps1" }
$ruffExitCode = Run-Command -Name "Ruff (verificación de formato)" `
    -Command $ruffCommand `
    -SuccessMessage "✓ Verificación de formato completada con éxito." `
    -FailureMessage "⚠ Se encontraron problemas de formato. Ejecute .\scripts\run_ruff.ps1 -fix para corregirlos."

# Verificar tipos con MyPy
$mypyExitCode = Run-Command -Name "MyPy (verificación de tipos)" `
    -Command ".\scripts\run_mypy.ps1" `
    -SuccessMessage "✓ Verificación de tipos completada con éxito." `
    -FailureMessage "⚠ Se encontraron problemas de tipos. Consulte reports\mypy_report.txt para más detalles."

# Verificar docstrings
$docstringsCommand = if ($fix) { ".\scripts\run_docstring_fix.ps1" } else { ".\scripts\run_docstring_check.ps1" }
$docstringsExitCode = Run-Command -Name "Verificación de docstrings" `
    -Command $docstringsCommand `
    -SuccessMessage "✓ Verificación de docstrings completada con éxito." `
    -FailureMessage "⚠ Se encontraron problemas de documentación. Ejecute .\scripts\run_docstring_fix.ps1 para generar plantillas."

# Verificar seguridad
$securityExitCode = Run-Command -Name "Verificación de seguridad" `
    -Command ".\scripts\run_security_checks.ps1" `
    -SuccessMessage "✓ Verificación de seguridad completada con éxito." `
    -FailureMessage "⚠ Se encontraron problemas de seguridad. Consulte los informes en security-reports\ para más detalles."

# Verificar falsos positivos
$falsePositivesExitCode = Run-Command -Name "Revisión de falsos positivos" `
    -Command ".\scripts\run_false_positives_review.ps1" `
    -SuccessMessage "✓ Revisión de falsos positivos completada con éxito." `
    -FailureMessage "⚠ Se encontraron posibles problemas de seguridad. Consulte reports\false_positives_report.md para más detalles."

# Resumen
Write-Host "`n============================================================" -ForegroundColor $Cyan
Write-Host "Resumen de verificaciones:" -ForegroundColor $Cyan

function Show-Result {
    param (
        [string]$Name,
        [int]$ExitCode
    )

    $status = if ($ExitCode -eq 0) { "✓ Pasó" } else { "✗ Falló" }
    $color = if ($ExitCode -eq 0) { $Green } else { $Red }

    Write-Host "${Name}: " -NoNewline
    Write-Host $status -ForegroundColor $color
}

Show-Result -Name "Formato (Ruff)" -ExitCode $ruffExitCode
Show-Result -Name "Tipos (MyPy)" -ExitCode $mypyExitCode
Show-Result -Name "Documentación" -ExitCode $docstringsExitCode
Show-Result -Name "Seguridad" -ExitCode $securityExitCode
Show-Result -Name "Falsos positivos" -ExitCode $falsePositivesExitCode

# Resultado final
$totalExitCode = $ruffExitCode + $mypyExitCode + $docstringsExitCode + $securityExitCode + $falsePositivesExitCode
if ($totalExitCode -eq 0) {
    Write-Host "`n✓ Todas las verificaciones pasaron correctamente." -ForegroundColor $Green
}
else {
    Write-Host "`n⚠ Algunas verificaciones fallaron. Revise los informes para más detalles." -ForegroundColor $Yellow

    if ($fix) {
        Write-Host "Se han aplicado correcciones automáticas donde fue posible." -ForegroundColor $Yellow
    }
    else {
        Write-Host "Ejecute este script con el parámetro -fix para aplicar correcciones automáticas donde sea posible:" -ForegroundColor $Yellow
        Write-Host "  .\scripts\run_all_quality_checks.ps1 -fix" -ForegroundColor $Yellow
    }
}

exit $totalExitCode
