# Seguridad en CALLi

Este documento proporciona una guía sobre las prácticas de seguridad implementadas en el proyecto CALLi y cómo mantener un alto nivel de seguridad en el desarrollo.

## Verificaciones de Seguridad

El proyecto CALLi implementa varias capas de verificación de seguridad:

1. **Pre-commit hooks**: Verificaciones automáticas antes de cada commit
2. **GitHub Actions**: Flujos de trabajo automatizados para verificar la seguridad
3. **Scripts locales**: Herramientas para verificar la seguridad localmente

## Cómo ejecutar verificaciones de seguridad localmente

### Requisitos previos

Antes de ejecutar las verificaciones de seguridad, asegúrate de tener instaladas las siguientes herramientas:

```bash
# Instalar dependencias de Python
pip install pre-commit safety bandit detect-secrets

# Instalar Node.js y npm (si no están instalados)
# Visita https://nodejs.org/ para descargar e instalar Node.js
```

### Usando pre-commit

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar los hooks
pre-commit install

# Ejecutar todas las verificaciones manualmente
pre-commit run --all-files
```

### Usando el script de verificación de seguridad

```bash
# Ejecutar el script de verificación de seguridad
python scripts/security_check_local.py
```

### Solución de problemas comunes

Si encuentras errores al ejecutar el script de verificación de seguridad:

1. **Error con safety**: Instala safety manualmente con `pip install safety`
2. **Error con npm**: Instala Node.js desde [nodejs.org](https://nodejs.org/)
3. **Error con detect-secrets**: Instala detect-secrets con `pip install detect-secrets`

## Archivos de seguridad requeridos

El proyecto CALLi requiere los siguientes archivos de seguridad:

- `SECURITY.md`: Política de seguridad
- `CODE_OF_CONDUCT.md`: Código de conducta
- `.github/CONTRIBUTING.md`: Guía de contribución
- `.github/PULL_REQUEST_TEMPLATE.md`: Plantilla de Pull Request
- `.github/ISSUE_TEMPLATE/security_issue.md`: Plantilla de Issue de Seguridad
- `.github/workflows/codeql-analysis.yml`: Flujo de trabajo de CodeQL
- `.github/dependabot.yml`: Configuración de Dependabot
- `.github/workflows/secret-scanning.yml`: Flujo de trabajo de escaneo de secretos

## Encabezados de seguridad requeridos

El archivo `nginx/conf.d/default.conf` debe incluir los siguientes encabezados de seguridad:

- `Strict-Transport-Security`
- `X-Content-Type-Options`
- `X-Frame-Options`
- `Content-Security-Policy`

## Mejores prácticas de seguridad

### Gestión de dependencias

- Mantener todas las dependencias actualizadas
- Verificar regularmente las vulnerabilidades con `safety` (Python) y `npm audit` (JavaScript)
- Utilizar versiones específicas de las dependencias

### Código seguro

- No incluir credenciales, tokens o secretos en el código fuente
- Validar todas las entradas de usuario
- Sanitizar todas las salidas para prevenir ataques XSS
- Utilizar consultas parametrizadas para acceder a bases de datos

### Autenticación y autorización

- Implementar el principio de privilegio mínimo
- Utilizar algoritmos de hash seguros para almacenar contraseñas
- Asegurarse de que los tokens tengan un tiempo de expiración adecuado

## Resolución de problemas en CI/CD

### Fallos en los flujos de trabajo de GitHub Actions

Si los flujos de trabajo de seguridad fallan en GitHub Actions:

1. Ejecuta las verificaciones localmente para identificar el problema
2. Corrige los problemas identificados
3. Verifica que todos los archivos de seguridad requeridos existan
4. Asegúrate de que los encabezados de seguridad estén configurados correctamente

### Problemas con dependencias

Si se encuentran vulnerabilidades en las dependencias:

1. Actualiza las dependencias afectadas
2. Si no es posible actualizar, evalúa el impacto de la vulnerabilidad
3. Implementa mitigaciones si es necesario

## Recursos adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
