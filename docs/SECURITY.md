# Seguridad en CALLi

Este documento describe las prácticas de seguridad implementadas en el proyecto CALLi y proporciona guías para mantener un alto nivel de seguridad en el desarrollo y despliegue.

## Principios de Seguridad

CALLi sigue estos principios fundamentales de seguridad:

1. **Defensa en profundidad**: Múltiples capas de seguridad para proteger los datos y sistemas
2. **Mínimo privilegio**: Acceso limitado solo a lo necesario para cada función
3. **Seguridad por diseño**: Consideraciones de seguridad desde el inicio del desarrollo
4. **Actualizaciones regulares**: Mantener todas las dependencias actualizadas
5. **Monitoreo continuo**: Detección temprana de posibles problemas de seguridad

## Herramientas de Seguridad

### Scripts de Verificación Automatizados

Hemos implementado un conjunto completo de scripts para verificar la seguridad del proyecto:

```bash
# Ejecutar todas las verificaciones
./scripts/run_all_checks.sh  # Linux/macOS
.\scripts\run_all_checks.ps1  # Windows
```

Este script maestro ejecuta todas las verificaciones de seguridad y genera informes detallados en el directorio `reports/`.

### Verificación de Formato y Estilo

```bash
# Verificar y corregir formato con Ruff
./scripts/run_ruff.sh --fix  # Linux/macOS
.\scripts\run_ruff.ps1 -fix  # Windows
```

### Verificación de Tipos con mypy

La verificación estática de tipos ayuda a prevenir errores que podrían llevar a vulnerabilidades:

```bash
# Ejecutar verificación de tipos
./scripts/run_mypy.sh  # Linux/macOS
.\scripts\run_mypy.ps1  # Windows
```

### Verificación de Documentación

```bash
# Verificar docstrings
./scripts/run_docstring_check.sh  # Linux/macOS
.\scripts\run_docstring_check.ps1  # Windows

# Verificar documentación RST
./scripts/run_rst_check.sh  # Linux/macOS
.\scripts\run_rst_check.ps1  # Windows
```

### Verificación de Dependencias

```bash
# Verificar dependencias JavaScript
./scripts/check_js_dependencies.sh  # Linux/macOS
.\scripts\check_js_dependencies.ps1  # Windows
```

### Pre-commit

Utilizamos pre-commit para verificar el código antes de cada commit, lo que ayuda a prevenir problemas de seguridad comunes:

```bash
# Instalar pre-commit
pip install pre-commit

# Instalar los hooks
pre-commit install

# Ejecutar en todos los archivos
pre-commit run --all-files
```

Los hooks configurados incluyen:

- Detección de secretos con Gitleaks
- Verificación de dependencias con Safety
- Análisis estático con Bandit
- Verificación de sintaxis y estilo

### KICS (Keeping Infrastructure as Code Secure)

KICS es una herramienta de análisis estático para código de infraestructura que ayuda a identificar vulnerabilidades de seguridad:

```bash
# Instalar KICS
bash scripts/install_kics.sh

# Ejecutar escaneo
kics scan -p . --config .kics.config -o security-reports
```

## Prácticas de Seguridad en el Código

### Manejo de Secretos

- **NO** incluir secretos o credenciales en el código fuente
- Utilizar variables de entorno para configuraciones sensibles
- Usar `.env` para desarrollo local (incluido en `.gitignore`)
- Utilizar gestores de secretos para entornos de producción

### Validación de Entrada

- Validar todas las entradas de usuario con Pydantic
- Implementar límites apropiados para prevenir ataques de denegación de servicio
- Sanitizar datos antes de almacenarlos o procesarlos

### Autenticación y Autorización

- Implementar autenticación multifactor cuando sea posible
- Utilizar tokens JWT con tiempos de expiración adecuados
- Verificar permisos en cada endpoint de la API
- Implementar bloqueo de cuentas después de múltiples intentos fallidos

## CI/CD y Seguridad

Nuestro pipeline de CI/CD incluye verificaciones de seguridad automatizadas:

1. **Escaneo de dependencias**: Verificación de vulnerabilidades conocidas
2. **Análisis estático**: Detección de problemas de seguridad en el código
3. **Pruebas de seguridad**: Verificación de configuraciones seguras
4. **Escaneo de secretos**: Prevención de filtración de credenciales
5. **Verificación de formato**: Asegurar que el código sigue las mejores prácticas
6. **Verificación de tipos**: Prevenir errores de tipo que podrían causar vulnerabilidades
7. **Verificación de documentación**: Asegurar que el código está bien documentado

Hemos implementado un nuevo workflow de GitHub Actions (`security-checks-improved.yml`) que ejecuta todas estas verificaciones automáticamente.

## Reportar Vulnerabilidades

Si descubres una vulnerabilidad de seguridad en CALLi, por favor:

1. **NO** la divulgues públicamente
2. Envía un correo a [security@example.com](mailto:security@example.com) con los detalles
3. Incluye pasos para reproducir el problema
4. Si es posible, sugiere una solución o mitigación

Agradecemos tu ayuda para mantener CALLi seguro.

## Recursos Adicionales

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Python Security Best Practices](https://snyk.io/blog/python-security-best-practices-cheat-sheet/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [Next.js Security Documentation](https://nextjs.org/docs/advanced-features/security-headers)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)
- [KICS Documentation](https://docs.kics.io/)
- [Gitleaks Documentation](https://github.com/zricethezav/gitleaks)

## Historial de Mejoras de Seguridad

### 2023-11-15: Mejoras en la Verificación de Seguridad

- Implementación de scripts automatizados para verificar la seguridad del proyecto
- Mejora de la configuración para excluir falsos positivos
- Actualización de la documentación de seguridad
- Implementación de un nuevo workflow de GitHub Actions para verificaciones de seguridad
