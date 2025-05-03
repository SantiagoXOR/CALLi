# Script maestro para ejecutar todas las verificaciones de seguridad
# Uso: .\scripts\run_all_checks.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Ejecutando todas las verificaciones de seguridad..." -ForegroundColor $Cyan

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Función para ejecutar un script y mostrar su resultado
function Run-Script {
    param (
        [string]$ScriptName,
        [string]$Description,
        [string[]]$Arguments = @()
    )

    Write-Host ""
    Write-Host "=== $Description ===" -ForegroundColor $Cyan

    & $ScriptName @Arguments
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        Write-Host "✓ $Description completado con éxito" -ForegroundColor $Green
    } else {
        Write-Host "✗ $Description completado con errores" -ForegroundColor $Red
    }

    return $exitCode
}

# Verificar Node.js
$nodeResult = Run-Script -ScriptName ".\scripts\check_nodejs.ps1" -Description "Verificación de Node.js"

# Ejecutar verificaciones
$results = @()

$results += @{
    Name = "Verificación de formato con Ruff"
    Result = (Run-Script -ScriptName ".\scripts\run_ruff.ps1" -Description "Verificación de formato con Ruff")
}

$results += @{
    Name = "Verificación de tipos con MyPy"
    Result = (Run-Script -ScriptName ".\scripts\run_mypy.ps1" -Description "Verificación de tipos con MyPy")
}

$results += @{
    Name = "Verificación de docstrings"
    Result = (Run-Script -ScriptName ".\scripts\run_docstring_check.ps1" -Description "Verificación de docstrings")
}

$results += @{
    Name = "Verificación de documentación RST"
    Result = (Run-Script -ScriptName ".\scripts\run_rst_check.ps1" -Description "Verificación de documentación RST")
}

# Verificar dependencias JavaScript solo si Node.js está instalado
if ($nodeResult -eq 0) {
    $results += @{
        Name = "Verificación de dependencias JavaScript"
        Result = (Run-Script -ScriptName ".\scripts\check_js_dependencies.ps1" -Description "Verificación de dependencias JavaScript")
    }
}

# Ejecutar verificación de seguridad
$results += @{
    Name = "Verificación de seguridad"
    Result = (Run-Script -ScriptName "python" -Description "Verificación de seguridad" -Arguments @("scripts\security_check_local.py"))
}

# Revisar falsos positivos
$results += @{
    Name = "Revisión de falsos positivos"
    Result = (Run-Script -ScriptName ".\scripts\run_false_positives_review.ps1" -Description "Revisión de falsos positivos")
}

# Generar informe final
Write-Host ""
Write-Host "=== Resumen de Verificaciones ===" -ForegroundColor $Cyan
Write-Host ""

$allPassed = $true
foreach ($result in $results) {
    if ($result.Result -eq 0) {
        Write-Host "✓ $($result.Name): Éxito" -ForegroundColor $Green
    } else {
        Write-Host "✗ $($result.Name): Error" -ForegroundColor $Red
        $allPassed = $false
    }
}

Write-Host ""
if ($allPassed) {
    Write-Host "✓ Todas las verificaciones completadas con éxito" -ForegroundColor $Green
} else {
    Write-Host "✗ Algunas verificaciones fallaron. Revise los informes para más detalles." -ForegroundColor $Red
}

# Generar informe en Markdown
$reportContent = @"
# Informe de Verificaciones de Seguridad

## Resumen

Fecha: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

| Verificación | Resultado |
|--------------|-----------|
"@

foreach ($result in $results) {
    $status = if ($result.Result -eq 0) { "✅ Éxito" } else { "❌ Error" }
    $reportContent += "`n| $($result.Name) | $status |"
}

$reportContent += @"

## Detalles

Para ver los detalles de cada verificación, consulte los informes individuales en el directorio `reports/`.

## Próximos Pasos

"@

if ($allPassed) {
    $reportContent += @"
- Continuar con el desarrollo normal
- Considerar implementar pruebas adicionales
- Revisar periódicamente las dependencias para mantenerlas actualizadas
"@
} else {
    $reportContent += @"
- Corregir los problemas identificados en los informes
- Volver a ejecutar las verificaciones para confirmar que los problemas se han resuelto
- Considerar automatizar estas verificaciones en el flujo de trabajo de CI/CD
"@
}

$reportContent | Out-File -FilePath "reports\verification_summary.md"

Write-Host "Informe guardado en reports\verification_summary.md" -ForegroundColor $Cyan

# Devolver código de salida
if ($allPassed) {
    exit 0
} else {
    exit 1
}
