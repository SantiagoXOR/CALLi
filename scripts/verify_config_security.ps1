# Script para verificar la seguridad de la configuración localmente
# Uso: .\scripts\verify_config_security.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow

Write-Host "Iniciando verificación de seguridad de configuración..." -ForegroundColor $Yellow
Write-Host ""

# Verificar si KICS está instalado
$kicsInstalled = $null
try {
    $kicsInstalled = Get-Command kics -ErrorAction SilentlyContinue
} catch {
    $kicsInstalled = $null
}

if (-not $kicsInstalled) {
    Write-Host "KICS no está instalado o no está en el PATH" -ForegroundColor $Red
    Write-Host "Instalando KICS..." -ForegroundColor $Yellow
    
    # Verificar si el script de instalación existe
    if (Test-Path ".\scripts\install_kics.ps1") {
        & .\scripts\install_kics.ps1
    } else {
        Write-Host "No se encontró el script de instalación de KICS" -ForegroundColor $Red
        Write-Host "Por favor, ejecute: .\scripts\install_kics.ps1" -ForegroundColor $Yellow
        exit 1
    }
    
    # Verificar nuevamente si KICS está instalado
    try {
        $kicsInstalled = Get-Command kics -ErrorAction SilentlyContinue
    } catch {
        $kicsInstalled = $null
    }
    
    if (-not $kicsInstalled) {
        Write-Host "No se pudo instalar KICS. Por favor, instálelo manualmente." -ForegroundColor $Red
        exit 1
    }
}

# Crear directorio para informes si no existe
if (-not (Test-Path "security-reports")) {
    New-Item -ItemType Directory -Path "security-reports" -Force | Out-Null
}

# Ejecutar KICS
Write-Host "Ejecutando escaneo de seguridad con KICS..." -ForegroundColor $Yellow
try {
    & kics scan -p . --config .kics.config -o security-reports
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Escaneo de KICS completado sin problemas críticos" -ForegroundColor $Green
    } else {
        Write-Host "Escaneo de KICS completado con problemas" -ForegroundColor $Red
        Write-Host "Revise los informes en el directorio 'security-reports'" -ForegroundColor $Yellow
    }
} catch {
    Write-Host "Error al ejecutar KICS: $_" -ForegroundColor $Red
    exit 1
}

# Verificar archivos de seguridad
Write-Host ""
Write-Host "Verificando archivos de seguridad requeridos..." -ForegroundColor $Yellow

$requiredFiles = @(
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
    ".github/CONTRIBUTING.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/security_issue.md",
    ".github/workflows/codeql-analysis.yml",
    ".github/dependabot.yml",
    ".github/workflows/secret-scanning.yml"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "Faltan los siguientes archivos de seguridad:" -ForegroundColor $Red
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor $Red
    }
} else {
    Write-Host "Todos los archivos de seguridad requeridos están presentes" -ForegroundColor $Green
}

# Verificar encabezados de seguridad en nginx
Write-Host ""
Write-Host "Verificando encabezados de seguridad en nginx..." -ForegroundColor $Yellow

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
    } else {
        Write-Host "Todos los encabezados de seguridad requeridos están presentes en nginx" -ForegroundColor $Green
    }
} else {
    Write-Host "No se encontró el archivo de configuración de nginx: $nginxConf" -ForegroundColor $Yellow
}

Write-Host ""
Write-Host "Verificación de seguridad completada" -ForegroundColor $Yellow
Write-Host "Revise los informes en el directorio 'security-reports' para más detalles" -ForegroundColor $Yellow
