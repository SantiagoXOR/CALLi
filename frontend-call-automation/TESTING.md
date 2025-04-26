# Estrategia de Pruebas - Proyecto de Automatización de Llamadas

Este documento describe la estrategia de pruebas implementada en el proyecto de automatización de llamadas, incluyendo pruebas unitarias, de integración y end-to-end.

## Estructura de Pruebas

El proyecto utiliza diferentes niveles de pruebas para garantizar la calidad del código:

1. **Pruebas Unitarias**: Prueban componentes y servicios de forma aislada.
2. **Pruebas de Integración**: Prueban la interacción entre componentes.
3. **Pruebas End-to-End**: Prueban flujos completos de la aplicación.

## Tecnologías Utilizadas

- **Jest**: Framework de pruebas principal
- **React Testing Library**: Biblioteca para probar componentes de React
- **Cypress**: Framework para pruebas end-to-end
- **MSW (Mock Service Worker)**: Para simular respuestas de API
- **GitHub Actions**: Para integración continua
- **Codecov**: Para análisis de cobertura de código

## Pruebas Unitarias y de Integración

### Ubicación de los Archivos

Las pruebas unitarias y de integración se encuentran en los siguientes directorios:

- `src/components/__tests__/`: Pruebas para componentes de UI
- `src/services/__tests__/`: Pruebas para servicios de API

### Ejecución de Pruebas

Para ejecutar las pruebas unitarias y de integración:

```bash
# Ejecutar todas las pruebas
npm test

# Ejecutar pruebas en modo watch
npm run test:watch

# Generar informe de cobertura
npm run test:coverage
```

### Mocks

Las pruebas utilizan mocks para simular dependencias externas:

- **Axios**: Se mockea para simular llamadas a API
- **React Query**: Se mockea para simular estados de carga y datos
- **Servicios**: Se mockean para aislar componentes

Los mocks se encuentran en:
- `src/__mocks__/`: Mocks globales
- Mocks inline en los archivos de prueba

### Selectores

Las pruebas utilizan selectores robustos basados en:

- Roles de accesibilidad (`getByRole`)
- Textos con expresiones regulares
- Atributos específicos

Esto hace que las pruebas sean menos frágiles ante cambios en la implementación.

## Pruebas End-to-End

### Ubicación de los Archivos

Las pruebas end-to-end se encuentran en:

- `cypress/e2e/`: Pruebas de flujos completos

### Ejecución de Pruebas

Para ejecutar las pruebas end-to-end:

```bash
# Abrir Cypress en modo interactivo
npm run cypress

# Ejecutar pruebas en modo headless
npm run cypress:run

# Ejecutar pruebas con servidor de desarrollo
npm run test:e2e
```

### Flujos Probados

Las pruebas end-to-end cubren los siguientes flujos:

1. **Gestión de Contactos**:
   - Listar contactos
   - Crear contacto
   - Ver detalles de contacto
   - Editar contacto
   - Eliminar contacto
   - Buscar contactos

2. **Gestión de Campañas**:
   - Listar campañas
   - Crear campaña
   - Ver detalles de campaña
   - Editar campaña
   - Eliminar campaña
   - Filtrar campañas por estado

## Integración Continua

El proyecto utiliza GitHub Actions para ejecutar pruebas automáticamente en cada push y pull request.

### Configuración

La configuración se encuentra en:
- `.github/workflows/tests.yml`

### Trabajos Configurados

1. **test**: Ejecuta pruebas unitarias y de integración
2. **lint**: Ejecuta linting para verificar la calidad del código
3. **e2e**: Ejecuta pruebas end-to-end con Cypress

## Cobertura de Código

El proyecto utiliza Codecov para analizar la cobertura de código.

### Umbrales de Cobertura

Se han establecido los siguientes umbrales:

- **Proyecto general**: 80%
- **Componentes**: 85%
- **Servicios**: 90%

### Configuración

La configuración se encuentra en:
- `codecov.yml`

## Mejores Prácticas

1. **Pruebas Aisladas**: Cada prueba debe ser independiente y no depender del estado de otras pruebas.
2. **Selectores Robustos**: Utilizar selectores basados en roles y atributos en lugar de clases o IDs.
3. **Mocks Consistentes**: Utilizar mocks consistentes para simular dependencias externas.
4. **Pruebas Descriptivas**: Utilizar nombres descriptivos para las pruebas que indiquen qué se está probando.
5. **Cobertura Completa**: Asegurarse de que las pruebas cubran todos los casos de uso importantes.

## Próximos Pasos

1. **Aumentar Cobertura**: Continuar aumentando la cobertura de pruebas para alcanzar los umbrales establecidos.
2. **Mejorar Pruebas E2E**: Agregar más pruebas end-to-end para cubrir más flujos de la aplicación.
3. **Pruebas de Rendimiento**: Implementar pruebas de rendimiento para identificar cuellos de botella.
4. **Pruebas de Accesibilidad**: Implementar pruebas de accesibilidad para garantizar que la aplicación sea accesible para todos los usuarios.
5. **Pruebas de Seguridad**: Implementar pruebas de seguridad para identificar vulnerabilidades.

## Recursos Adicionales

- [Documentación de Jest](https://jestjs.io/docs/getting-started)
- [Documentación de React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Documentación de Cypress](https://docs.cypress.io/guides/overview/why-cypress)
- [Documentación de MSW](https://mswjs.io/docs/)
- [Documentación de GitHub Actions](https://docs.github.com/en/actions)
- [Documentación de Codecov](https://docs.codecov.io/docs)
