# Script para verificar si Node.js está instalado
# Uso: .\scripts\check_nodejs.ps1

# Colores para la salida
$Green = [ConsoleColor]::Green
$Red = [ConsoleColor]::Red
$Yellow = [ConsoleColor]::Yellow
$Cyan = [ConsoleColor]::Cyan

Write-Host "Verificando instalación de Node.js..." -ForegroundColor $Cyan

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

if ($nodeInstalled -and $npmInstalled) {
    Write-Host "Node.js está instalado correctamente:" -ForegroundColor $Green
    Write-Host "- Node.js: $nodeInstalled" -ForegroundColor $Green
    Write-Host "- npm: $npmInstalled" -ForegroundColor $Green
    exit 0
} else {
    Write-Host "Node.js no está instalado o no está en el PATH." -ForegroundColor $Red
    Write-Host "Por favor, instale Node.js siguiendo estos pasos:" -ForegroundColor $Yellow
    Write-Host "1. Descargue el instalador de Node.js desde https://nodejs.org/" -ForegroundColor $Yellow
    Write-Host "2. Ejecute el instalador y siga las instrucciones" -ForegroundColor $Yellow
    Write-Host "3. Reinicie su terminal después de la instalación" -ForegroundColor $Yellow
    Write-Host "4. Verifique la instalación ejecutando 'node --version' y 'npm --version'" -ForegroundColor $Yellow

    # Preguntar si desea abrir el sitio web de Node.js
    $openWebsite = Read-Host "¿Desea abrir el sitio web de Node.js ahora? (s/n)"
    if ($openWebsite -eq "s") {
        Start-Process "https://nodejs.org/"
    }

    exit 1
}
