# Guía de Contribución

¡Gracias por tu interés en contribuir a CALLi! Esta guía te ayudará a entender el proceso de contribución y los estándares de seguridad que debemos mantener.

## Proceso de Contribución

1. **Fork** el repositorio en GitHub
2. **Clona** tu fork a tu máquina local
3. **Crea una rama** para tu contribución (`git checkout -b feature/amazing-feature`)
4. **Realiza tus cambios** siguiendo las guías de estilo y seguridad
5. **Ejecuta las pruebas** para asegurarte de que todo funciona correctamente
6. **Commit** tus cambios (`git commit -m 'Add amazing feature'`)
7. **Push** a tu rama (`git push origin feature/amazing-feature`)
8. Abre un **Pull Request** desde tu rama a la rama principal del repositorio original

## Estándares de Seguridad

Al contribuir código, asegúrate de seguir estas prácticas de seguridad:

### Autenticación y Autorización

- Nunca almacenes contraseñas en texto plano
- Utiliza algoritmos de hash seguros (bcrypt, Argon2) para almacenar contraseñas
- Implementa el principio de privilegio mínimo para los permisos
- Asegúrate de que los tokens tengan un tiempo de expiración adecuado

### Manejo de Datos

- Cifra los datos sensibles tanto en reposo como en tránsito
- Valida todas las entradas de usuario para prevenir inyecciones
- Sanitiza las salidas para prevenir ataques XSS
- No incluyas datos sensibles en registros (logs) o mensajes de error

### Gestión de Dependencias

- Mantén las dependencias actualizadas
- Verifica las vulnerabilidades conocidas en las dependencias
- Utiliza versiones específicas de las dependencias para evitar cambios inesperados

### Código Seguro

- Evita usar funciones obsoletas o inseguras
- Maneja adecuadamente los errores sin revelar información sensible
- No incluyas credenciales, tokens o secretos en el código fuente
- Utiliza consultas parametrizadas para acceder a bases de datos

## Revisión de Código

Todos los Pull Requests serán revisados para asegurar que cumplan con los estándares de calidad y seguridad. La revisión incluirá:

- Verificación de funcionalidad
- Revisión de seguridad
- Análisis de calidad del código
- Comprobación de pruebas

## Pruebas

Asegúrate de incluir pruebas para tu código. Deberías:

- Escribir pruebas unitarias para la lógica de negocio
- Incluir pruebas de integración cuando sea necesario
- Verificar que todas las pruebas existentes pasen con tus cambios
- Considerar casos límite y escenarios de error

## Informar Problemas de Seguridad

Si descubres un problema de seguridad, por favor NO lo reportes como un issue público. Sigue el proceso descrito en nuestro archivo [SECURITY.md](../SECURITY.md).

## Licencia

Al contribuir a este proyecto, aceptas que tus contribuciones estarán bajo la misma licencia que el proyecto original.
