# Script para verificar la configuración de GitHub Actions
Write-Host "Verificación de la configuración de GitHub Actions para despliegue" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Verificar archivos de workflow
$workflowFiles = @(
    ".github\workflows\deploy.yml",
    ".github\workflows\deploy-fixed.yml"
)

foreach ($file in $workflowFiles) {
    if (Test-Path $file) {
        Write-Host "Archivo de workflow encontrado: $file" -ForegroundColor Green

        # Verificar secretos utilizados
        $content = Get-Content $file -Raw
        $secretsToCheck = @(
            "DEPLOY_HOST",
            "DEPLOY_USERNAME",
            "DEPLOY_KEY"
        )

        Write-Host "Verificando secretos utilizados:" -ForegroundColor Yellow
        foreach ($secret in $secretsToCheck) {
            if ($content -match "\`${{ secrets.$secret }}") {
                Write-Host "  - $secret: Utilizado en el workflow" -ForegroundColor Green
            } else {
                Write-Host "  - $secret: No encontrado en el workflow" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "Archivo de workflow no encontrado: $file" -ForegroundColor Yellow
    }
}

Write-Host "`nPasos para configurar los secretos en GitHub:" -ForegroundColor Cyan
Write-Host "1. Ve a tu repositorio en GitHub" -ForegroundColor Yellow
Write-Host "2. Haz clic en 'Settings' (Configuración)" -ForegroundColor Yellow
Write-Host "3. En el menú lateral, haz clic en 'Secrets and variables' > 'Actions'" -ForegroundColor Yellow
Write-Host "4. Haz clic en 'New repository secret'" -ForegroundColor Yellow
Write-Host "5. Configura los siguientes secretos:" -ForegroundColor Yellow
Write-Host "   - DEPLOY_HOST: La dirección IP o nombre de dominio de tu servidor" -ForegroundColor Yellow
Write-Host "   - DEPLOY_USERNAME: El nombre de usuario para conectarse al servidor" -ForegroundColor Yellow
Write-Host "   - DEPLOY_KEY: El contenido de tu clave SSH privada (C:\Users\marti\.ssh\id_rsa)" -ForegroundColor Yellow
Write-Host "     IMPORTANTE: Asegúrate de incluir TODO el contenido de la clave, incluyendo las líneas" -ForegroundColor Red
Write-Host "     '-----BEGIN OPENSSH PRIVATE KEY-----' y '-----END OPENSSH PRIVATE KEY-----'" -ForegroundColor Red

Write-Host "`nPara obtener el contenido de tu clave privada, puedes ejecutar:" -ForegroundColor Cyan
Write-Host "Get-Content C:\Users\marti\.ssh\id_rsa" -ForegroundColor Yellow
