# Guía de Desarrollo Frontend - Sistema de Automatización de Llamadas

## Índice

1. [Introducción](#1-introducción)
2. [Configuración del Entorno de Desarrollo](#2-configuración-del-entorno-de-desarrollo)
3. [Arquitectura y Estructura del Proyecto](#3-arquitectura-y-estructura-del-proyecto)
4. [Componentes y Patrones de Diseño](#4-componentes-y-patrones-de-diseño)
5. [Gestión de Estado y Comunicación con el Backend](#5-gestión-de-estado-y-comunicación-con-el-backend)
6. [Guías de Estilo y Mejores Prácticas](#6-guías-de-estilo-y-mejores-prácticas)
7. [Flujo de Trabajo de Desarrollo](#7-flujo-de-trabajo-de-desarrollo)
8. [Pruebas](#8-pruebas)
9. [Despliegue](#9-despliegue)
10. [Recursos y Referencias](#10-recursos-y-referencias)

## 1. Introducción

El frontend del Sistema de Automatización de Llamadas es una aplicación web moderna desarrollada con Next.js (App Router), TypeScript y TailwindCSS. Esta guía proporciona toda la información necesaria para entender, desarrollar y mantener el frontend del proyecto.

### 1.1 Visión General

El frontend permite a los usuarios:
- Gestionar campañas de llamadas automatizadas
- Visualizar el progreso y resultados de las campañas
- Administrar contactos y configuraciones del sistema
- Acceder a reportes y análisis de llamadas

### 1.2 Tecnologías Principales

- **Next.js (App Router)**: Framework React para renderizado del lado del servidor y generación de sitios estáticos
- **TypeScript**: Superset tipado de JavaScript
- **Tailwind CSS**: Framework CSS de utilidades
- **Shadcn/ui**: Componentes UI reutilizables
- **React Hook Form**: Gestión de formularios
- **Axios**: Cliente HTTP para comunicación con el backend
- **TanStack Query (React Query)**: Gestión de estado del servidor y caché
- **Sonner**: Notificaciones toast
- **Lucide-react**: Iconos

## 2. Configuración del Entorno de Desarrollo

### 2.1 Requisitos Previos

- Node.js (v18 o superior)
- Bun (recomendado para mejor rendimiento)
- Editor de código (VS Code recomendado)
- Git

### 2.2 Instalación

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd call-automation-project/frontend-call-automation
   ```

2. Instalar dependencias:
   ```bash
   # Con npm
   npm install

   # Con Bun (recomendado)
   bun install
   ```

3. Configurar variables de entorno:
   - Copiar `.env.example` a `.env.local`
   - Actualizar las variables según sea necesario

4. Iniciar el servidor de desarrollo:
   ```bash
   # Con npm
   npm run dev

   # Con Bun
   bun dev
   ```

5. Acceder a la aplicación en `http://localhost:3000`

### 2.3 Extensiones Recomendadas para VS Code

- ESLint
- Prettier
- Tailwind CSS IntelliSense
- TypeScript Hero
- Error Lens

## 3. Arquitectura y Estructura del Proyecto

### 3.1 Estructura de Carpetas

```
frontend-call-automation/
├── public/                 # Archivos estáticos
├── src/                    # Código fuente
│   ├── app/                # Rutas y páginas (Next.js App Router)
│   │   ├── campaigns/      # Rutas relacionadas con campañas
│   │   │   ├── create/     # Creación de campañas
│   │   │   └── [id]/       # Detalles y edición de campañas
│   │   └── layout.tsx      # Layout principal de la aplicación
│   ├── components/         # Componentes React
│   │   ├── ui/             # Componentes UI reutilizables (Shadcn)
│   │   └── ...             # Componentes específicos de la aplicación
│   ├── lib/                # Utilidades y funciones auxiliares
│   ├── providers/          # Proveedores de contexto
│   ├── services/           # Servicios para comunicación con API
│   └── types/              # Definiciones de tipos TypeScript
├── .env.example            # Ejemplo de variables de entorno
├── components.json         # Configuración de Shadcn UI
├── next.config.js          # Configuración de Next.js
├── package.json            # Dependencias y scripts
├── tailwind.config.js      # Configuración de Tailwind CSS
└── tsconfig.json           # Configuración de TypeScript
```

### 3.2 Arquitectura de la Aplicación

La aplicación sigue una arquitectura basada en componentes con el patrón de diseño de App Router de Next.js:

1. **Páginas (Pages)**: Componentes en `src/app` que definen las rutas de la aplicación
2. **Componentes (Components)**: Elementos UI reutilizables
3. **Servicios (Services)**: Lógica para comunicación con el backend
4. **Proveedores (Providers)**: Contextos para compartir estado global
5. **Utilidades (Utils)**: Funciones auxiliares

### 3.3 Flujo de Datos

```
Usuario → Componente de Página → Servicio API → Backend → Base de Datos
   ↑                  ↓
   └──────── Componentes UI
```

## 4. Componentes y Patrones de Diseño

### 4.1 Componentes Principales

- **Layout**: Estructura general de la aplicación con navegación
- **CampaignList**: Lista de campañas con opciones de filtrado
- **CampaignDetail**: Detalles de una campaña específica
- **CampaignForm**: Formulario para crear/editar campañas
- **DashboardView**: Panel principal con métricas y resúmenes

### 4.2 Componentes UI (Shadcn)

Utilizamos componentes de Shadcn UI para mantener una interfaz consistente:

- Button, Card, Dialog, Form, Input, Select, Tabs, etc.
- Estos componentes se encuentran en `src/components/ui/`

### 4.3 Patrones de Diseño

#### Patrón de Presentación/Contenedor

Separamos los componentes en:
- **Componentes de Presentación**: Enfocados en la UI (cómo se ven las cosas)
- **Componentes Contenedores**: Manejan la lógica y el estado (cómo funcionan las cosas)

Ejemplo:
- `CampaignListView.tsx` (Presentación)
- `CampaignList.tsx` (Contenedor)

#### Composición de Componentes

Construimos componentes complejos a partir de componentes más simples:

```tsx
// Ejemplo de composición
<Card>
  <CardHeader>
    <CardTitle>Título</CardTitle>
    <CardDescription>Descripción</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Contenido</p>
  </CardContent>
  <CardFooter>
    <Button>Acción</Button>
  </CardFooter>
</Card>
```

## 5. Gestión de Estado y Comunicación con el Backend

### 5.1 Gestión de Estado Local

- Utilizamos hooks de React (`useState`, `useReducer`) para estado local de componentes
- Para formularios, empleamos `react-hook-form`

### 5.2 Gestión de Estado Global

- Para estado global, utilizamos React Context API a través de proveedores personalizados
- TanStack Query (React Query) para estado del servidor y caché

### 5.3 Comunicación con el Backend

#### Servicios API

Los servicios en `src/services/` encapsulan la lógica de comunicación con el backend:

```tsx
// Ejemplo de servicio API (campaignApi.ts)
import axios from 'axios';
import { Campaign, CampaignCreate } from '../types/campaign';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const campaignApi = {
  async getCampaigns(): Promise<Campaign[]> {
    const response = await axios.get(`${API_BASE_URL}/api/campaigns`);
    return response.data;
  },

  async createCampaign(campaign: CampaignCreate): Promise<Campaign> {
    const response = await axios.post(`${API_BASE_URL}/api/campaigns`, campaign);
    return response.data;
  },

  // Otros métodos...
};
```

#### Hooks de React Query

Utilizamos React Query para simplificar la gestión del estado del servidor:

```tsx
// Ejemplo de hook con React Query
export const useGetCampaigns = (page = 1, limit = 10) => {
  return useQuery({
    queryKey: ['campaigns', page, limit],
    queryFn: () => campaignService.getCampaigns(page, limit),
  });
};
```

### 5.4 Manejo de Errores

- Utilizamos bloques try/catch para capturar errores en llamadas API
- Mostramos notificaciones de error con Sonner
- Implementamos estados de carga para mejorar la experiencia de usuario

## 6. Guías de Estilo y Mejores Prácticas

### 6.1 Convenciones de Nomenclatura

- **Componentes**: PascalCase (ej. `CampaignList.tsx`)
- **Funciones/Hooks**: camelCase (ej. `useGetCampaigns`)
- **Constantes**: UPPER_SNAKE_CASE (ej. `API_BASE_URL`)
- **Tipos/Interfaces**: PascalCase (ej. `Campaign`, `CampaignCreate`)

### 6.2 Estilo de Código

- Utilizamos ESLint y Prettier para mantener un estilo de código consistente
- Preferimos funciones de flecha para componentes y hooks
- Utilizamos tipos explícitos en TypeScript

### 6.3 Mejores Prácticas de React

- Evitar renderizados innecesarios con memoización (`useMemo`, `useCallback`, `memo`)
- Utilizar claves (keys) únicas en listas
- Mantener componentes pequeños y enfocados en una sola responsabilidad
- Extraer lógica compleja a hooks personalizados

### 6.4 Accesibilidad (a11y)

- Utilizar elementos semánticos de HTML
- Proporcionar textos alternativos para imágenes
- Asegurar contraste de color adecuado
- Implementar navegación por teclado
- Seguir las pautas WCAG 2.1

## 7. Flujo de Trabajo de Desarrollo

### 7.1 Proceso de Desarrollo

1. **Planificación**: Entender los requisitos y diseñar la solución
2. **Implementación**: Desarrollar la funcionalidad
3. **Pruebas**: Verificar que todo funciona correctamente
4. **Revisión**: Solicitar revisión de código
5. **Despliegue**: Integrar cambios en la rama principal

### 7.2 Control de Versiones

- Utilizamos Git para control de versiones
- Seguimos el flujo de trabajo de Gitflow:
  - `main`: Código en producción
  - `develop`: Código en desarrollo
  - `feature/*`: Nuevas funcionalidades
  - `bugfix/*`: Correcciones de errores
  - `release/*`: Preparación para lanzamiento

### 7.3 Revisión de Código

- Todas las contribuciones deben pasar por revisión de código
- Utilizamos Pull Requests para revisar cambios
- Criterios de revisión:
  - Funcionalidad correcta
  - Calidad del código
  - Pruebas adecuadas
  - Documentación

## 8. Pruebas

### 8.1 Tipos de Pruebas

- **Pruebas Unitarias**: Probar componentes individuales
- **Pruebas de Integración**: Probar interacciones entre componentes
- **Pruebas E2E**: Probar flujos completos de usuario

### 8.2 Herramientas de Prueba

- **Jest**: Framework de pruebas
- **React Testing Library**: Pruebas de componentes
- **Cypress/Playwright**: Pruebas E2E

### 8.3 Ejemplos de Pruebas

```tsx
// Ejemplo de prueba unitaria con Jest y React Testing Library
import { render, screen } from '@testing-library/react';
import CampaignListView from './CampaignListView';

describe('CampaignListView', () => {
  it('muestra mensaje cuando no hay campañas', () => {
    render(<CampaignListView campaigns={[]} isLoading={false} />);
    expect(screen.getByText(/No hay campañas disponibles/i)).toBeInTheDocument();
  });

  it('muestra lista de campañas cuando hay datos', () => {
    const mockCampaigns = [
      { id: '1', name: 'Campaña 1', status: 'active' },
      { id: '2', name: 'Campaña 2', status: 'draft' },
    ];

    render(<CampaignListView campaigns={mockCampaigns} isLoading={false} />);
    expect(screen.getByText('Campaña 1')).toBeInTheDocument();
    expect(screen.getByText('Campaña 2')).toBeInTheDocument();
  });
});
```

## 9. Despliegue

### 9.1 Entornos

- **Desarrollo**: Para pruebas locales
- **Staging**: Para pruebas antes de producción
- **Producción**: Entorno de usuario final

### 9.2 Proceso de Construcción

```bash
# Construir la aplicación
npm run build

# Verificar la construcción localmente
npm run start
```

### 9.3 Despliegue con Docker

Utilizamos Docker para garantizar consistencia entre entornos:

```dockerfile
# Ejemplo de Dockerfile
FROM node:18-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
```

## 10. Recursos y Referencias

### 10.1 Documentación Oficial

- [Next.js](https://nextjs.org/docs)
- [React](https://reactjs.org/docs)
- [TypeScript](https://www.typescriptlang.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Shadcn UI](https://ui.shadcn.com)
- [React Hook Form](https://react-hook-form.com/get-started)
- [TanStack Query](https://tanstack.com/query/latest)

### 10.2 Recursos Internos

- [Plan de Desarrollo Frontend](./frontend-development-plan.md)
- [Arquitectura de Componentes](../architecture/component-architecture.md)
- [API Backend](../backend/api-documentation.md)

### 10.3 Mejores Prácticas

- [React Patterns](https://reactpatterns.com/)
- [Clean Code en JavaScript](https://github.com/ryanmcdermott/clean-code-javascript)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
