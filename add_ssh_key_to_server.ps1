# Script para añadir clave SSH al servidor
param (
    [Parameter(Mandatory=$true)]
    [string]$Usuario,

    [Parameter(Mandatory=$true)]
    [string]$Servidor,

    [Parameter(Mandatory=$false)]
    [string]$Puerto = "22"
)

# Verificar que el archivo de clave pública existe
if (-not (Test-Path "clave_publica.txt")) {
    Write-Error "No se encontró el archivo clave_publica.txt"
    exit 1
}

# Mostrar instrucciones
Write-Host "Este script te ayudará a añadir tu clave SSH al servidor $Servidor" -ForegroundColor Cyan
Write-Host "Opciones disponibles:" -ForegroundColor Cyan
Write-Host "1. Usar ssh-copy-id (requiere Git Bash u otro cliente SSH con esta herramienta)" -ForegroundColor Green
Write-Host "2. Conexión manual (te guiaré paso a paso)" -ForegroundColor Green
Write-Host "3. Usar SCP y SSH (método automático, requiere acceso SSH actual)" -ForegroundColor Green

$opcion = Read-Host "Selecciona una opción (1-3)"

switch ($opcion) {
    "1" {
        Write-Host "Para usar ssh-copy-id, abre Git Bash y ejecuta:" -ForegroundColor Yellow
        Write-Host "ssh-copy-id -i $((Get-Location).Path)\clave_publica.txt $Usuario@$Servidor -p $Puerto" -ForegroundColor Yellow
    }
    "2" {
        Write-Host "Instrucciones para conexión manual:" -ForegroundColor Yellow
        Write-Host "1. Conéctate al servidor: ssh $Usuario@$Servidor -p $Puerto" -ForegroundColor Yellow
        Write-Host "2. Ejecuta: mkdir -p ~/.ssh && chmod 700 ~/.ssh" -ForegroundColor Yellow
        Write-Host "3. Ejecuta: touch ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys" -ForegroundColor Yellow
        Write-Host "4. Abre el archivo clave_publica.txt en este directorio" -ForegroundColor Yellow
        Write-Host "5. Copia su contenido y añádelo al archivo ~/.ssh/authorized_keys en el servidor" -ForegroundColor Yellow
        Write-Host "   Puedes usar: nano ~/.ssh/authorized_keys" -ForegroundColor Yellow
        Write-Host "6. Guarda el archivo (en nano: Ctrl+O, Enter, Ctrl+X)" -ForegroundColor Yellow
        Write-Host "7. Prueba la conexión: ssh $Usuario@$Servidor -p $Puerto" -ForegroundColor Yellow
    }
    "3" {
        Write-Host "Intentando método automático con SCP y SSH..." -ForegroundColor Yellow

        # Intentar crear directorio .ssh en el servidor
        Write-Host "Creando directorio .ssh en el servidor..." -ForegroundColor Yellow
        ssh -p $Puerto $Usuario@$Servidor "mkdir -p ~/.ssh && chmod 700 ~/.ssh"

        if ($LASTEXITCODE -ne 0) {
            Write-Error "No se pudo conectar al servidor o crear el directorio .ssh"
            exit 1
        }

        # Copiar la clave al servidor
        Write-Host "Copiando clave pública al servidor..." -ForegroundColor Yellow
        scp -P $Puerto clave_publica.txt $Usuario@$Servidor:~/

        if ($LASTEXITCODE -ne 0) {
            Write-Error "No se pudo copiar la clave al servidor"
            exit 1
        }

        # Añadir la clave al archivo authorized_keys
        Write-Host "Añadiendo clave al archivo authorized_keys..." -ForegroundColor Yellow
        ssh -p $Puerto $Usuario@$Servidor "cat ~/clave_publica.txt >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && rm ~/clave_publica.txt"

        if ($LASTEXITCODE -ne 0) {
            Write-Error "No se pudo añadir la clave al archivo authorized_keys"
            exit 1
        }

        Write-Host "¡Clave añadida correctamente!" -ForegroundColor Green
        Write-Host "Prueba la conexión: ssh $Usuario@$Servidor -p $Puerto" -ForegroundColor Yellow
    }
    default {
        Write-Error "Opción no válida"
        exit 1
    }
}
