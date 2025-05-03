# Script para corregir finales de línea en archivos del proyecto CALLi
# Este script normaliza los finales de línea a LF (estilo Unix)

$Yellow = "Yellow"
$Green = "Green"
$Red = "Red"
$Cyan = "Cyan"

Write-Host "=====================================================" -ForegroundColor $Cyan
Write-Host "      Corrección de Finales de Línea para CALLi      " -ForegroundColor $Cyan
Write-Host "=====================================================" -ForegroundColor $Cyan
Write-Host ""

# Verificar si git está instalado
try {
    $gitVersion = git --version
    Write-Host "Git detectado: $gitVersion" -ForegroundColor $Green
}
catch {
    Write-Host "Error: Git no está instalado o no está en el PATH." -ForegroundColor $Red
    Write-Host "Por favor, instale Git y asegúrese de que esté en el PATH del sistema." -ForegroundColor $Red
    exit 1
}

# Crear o actualizar .gitattributes si no existe
$gitattributesPath = ".gitattributes"
if (-not (Test-Path $gitattributesPath)) {
    Write-Host "Creando archivo .gitattributes para normalizar finales de línea..." -ForegroundColor $Yellow
    
    @"
# Configuración de finales de línea para el proyecto CALLi
# Establecer el comportamiento predeterminado para todos los archivos
* text=auto eol=lf

# Archivos de texto que siempre deben normalizarse y convertirse a LF
*.py text eol=lf
*.js text eol=lf
*.jsx text eol=lf
*.ts text eol=lf
*.tsx text eol=lf
*.json text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.md text eol=lf
*.rst text eol=lf
*.txt text eol=lf
*.html text eol=lf
*.css text eol=lf
*.scss text eol=lf
*.sh text eol=lf
*.ps1 text eol=lf
*.sql text eol=lf
*.toml text eol=lf
*.ini text eol=lf
*.cfg text eol=lf
*.bat text eol=crlf

# Archivos binarios que no deben modificarse
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.svg binary
*.woff binary
*.woff2 binary
*.ttf binary
*.eot binary
*.mp3 binary
*.mp4 binary
*.zip binary
*.gz binary
*.tar binary
*.pdf binary
*.xls binary
*.xlsx binary
*.doc binary
*.docx binary
*.ppt binary
*.pptx binary
"@ | Out-File -FilePath $gitattributesPath -Encoding utf8
    
    Write-Host "Archivo .gitattributes creado correctamente." -ForegroundColor $Green
}
else {
    Write-Host "El archivo .gitattributes ya existe." -ForegroundColor $Green
}

# Normalizar finales de línea en el repositorio
Write-Host "`nNormalizando finales de línea en el repositorio..." -ForegroundColor $Yellow

# Configurar Git para manejar correctamente los finales de línea
git config core.autocrlf false
git config core.eol lf

# Usar git para normalizar los finales de línea
Write-Host "Aplicando normalización de finales de línea a todos los archivos..." -ForegroundColor $Yellow
git add --renormalize .

# Verificar si hay cambios
$changes = git status --porcelain
if ($changes) {
    Write-Host "`nSe han normalizado los finales de línea en los siguientes archivos:" -ForegroundColor $Green
    git status --porcelain | ForEach-Object {
        Write-Host $_ -ForegroundColor $Cyan
    }
    
    Write-Host "`nPara aplicar estos cambios, ejecute:" -ForegroundColor $Yellow
    Write-Host "git commit -m 'fix: normalizar finales de línea'" -ForegroundColor $Cyan
}
else {
    Write-Host "`nNo se detectaron problemas de finales de línea en los archivos." -ForegroundColor $Green
}

Write-Host "`n=====================================================" -ForegroundColor $Cyan
Write-Host "      Proceso de normalización completado            " -ForegroundColor $Cyan
Write-Host "=====================================================" -ForegroundColor $Cyan
