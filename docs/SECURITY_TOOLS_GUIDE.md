# Guía de Herramientas de Seguridad para CALLi

Este documento describe las herramientas de seguridad implementadas en el proyecto CALLi y cómo utilizarlas correctamente.

## Herramientas de Verificación de Seguridad

### 1. Verificación de Seguridad Completa

Para ejecutar una verificación completa de seguridad en el proyecto:

```powershell
# Windows
.\scripts\run_security_checks.ps1

# Linux/macOS
./scripts/run_security_checks.sh
```

Este script realiza las siguientes verificaciones:
- Configuración de seguridad
- Vulnerabilidades en dependencias Python
- Vulnerabilidades en dependencias JavaScript
- Detección de secretos en el código
- Verificación de encabezados de seguridad HTTP

### 2. Verificación de Configuración

Para verificar específicamente la configuración de seguridad:

```powershell
# Windows
.\scripts\verify_config_security.ps1

# Linux/macOS
./scripts/verify_config_security.sh
```

### 3. Verificación de Encabezados HTTP

Para verificar los encabezados de seguridad HTTP:

```powershell
# Windows
.\scripts\run_security_headers_check.ps1

# Linux/macOS
python ./scripts/check_security_headers.py
```

### 4. Detección de Secretos

Para detectar secretos en el código:

```powershell
# Windows
.\scripts\run_gitleaks.ps1

# Linux/macOS
./scripts/run_gitleaks.sh
```

## Buenas Prácticas de Seguridad

### Manejo de Secretos

1. **Nunca incluir secretos en el código**:
   - No incluir API keys, tokens, contraseñas o cualquier información sensible directamente en el código.
   - Utilizar variables de entorno o servicios de gestión de secretos.

2. **Archivos .env**:
   - Nunca hacer commit de archivos `.env` que contengan secretos reales.
   - Utilizar `.env.example` como plantilla, sin incluir valores reales.
   - Asegurarse de que todos los archivos `.env*` (excepto `.env.example`) estén en `.gitignore`.

3. **Enmascaramiento de Secretos**:
   - Utilizar la función `mask_secret` de `scripts/security_check_local.py` para enmascarar secretos en logs.
   - Ejemplo: `logger.info(f"Conectando con API key: {mask_secret(api_key)}")`

### Configuración de Pre-commit

Para configurar pre-commit y ejecutar verificaciones de seguridad antes de cada commit:

```powershell
# Instalar pre-commit
pip install pre-commit

# Instalar los hooks de pre-commit
pre-commit install

# Verificar la instalación
pre-commit run --all-files
```

El archivo `.pre-commit-config.yaml` ya está configurado para ejecutar:
- Verificación de secretos con gitleaks
- Verificación de formato con Ruff
- Verificación de tipos con MyPy
- Verificación de seguridad básica con Bandit

## Recursos Adicionales

- [Documentación de Seguridad Completa](./SECURITY.md)
- [Plan de Pruebas de Seguridad](../SECURITY_TEST_PLAN.md)
- [Guía de Autenticación](./security/authentication-guide.md)
- [Visión General de Seguridad](./security/security-overview.md)

## Contacto

Si encuentras algún problema de seguridad, por favor contacta inmediatamente a:
- Santiago Martínez <santiago@xor.com.ar>
