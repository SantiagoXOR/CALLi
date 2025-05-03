# Script para revisar falsos positivos en informes de seguridad
# Uso: .\scripts\run_false_positives_review.ps1 [--report <ruta_informe>]

param (
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$args
)

# Procesar argumentos
$report = ""
for ($i = 0; $i -lt $args.Count; $i++) {
    if ($args[$i] -eq "--report") {
        if ($i + 1 -lt $args.Count) {
            $report = $args[$i + 1]
            $i++
        }
    }
}

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Revisando falsos positivos en informes de seguridad..." -ForegroundColor $Cyan

# Crear directorio para informes
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

# Si no se especificó un informe, buscar el más reciente
if (-not $report) {
    Write-Host "No se especificó un informe. Buscando el más reciente..." -ForegroundColor $Yellow

    $securityReports = Get-ChildItem -Path "security-reports" -Filter "*.json" -Recurse -ErrorAction SilentlyContinue

    if (-not $securityReports) {
        Write-Host "No se encontraron informes de seguridad. Ejecutando verificación de seguridad..." -ForegroundColor $Yellow

        # Ejecutar verificación de seguridad
        & .\scripts\security_check_local.py

        # Buscar nuevamente
        $securityReports = Get-ChildItem -Path "security-reports" -Filter "*.json" -Recurse -ErrorAction SilentlyContinue
    }

    if ($securityReports) {
        $report = ($securityReports | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
        Write-Host "Se utilizará el informe más reciente: $report" -ForegroundColor $Yellow
    }
    else {
        Write-Host "No se encontraron informes de seguridad. Por favor, ejecute una verificación de seguridad primero." -ForegroundColor $Red
        exit 1
    }
}

# Ejecutar el script de revisión de falsos positivos
Write-Host "Ejecutando revisión de falsos positivos..." -ForegroundColor $Yellow
$command = "python scripts\review_false_positives.py --report `"$report`" --output reports\false_positives_report.md"
Invoke-Expression $command
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host "Revisión completada con éxito. No se encontraron verdaderos positivos." -ForegroundColor $Green
}
else {
    Write-Host "Se encontraron verdaderos positivos. Consulte reports\false_positives_report.md para más detalles." -ForegroundColor $Yellow
}

exit $exitCode
