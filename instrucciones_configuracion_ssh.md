# Configuración de SSH para Despliegue Automático

Este documento proporciona instrucciones detalladas para configurar correctamente la autenticación SSH para el despliegue automático de tu aplicación mediante GitHub Actions.

## 1. Añadir tu Clave Pública al Servidor

Para que GitHub Actions pueda conectarse a tu servidor, necesitas añadir la clave pública correspondiente a la clave privada que configurarás como secreto en GitHub.

### Opción 1: Usando el Script Automatizado

1. Abre PowerShell en este directorio
2. Ejecuta el script:
   ```powershell
   .\add_ssh_key_to_server.ps1 -Usuario "tu_usuario" -Servidor "tu_servidor" -Puerto "22"
   ```
3. Sigue las instrucciones que aparecen en pantalla

### Opción 2: Conexión Manual al Servidor

1. Conéctate a tu servidor usando tu método actual (contraseña u otra clave):
   ```bash
   ssh tu_usuario@tu_servidor
   ```

2. Crea el directorio `.ssh` si no existe:
   ```bash
   mkdir -p ~/.ssh && chmod 700 ~/.ssh
   ```

3. Crea o edita el archivo `authorized_keys`:
   ```bash
   nano ~/.ssh/authorized_keys
   ```

4. Pega el contenido del archivo `clave_publica.txt` al final del archivo
5. Guarda el archivo (en nano: Ctrl+O, Enter, Ctrl+X)
6. Establece los permisos correctos:
   ```bash
   chmod 600 ~/.ssh/authorized_keys
   ```

### Opción 3: Usando ssh-copy-id (si tienes Git Bash u otro cliente SSH con esta herramienta)

1. Abre Git Bash
2. Ejecuta el comando:
   ```bash
   ssh-copy-id -i ./clave_publica.txt tu_usuario@tu_servidor
   ```

## 2. Configurar los Secretos en GitHub

Para que el workflow de GitHub Actions funcione correctamente, necesitas configurar los siguientes secretos:

1. Ve a tu repositorio en GitHub
2. Haz clic en "Settings" (Configuración)
3. En el menú lateral, haz clic en "Secrets and variables" > "Actions"
4. Haz clic en "New repository secret"
5. Configura los siguientes secretos:

   - **DEPLOY_HOST**: La dirección IP o nombre de dominio de tu servidor
   - **DEPLOY_USERNAME**: El nombre de usuario para conectarse al servidor
   - **DEPLOY_KEY**: El contenido de tu clave SSH privada (C:\Users\marti\.ssh\id_rsa)

     **IMPORTANTE**: Asegúrate de incluir TODO el contenido de la clave, incluyendo las líneas
     '-----BEGIN OPENSSH PRIVATE KEY-----' y '-----END OPENSSH PRIVATE KEY-----'

Para obtener el contenido de tu clave privada, puedes ejecutar:
```powershell
Get-Content C:\Users\marti\.ssh\id_rsa
```

## 3. Verificar la Configuración

1. Prueba la conexión SSH al servidor:
   ```bash
   ssh tu_usuario@tu_servidor
   ```
   Si la conexión se establece sin solicitar contraseña, la configuración es correcta.

2. Verifica la configuración de GitHub Actions ejecutando:
   ```powershell
   .\verify_github_actions_config.ps1
   ```

## 4. Ejecutar el Workflow de Despliegue

Una vez configurado todo correctamente:

1. Realiza un cambio en tu repositorio
2. Haz commit y push a la rama principal (main o master)
3. El workflow de despliegue se ejecutará automáticamente

También puedes ejecutar el workflow manualmente desde la pestaña "Actions" en GitHub.

## Solución de Problemas

Si encuentras problemas durante el despliegue, verifica:

1. Los logs de GitHub Actions para identificar el error específico
2. Que la clave pública esté correctamente añadida al archivo `~/.ssh/authorized_keys` del servidor
3. Que los secretos en GitHub estén correctamente configurados
4. Que el servidor sea accesible desde Internet (puertos abiertos, firewall configurado, etc.)
5. Que el usuario tenga permisos suficientes en el servidor para realizar las operaciones necesarias

Si el problema persiste, puedes probar a conectarte manualmente al servidor usando la misma clave privada para verificar que funciona correctamente.
