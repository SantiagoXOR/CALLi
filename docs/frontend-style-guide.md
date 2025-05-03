# Guía de Estilo y Mejores Prácticas Frontend

Esta guía establece los estándares y mejores prácticas para el desarrollo frontend en el proyecto de Sistema de Automatización de Llamadas.

## Índice

1. [Convenciones de Código](#1-convenciones-de-código)
2. [Estructura de Archivos y Carpetas](#2-estructura-de-archivos-y-carpetas)
3. [Componentes React](#3-componentes-react)
4. [TypeScript](#4-typescript)
5. [Estilos con Tailwind CSS](#5-estilos-con-tailwind-css)
6. [Gestión de Estado](#6-gestión-de-estado)
7. [Manejo de Formularios](#7-manejo-de-formularios)
8. [Comunicación con el Backend](#8-comunicación-con-el-backend)
9. [Rendimiento](#9-rendimiento)
10. [Accesibilidad](#10-accesibilidad)
11. [Pruebas](#11-pruebas)

## 1. Convenciones de Código

### 1.1 Nomenclatura

- **Archivos y Carpetas**:
  - Componentes: PascalCase (ej. `CampaignList.tsx`)
  - Hooks: camelCase con prefijo "use" (ej. `useAuth.ts`)
  - Utilidades: camelCase (ej. `formatDate.ts`)
  - Constantes: UPPER_SNAKE_CASE (ej. `API_ENDPOINTS.ts`)

- **Variables y Funciones**:
  - Variables: camelCase (ej. `const userName = 'John'`)
  - Funciones: camelCase (ej. `function handleSubmit() {}`)
  - Componentes: PascalCase (ej. `function UserProfile() {}`)
  - Interfaces/Tipos: PascalCase (ej. `interface UserData {}`)
  - Enums: PascalCase (ej. `enum UserRole {}`)

### 1.2 Formato de Código

- Utilizar 2 espacios para la indentación
- Utilizar punto y coma al final de cada declaración
- Utilizar comillas simples para strings
- Limitar la longitud de línea a 100 caracteres
- Añadir una línea en blanco al final de cada archivo

### 1.3 Comentarios

- Utilizar JSDoc para documentar funciones y componentes importantes
- Evitar comentarios obvios que no añaden valor
- Explicar el "por qué" en lugar del "qué" cuando sea necesario

**Ejemplo**:
```tsx
/**
 * Componente que muestra los detalles de una campaña
 * @param {string} id - ID de la campaña a mostrar
 * @returns {JSX.Element} Componente de detalles de campaña
 */
function CampaignDetail({ id }: { id: string }): JSX.Element {
  // ...
}
```

## 2. Estructura de Archivos y Carpetas

### 2.1 Organización de Carpetas

```
src/
├── app/                 # Rutas y páginas (Next.js App Router)
├── components/          # Componentes React
│   ├── ui/              # Componentes UI reutilizables
│   └── [feature]/       # Componentes específicos de una característica
├── hooks/               # Hooks personalizados
├── lib/                 # Utilidades y funciones auxiliares
├── providers/           # Proveedores de contexto
├── services/            # Servicios para comunicación con API
└── types/               # Definiciones de tipos TypeScript
```

### 2.2 Estructura de Componentes

Cada componente debe estar en su propio archivo y seguir esta estructura:

1. Importaciones
2. Definición de tipos/interfaces
3. Definición del componente
4. Exportación

**Ejemplo**:
```tsx
// Importaciones
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';

// Definición de tipos
interface UserProfileProps {
  userId: string;
  showDetails?: boolean;
}

// Definición del componente
function UserProfile({ userId, showDetails = false }: UserProfileProps): JSX.Element {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Lógica para cargar datos del usuario
  }, [userId]);

  return (
    <div>
      {/* Contenido del componente */}
    </div>
  );
}

// Exportación
export default UserProfile;
```

## 3. Componentes React

### 3.1 Componentes Funcionales

- Utilizar siempre componentes funcionales con hooks
- Evitar componentes de clase

### 3.2 Props

- Definir tipos explícitos para las props
- Utilizar destructuring para acceder a las props
- Proporcionar valores por defecto cuando sea apropiado

```tsx
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
}

function CustomButton({
  label,
  onClick,
  variant = 'primary',
  disabled = false
}: ButtonProps): JSX.Element {
  // ...
}
```

### 3.3 Composición de Componentes

- Preferir composición sobre herencia
- Utilizar el patrón de componentes compuestos cuando sea apropiado

```tsx
// Ejemplo de composición
<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
  </CardHeader>
  <CardContent>
    <p>Contenido</p>
  </CardContent>
</Card>
```

### 3.4 Separación de Responsabilidades

- Separar componentes de presentación (UI) y contenedores (lógica)
- Extraer lógica compleja a hooks personalizados

## 4. TypeScript

### 4.1 Tipos vs Interfaces

- Utilizar `interface` para definir la forma de objetos y clases
- Utilizar `type` para alias de tipos, uniones, intersecciones y tipos utilitarios

```tsx
// Interface para objetos
interface User {
  id: string;
  name: string;
  email: string;
}

// Type para uniones
type Status = 'pending' | 'active' | 'completed';
```

### 4.2 Tipado Explícito

- Proporcionar tipos explícitos para variables, funciones y componentes
- Evitar el uso de `any` siempre que sea posible
- Utilizar `unknown` en lugar de `any` cuando el tipo no es conocido

```tsx
// Tipado explícito
const users: User[] = [];
function getUser(id: string): User | undefined {
  return users.find(user => user.id === id);
}
```

### 4.3 Tipos Genéricos

- Utilizar tipos genéricos para componentes y funciones reutilizables

```tsx
// Ejemplo de tipo genérico
function fetchData<T>(url: string): Promise<T> {
  return fetch(url).then(response => response.json());
}

// Uso
const users = await fetchData<User[]>('/api/users');
```

## 5. Estilos con Tailwind CSS

### 5.1 Organización de Clases

- Agrupar clases relacionadas
- Seguir un orden consistente: layout, dimensiones, espaciado, tipografía, colores, estados

```tsx
// Orden recomendado de clases
<div className="
  flex items-center justify-between  /* Layout */
  w-full h-12                        /* Dimensiones */
  p-4 my-2                           /* Espaciado */
  text-sm font-medium                /* Tipografía */
  bg-white text-gray-800             /* Colores */
  hover:bg-gray-50                   /* Estados */
">
  {/* Contenido */}
</div>
```

### 5.2 Responsive Design

- Utilizar los modificadores responsive de Tailwind (`sm:`, `md:`, `lg:`, `xl:`)
- Diseñar primero para móvil (mobile-first)

```tsx
<div className="
  flex-col items-center    /* Móvil (por defecto) */
  sm:flex-row sm:justify-between  /* Tablet y superior */
">
  {/* Contenido */}
</div>
```

### 5.3 Componentes UI

- Utilizar los componentes de Shadcn UI como base
- Personalizar los componentes según sea necesario
- Mantener la consistencia visual en toda la aplicación

## 6. Gestión de Estado

### 6.1 Estado Local

- Utilizar `useState` para estado local simple
- Utilizar `useReducer` para estado local complejo

```tsx
// Estado simple
const [isOpen, setIsOpen] = useState(false);

// Estado complejo
const [state, dispatch] = useReducer(reducer, initialState);
```

### 6.2 Estado Global

- Utilizar React Context para estado compartido entre componentes
- Considerar TanStack Query para estado del servidor

```tsx
// Ejemplo de Context
export const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  // Lógica para autenticación

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}
```

### 6.3 Estado del Servidor

- Utilizar TanStack Query para gestionar el estado del servidor
- Aprovechar el caché y la revalidación automática

```tsx
// Ejemplo con TanStack Query
export function useCampaigns() {
  return useQuery({
    queryKey: ['campaigns'],
    queryFn: () => campaignService.getCampaigns(),
  });
}
```

## 7. Manejo de Formularios

### 7.1 React Hook Form

- Utilizar React Hook Form para la gestión de formularios
- Definir esquemas de validación con Zod o Yup

```tsx
// Ejemplo con React Hook Form y Zod
const formSchema = z.object({
  name: z.string().min(3, 'El nombre debe tener al menos 3 caracteres'),
  email: z.string().email('Email inválido'),
});

function ContactForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    // Lógica para enviar el formulario
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        {/* Campos del formulario */}
      </form>
    </Form>
  );
}
```

### 7.2 Validación

- Validar datos tanto en el cliente como en el servidor
- Proporcionar mensajes de error claros y específicos
- Mostrar feedback visual para campos válidos e inválidos

### 7.3 Experiencia de Usuario

- Mostrar indicadores de carga durante el envío
- Deshabilitar el botón de envío mientras se procesa
- Proporcionar feedback después del envío (éxito/error)

## 8. Comunicación con el Backend

### 8.1 Servicios API

- Encapsular la lógica de comunicación con el backend en servicios
- Utilizar Axios para peticiones HTTP
- Manejar errores de forma consistente

```tsx
// Ejemplo de servicio API
export const userService = {
  async getUsers(): Promise<User[]> {
    try {
      const response = await axios.get(`${API_URL}/users`);
      return response.data;
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  },

  async getUserById(id: string): Promise<User> {
    try {
      const response = await axios.get(`${API_URL}/users/${id}`);
      return response.data;
    } catch (error) {
      handleApiError(error);
      throw error;
    }
  },

  // Otros métodos...
};
```

### 8.2 Manejo de Errores

- Crear una función centralizada para manejar errores de API
- Mostrar mensajes de error apropiados al usuario
- Registrar errores para depuración

```tsx
// Función para manejar errores de API
function handleApiError(error: unknown): void {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;

    if (status === 401) {
      // Redirigir a login
      toast.error('Sesión expirada. Por favor, inicia sesión nuevamente.');
    } else if (status === 403) {
      toast.error('No tienes permisos para realizar esta acción.');
    } else if (status === 404) {
      toast.error('El recurso solicitado no existe.');
    } else {
      toast.error('Ha ocurrido un error. Por favor, intenta nuevamente.');
    }

    // Registrar error para depuración
    console.error('API Error:', error);
  } else {
    toast.error('Ha ocurrido un error inesperado.');
    console.error('Unexpected Error:', error);
  }
}
```

### 8.3 Caché y Revalidación

- Utilizar TanStack Query para gestionar la caché de datos
- Implementar estrategias de revalidación apropiadas

```tsx
// Configuración de TanStack Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutos
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
```

## 9. Rendimiento

### 9.1 Memoización

- Utilizar `useMemo` para cálculos costosos
- Utilizar `useCallback` para funciones que se pasan como props
- Utilizar `React.memo` para evitar renderizados innecesarios

```tsx
// Ejemplo de memoización
const sortedItems = useMemo(() => {
  return [...items].sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

const handleDelete = useCallback((id: string) => {
  // Lógica para eliminar
}, []);

const MemoizedComponent = React.memo(MyComponent);
```

### 9.2 Renderizado Condicional

- Utilizar renderizado condicional para mostrar/ocultar elementos
- Evitar renderizar grandes listas innecesariamente

```tsx
// Renderizado condicional
{isLoading ? (
  <LoadingSpinner />
) : error ? (
  <ErrorMessage message={error.message} />
) : (
  <DataTable data={data} />
)}
```

### 9.3 Optimización de Imágenes

- Utilizar el componente `Image` de Next.js para optimizar imágenes
- Especificar dimensiones para evitar layout shifts

```tsx
// Optimización de imágenes con Next.js
import Image from 'next/image';

<Image
  src="/images/logo.png"
  alt="Logo"
  width={200}
  height={100}
  priority
/>
```

## 10. Accesibilidad

### 10.1 Semántica HTML

- Utilizar elementos HTML semánticos (`nav`, `main`, `section`, etc.)
- Utilizar encabezados (`h1`-`h6`) de forma jerárquica
- Utilizar listas (`ul`, `ol`) para grupos de elementos relacionados

### 10.2 ARIA

- Añadir atributos ARIA cuando sea necesario
- Utilizar `aria-label` para elementos sin texto visible
- Utilizar `aria-describedby` para proporcionar descripciones adicionales

```tsx
// Ejemplo de atributos ARIA
<button
  aria-label="Cerrar diálogo"
  aria-describedby="dialog-description"
  onClick={closeDialog}
>
  <XIcon />
</button>
<p id="dialog-description" className="sr-only">
  Cierra el diálogo actual y descarta los cambios
</p>
```

### 10.3 Navegación por Teclado

- Asegurar que todos los elementos interactivos sean accesibles por teclado
- Mantener un orden de tabulación lógico
- Implementar atajos de teclado para acciones comunes

### 10.4 Contraste y Tamaño de Texto

- Asegurar un contraste suficiente entre texto y fondo
- Utilizar tamaños de texto legibles (mínimo 16px para texto principal)
- Permitir que el texto se pueda redimensionar

## 11. Pruebas

### 11.1 Pruebas Unitarias

- Probar componentes individuales con Jest y React Testing Library
- Enfocarse en el comportamiento, no en la implementación
- Utilizar mocks para servicios externos

```tsx
// Ejemplo de prueba unitaria
import { render, screen, fireEvent } from '@testing-library/react';
import UserProfile from './UserProfile';

describe('UserProfile', () => {
  it('muestra el nombre del usuario', () => {
    render(<UserProfile user={{ id: '1', name: 'John Doe' }} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('llama a onEdit cuando se hace clic en el botón de editar', () => {
    const handleEdit = jest.fn();
    render(<UserProfile user={{ id: '1', name: 'John Doe' }} onEdit={handleEdit} />);

    fireEvent.click(screen.getByRole('button', { name: /editar/i }));
    expect(handleEdit).toHaveBeenCalledWith('1');
  });
});
```

### 11.2 Pruebas de Integración

- Probar la interacción entre componentes
- Verificar flujos completos de usuario
- Utilizar mocks para APIs externas

### 11.3 Pruebas E2E

- Utilizar Cypress o Playwright para pruebas de extremo a extremo
- Probar flujos críticos de usuario
- Ejecutar pruebas en diferentes navegadores

```tsx
// Ejemplo de prueba E2E con Cypress
describe('Flujo de creación de campaña', () => {
  beforeEach(() => {
    cy.login('admin@example.com', 'password');
    cy.visit('/campaigns');
  });

  it('permite crear una nueva campaña', () => {
    cy.findByRole('button', { name: /crear campaña/i }).click();

    cy.findByLabelText(/nombre/i).type('Campaña de Prueba');
    cy.findByLabelText(/descripción/i).type('Esta es una campaña de prueba');
    cy.findByLabelText(/fecha de inicio/i).type('2025-05-01');

    cy.findByRole('button', { name: /guardar/i }).click();

    cy.findByText('Campaña creada con éxito').should('be.visible');
    cy.url().should('include', '/campaigns');
    cy.findByText('Campaña de Prueba').should('be.visible');
  });
});
```
