# Lista de Verificación de Seguridad

Esta lista de verificación debe ser revisada antes de cada lanzamiento importante o despliegue en producción.

## Autenticación y Autorización

- [ ] Implementar autenticación multifactor (MFA) para accesos críticos
- [ ] Verificar que los tokens JWT tengan un tiempo de expiración adecuado
- [ ] Asegurar que los permisos de usuario estén correctamente implementados
- [ ] Verificar que las contraseñas se almacenen con hash seguro (bcrypt/Argon2)
- [ ] Comprobar que las sesiones se invaliden correctamente al cerrar sesión

## Protección de Datos

- [ ] Verificar que los datos sensibles estén cifrados en reposo
- [ ] Asegurar que las comunicaciones utilicen TLS 1.2+ (HTTPS)
- [ ] Comprobar que no haya credenciales en el código fuente
- [ ] Verificar que las copias de seguridad estén cifradas
- [ ] Asegurar que los datos personales se manejen según las regulaciones (GDPR, etc.)

## Seguridad de API

- [ ] Implementar límites de velocidad (rate limiting) para prevenir abusos
- [ ] Verificar que las respuestas de error no revelen información sensible
- [ ] Asegurar que los encabezados de seguridad estén configurados correctamente
- [ ] Comprobar que la validación de entrada esté implementada para todos los parámetros
- [ ] Verificar que CORS esté configurado adecuadamente

## Seguridad de Infraestructura

- [ ] Asegurar que los firewalls estén correctamente configurados
- [ ] Verificar que solo los puertos necesarios estén abiertos
- [ ] Comprobar que los registros (logs) de seguridad estén habilitados
- [ ] Asegurar que las actualizaciones de seguridad estén aplicadas
- [ ] Verificar que los contenedores Docker utilicen imágenes base seguras

## Seguridad de Dependencias

- [ ] Ejecutar análisis de vulnerabilidades en dependencias
- [ ] Verificar que no haya bibliotecas obsoletas o sin mantenimiento
- [ ] Comprobar que las licencias de software cumplan con la política de la empresa
- [ ] Asegurar que las dependencias se obtengan de fuentes confiables
- [ ] Verificar que las versiones de dependencias estén fijadas (pinned)

## Seguridad de Código

- [ ] Ejecutar análisis estático de código (SAST)
- [ ] Verificar que no haya vulnerabilidades de inyección (SQL, XSS, etc.)
- [ ] Comprobar que no haya secretos o tokens en el código
- [ ] Asegurar que las revisiones de código incluyan aspectos de seguridad
- [ ] Verificar que los errores se manejen adecuadamente sin revelar información sensible

## Monitoreo y Respuesta

- [ ] Implementar monitoreo de seguridad continuo
- [ ] Verificar que las alertas de seguridad estén configuradas
- [ ] Comprobar que exista un plan de respuesta a incidentes
- [ ] Asegurar que los registros de auditoría estén habilitados
- [ ] Verificar que se realicen copias de seguridad regulares

## Pruebas de Seguridad

- [ ] Ejecutar pruebas de penetración (pentest)
- [ ] Verificar que se realicen análisis de vulnerabilidades regulares
- [ ] Comprobar que las pruebas de seguridad estén automatizadas en CI/CD
- [ ] Asegurar que se realicen pruebas de fuzzing en entradas críticas
- [ ] Verificar que se prueben escenarios de ataque comunes (OWASP Top 10)
