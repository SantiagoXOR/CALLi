# Guía para Escribir Pruebas

Esta guía proporciona instrucciones detalladas sobre cómo escribir pruebas para el proyecto de automatización de llamadas.

## Índice

1. [Pruebas Unitarias](#pruebas-unitarias)
2. [Pruebas de Integración](#pruebas-de-integración)
3. [Pruebas End-to-End](#pruebas-end-to-end)
4. [Mocks](#mocks)
5. [Selectores](#selectores)
6. [Buenas Prácticas](#buenas-prácticas)

## Pruebas Unitarias

Las pruebas unitarias se utilizan para probar componentes y servicios de forma aislada.

### Estructura de una Prueba Unitaria

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ComponentName } from '../ComponentName';

// Mocks
jest.mock('@/services/someService', () => ({
  useSomeHook: jest.fn(() => ({
    data: { /* datos de ejemplo */ },
    isLoading: false,
    error: null,
  })),
}));

describe('ComponentName', () => {
  // Configuración para cada prueba
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renderiza correctamente', () => {
    render(<ComponentName />);

    // Verificar que el componente se renderice correctamente
    expect(screen.getByRole('heading', { name: /título/i })).toBeInTheDocument();
  });

  it('maneja interacciones del usuario', async () => {
    render(<ComponentName />);

    // Simular interacción del usuario
    const button = screen.getByRole('button', { name: /acción/i });
    await userEvent.click(button);

    // Verificar el resultado de la interacción
    expect(screen.getByText(/resultado/i)).toBeInTheDocument();
  });
});
```

### Pruebas para Componentes

Al probar componentes, enfócate en:

1. **Renderizado**: Verificar que el componente se renderice correctamente.
2. **Interacciones**: Verificar que el componente responda correctamente a las interacciones del usuario.
3. **Estados**: Verificar que el componente muestre el contenido correcto según su estado.
4. **Callbacks**: Verificar que el componente llame a las funciones de callback correctamente.

### Pruebas para Servicios

Al probar servicios, enfócate en:

1. **Llamadas a API**: Verificar que el servicio llame a la API con los parámetros correctos.
2. **Transformación de Datos**: Verificar que el servicio transforme los datos correctamente.
3. **Manejo de Errores**: Verificar que el servicio maneje los errores correctamente.

## Pruebas de Integración

Las pruebas de integración se utilizan para probar la interacción entre componentes.

### Estructura de una Prueba de Integración

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ParentComponent } from '../ParentComponent';

// Configurar mocks para servicios externos
jest.mock('@/services/someService', () => ({
  // Implementación de mocks
}));

describe('ParentComponent Integration', () => {
  it('integra correctamente con sus componentes hijos', async () => {
    render(<ParentComponent />);

    // Verificar que los componentes se rendericen correctamente
    expect(screen.getByText(/componente padre/i)).toBeInTheDocument();
    expect(screen.getByText(/componente hijo/i)).toBeInTheDocument();

    // Simular interacción que afecta a múltiples componentes
    const button = screen.getByRole('button', { name: /acción/i });
    await userEvent.click(button);

    // Verificar que los componentes se actualicen correctamente
    await waitFor(() => {
      expect(screen.getByText(/resultado en componente hijo/i)).toBeInTheDocument();
    });
  });
});
```

## Pruebas End-to-End

Las pruebas end-to-end se utilizan para probar flujos completos de la aplicación.

### Estructura de una Prueba End-to-End

```typescript
describe('Flujo de Usuario', () => {
  beforeEach(() => {
    // Visitar la página inicial
    cy.visit('/');

    // Esperar a que la página cargue completamente
    cy.get('h1').contains('Título').should('be.visible');
  });

  it('completa un flujo de usuario', () => {
    // Paso 1: Navegar a una página
    cy.get('a').contains('Ir a Página').click();
    cy.url().should('include', '/pagina');

    // Paso 2: Interactuar con un formulario
    cy.get('input[name="campo"]').type('valor');
    cy.get('button').contains('Enviar').click();

    // Paso 3: Verificar el resultado
    cy.contains('Éxito').should('be.visible');
  });
});
```

### Consejos para Pruebas End-to-End

1. **Selectores Robustos**: Utiliza selectores que sean resistentes a cambios en la implementación.
2. **Esperas Explícitas**: Utiliza `cy.wait()` o `cy.should()` para esperar a que los elementos estén disponibles.
3. **Datos de Prueba**: Utiliza datos de prueba consistentes para facilitar la depuración.
4. **Flujos Completos**: Prueba flujos completos de usuario en lugar de acciones aisladas.

## Mocks

Los mocks se utilizan para simular dependencias externas.

### Mocks para Servicios

```typescript
// Mock para un servicio
jest.mock('@/services/contactService', () => ({
  getContacts: jest.fn(() => Promise.resolve({ data: [], total: 0 })),
  getContact: jest.fn((id) => Promise.resolve({ id, name: 'Test Contact' })),
  createContact: jest.fn((data) => Promise.resolve({ id: '123', ...data })),
  updateContact: jest.fn((id, data) => Promise.resolve({ id, ...data })),
  deleteContact: jest.fn(() => Promise.resolve({ success: true })),
}));
```

### Mocks para Hooks

```typescript
// Mock para un hook de React Query
jest.mock('@/services/contactService', () => ({
  useGetContacts: jest.fn(() => ({
    data: { data: [], total: 0 },
    isLoading: false,
    error: null,
  })),
  useGetContact: jest.fn(() => ({
    data: { id: '123', name: 'Test Contact' },
    isLoading: false,
    error: null,
  })),
  useCreateContact: jest.fn(() => ({
    mutateAsync: jest.fn((data) => Promise.resolve({ id: '123', ...data })),
    isPending: false,
  })),
}));
```

### Mocks para Axios

```typescript
// Mock para axios
jest.mock('axios');

// En la prueba
import axios from 'axios';

// Configurar el mock
axios.get.mockResolvedValueOnce({
  data: { /* datos de ejemplo */ },
});
```

## Selectores

Los selectores se utilizan para encontrar elementos en el DOM.

### Selectores Recomendados

1. **Por Rol**: `getByRole('button', { name: /texto/i })`
2. **Por Texto**: `getByText(/texto/i)`
3. **Por Etiqueta**: `getByLabelText(/etiqueta/i)`
4. **Por Placeholder**: `getByPlaceholderText(/placeholder/i)`
5. **Por TestId**: `getByTestId('test-id')`

### Ejemplos de Selectores

```typescript
// Encontrar un botón por su texto
const button = screen.getByRole('button', { name: /guardar/i });

// Encontrar un campo de texto por su etiqueta
const input = screen.getByLabelText(/nombre/i);

// Encontrar un elemento por su texto
const element = screen.getByText(/mensaje/i);

// Encontrar un elemento por su placeholder
const searchInput = screen.getByPlaceholderText(/buscar/i);

// Encontrar un elemento por su testId
const element = screen.getByTestId('test-id');
```

## Buenas Prácticas

### Estructura de las Pruebas

1. **Arrange**: Configurar el entorno de prueba.
2. **Act**: Realizar la acción que se está probando.
3. **Assert**: Verificar el resultado de la acción.

```typescript
it('ejemplo de estructura', async () => {
  // Arrange
  render(<Component />);
  const button = screen.getByRole('button', { name: /acción/i });

  // Act
  await userEvent.click(button);

  // Assert
  expect(screen.getByText(/resultado/i)).toBeInTheDocument();
});
```

### Nombres de las Pruebas

Utiliza nombres descriptivos que indiquen:
1. Qué se está probando
2. Bajo qué condiciones
3. Cuál es el resultado esperado

```typescript
it('muestra un mensaje de error cuando la API devuelve un error', async () => {
  // ...
});

it('llama a onSubmit con los datos del formulario cuando se hace clic en el botón de enviar', async () => {
  // ...
});
```

### Aislamiento de Pruebas

Cada prueba debe ser independiente y no depender del estado de otras pruebas.

```typescript
// Mal: Pruebas que dependen del estado de otras pruebas
let sharedState;

it('primera prueba', () => {
  sharedState = someFunction();
  expect(sharedState).toBe(expectedValue);
});

it('segunda prueba', () => {
  // Depende de sharedState de la primera prueba
  expect(sharedState).toBe(expectedValue);
});

// Bien: Pruebas independientes
it('primera prueba', () => {
  const result = someFunction();
  expect(result).toBe(expectedValue);
});

it('segunda prueba', () => {
  const result = someFunction();
  expect(result).toBe(expectedValue);
});
```

### Cobertura de Código

Asegúrate de que las pruebas cubran:
1. Todos los caminos de código
2. Todos los casos de borde
3. Todos los casos de error

```typescript
// Prueba para el caso exitoso
it('maneja el caso exitoso', async () => {
  // Configurar mock para éxito
  mockFunction.mockResolvedValueOnce({ success: true });

  // Realizar acción
  await someFunction();

  // Verificar resultado
  expect(screen.getByText(/éxito/i)).toBeInTheDocument();
});

// Prueba para el caso de error
it('maneja el caso de error', async () => {
  // Configurar mock para error
  mockFunction.mockRejectedValueOnce(new Error('Error'));

  // Realizar acción
  await someFunction();

  // Verificar resultado
  expect(screen.getByText(/error/i)).toBeInTheDocument();
});
```

### Pruebas de Accesibilidad

Utiliza `jest-axe` para probar la accesibilidad de tus componentes.

```typescript
import { axe } from 'jest-axe';

it('no tiene violaciones de accesibilidad', async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

## Recursos Adicionales

- [Documentación de Jest](https://jestjs.io/docs/getting-started)
- [Documentación de React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Documentación de Cypress](https://docs.cypress.io/guides/overview/why-cypress)
- [Documentación de MSW](https://mswjs.io/docs/)
- [Guía de Testing de Kent C. Dodds](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)
