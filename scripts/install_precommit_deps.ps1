# Script para instalar pre-commit y sus dependencias
# Uso: .\scripts\install_precommit_deps.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Instalando pre-commit y dependencias para el proyecto CALLi..." -ForegroundColor $Cyan
Write-Host "============================================================" -ForegroundColor $Cyan

# Verificar si pip está instalado
try {
    pip --version | Out-Null
}
catch {
    Write-Host "Error: pip no está instalado o no está en el PATH." -ForegroundColor $Red
    Write-Host "Por favor, instale Python y pip antes de continuar." -ForegroundColor $Red
    exit 1
}

# Instalar pre-commit
Write-Host "`nInstalando pre-commit..." -ForegroundColor $Yellow
pip install pre-commit
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al instalar pre-commit." -ForegroundColor $Red
    exit 1
}

# Instalar dependencias de Python para los hooks
Write-Host "`nInstalando dependencias de Python para los hooks..." -ForegroundColor $Yellow
pip install mypy ruff bandit safety docutils restructuredtext-lint
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al instalar dependencias de Python." -ForegroundColor $Red
    exit 1
}

# Instalar gitleaks
Write-Host "`nInstalando gitleaks..." -ForegroundColor $Yellow
& .\scripts\install_gitleaks.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al instalar gitleaks. Continuando de todos modos..." -ForegroundColor $Yellow
}

# Instalar KICS
Write-Host "`nInstalando KICS..." -ForegroundColor $Yellow
& .\scripts\install_kics.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al instalar KICS. Continuando de todos modos..." -ForegroundColor $Yellow
}

# Instalar hooks de pre-commit
Write-Host "`nInstalando hooks de pre-commit..." -ForegroundColor $Yellow
pre-commit install --install-hooks
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al instalar hooks de pre-commit." -ForegroundColor $Red
    exit 1
}

# Instalar hooks adicionales
Write-Host "`nInstalando hooks adicionales (pre-push)..." -ForegroundColor $Yellow
pre-commit install --hook-type pre-push
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error al instalar hooks de pre-push." -ForegroundColor $Red
    exit 1
}

# Ejecutar pre-commit en todos los archivos para verificar la instalación
Write-Host "`nVerificando la instalación de pre-commit..." -ForegroundColor $Yellow
pre-commit run --all-files
$precommitExitCode = $LASTEXITCODE

if ($precommitExitCode -eq 0) {
    Write-Host "`n✓ Pre-commit instalado y configurado correctamente." -ForegroundColor $Green
}
else {
    Write-Host "`n⚠ Pre-commit instalado, pero algunas verificaciones fallaron." -ForegroundColor $Yellow
    Write-Host "Esto es normal en la primera ejecución. Los problemas detectados deben corregirse antes de hacer commit." -ForegroundColor $Yellow
}

Write-Host "`nPara usar pre-commit:" -ForegroundColor $Cyan
Write-Host "1. Los hooks se ejecutarán automáticamente al hacer git commit" -ForegroundColor $Cyan
Write-Host "2. Para ejecutar manualmente: pre-commit run --all-files" -ForegroundColor $Cyan
Write-Host "3. Para omitir los hooks en un commit específico: git commit --no-verify" -ForegroundColor $Cyan

exit 0
