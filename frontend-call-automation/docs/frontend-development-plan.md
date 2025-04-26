# Plan de Desarrollo Frontend - CALL-AUTOMATION-PROYECT (Actualizado: 2025-04-03)

## 1. Objetivo General
Desarrollar una interfaz de usuario web moderna, funcional y escalable para la plataforma CALL-AUTOMATION-PROYECT, utilizando Next.js (App Router), TypeScript y TailwindCSS. La interfaz permitirá gestionar campañas de llamadas automatizadas, visualizar su progreso y resultados.

## 2. Arquitectura y Funcionalidades Implementadas/Planeadas

La aplicación sigue la estructura del App Router de Next.js.

**Funcionalidades Implementadas (CRUD Campañas):**

*   **Listado de Campañas (`/` o `/campaigns` - Implementado en `src/app/page.tsx` o similar y `src/components/CampaignListView.tsx`):**
    *   Muestra una lista/tabla de campañas obtenidas del backend.
    *   Permite la navegación a la creación de nuevas campañas.
    *   Permite la navegación al detalle de una campaña existente.
*   **Creación de Campaña (`/campaigns/create` - Implementado en `src/app/campaigns/create/page.tsx` y `src/components/CampaignForm.tsx`):**
    *   Utiliza el componente reutilizable `CampaignForm.tsx` para capturar los datos.
    *   Valida los datos del formulario.
    *   Envía los datos al endpoint de creación del backend.
    *   Redirige tras la creación exitosa.
*   **Detalle de Campaña (`/campaigns/[id]` - Implementado en `src/app/campaigns/[id]/page.tsx`):**
    *   Obtiene y muestra los detalles de una campaña específica por su ID.
    *   Muestra el estado actual, fechas, script, configuración, etc.
    *   Proporciona botones/enlaces para "Editar" y "Eliminar".
    *   Implementa la lógica de eliminación con diálogo de confirmación.
*   **Edición de Campaña (`/campaigns/[id]/edit` - Implementado en `src/app/campaigns/[id]/edit/page.tsx` y `src/components/CampaignForm.tsx`):**
    *   Obtiene los datos de la campaña existente.
    *   Reutiliza `CampaignForm.tsx`, pre-rellenando los campos con los datos actuales.
    *   Envía los datos actualizados al endpoint de actualización del backend.
    *   Redirige a la página de detalles tras la actualización exitosa.
*   **Formulario de Campaña Reutilizable (`src/components/CampaignForm.tsx`):**
    *   Componente controlado usando `react-hook-form` para manejar el estado y la validación.
    *   Acepta `initialData` para modo edición.
    *   Define los campos necesarios para una campaña (nombre, descripción, fechas, script, configuración de reintentos, etc.).
    *   Maneja el estado de carga (`isLoading`).

**Funcionalidades Pendientes/Próximos Pasos:**

*   **Gestión de Contactos:**
    *   Interfaz para subir/gestionar listas de contactos.
    *   Asociar listas de contactos a las campañas (modificar `CampaignForm.tsx` y backend si es necesario).
    *   Visualizar contactos asociados en el detalle de la campaña.
*   **Visualización de Llamadas:**
    *   Página o sección dentro del detalle de campaña para listar las llamadas realizadas (estado, duración, resultado).
    *   Posiblemente, ver transcripciones o detalles de llamadas individuales.
*   **Dashboard/Métricas:**
    *   Vista principal (`/`) que muestre estadísticas clave (campañas activas, llamadas totales/exitosas/fallidas, etc.).
    *   Gráficos para visualizar el rendimiento.
*   **Autenticación/Autorización:**
    *   Implementar flujo de login.
    *   Proteger rutas y funcionalidades según roles de usuario (si aplica).
    *   Integrar con el sistema de autenticación del backend.
*   **Mejoras UI/UX:**
    *   Refinar diseño responsivo.
    *   Implementar filtros/ordenamiento avanzado en listas.
    *   Mejorar feedback visual (skeletons, toasts más detallados).
    *   Asegurar accesibilidad (a11y).
*   **Pruebas:**
    *   Incrementar cobertura de pruebas unitarias y de integración (Jest/React Testing Library).
    *   Añadir pruebas E2E para flujos críticos (Cypress/Playwright).

## 3. Servicio API (`src/services/campaignApi.ts`)
*   **Tecnología:** Axios.
*   **Funciones Implementadas (CRUD Campañas):**
    *   `getCampaigns()`
    *   `getCampaignById(id: string)`
    *   `createCampaign(data: CampaignCreate)`
    *   `updateCampaign(id: string, data: CampaignUpdate)`
    *   `deleteCampaign(id: string)`
    *   `getCampaignStats(id: string)` (Implementada pero no usada activamente en UI aún)
*   **Tipado:** Definiciones en `src/types/campaign.ts`. Se añadirán tipos para Contactos, Llamadas, etc.
*   **Manejo de Errores:** Implementado a nivel básico (log a consola, re-throw). Se puede mejorar con manejo más específico en UI.

## 4. Gestión de Estado
*   **Actual:** Hooks nativos de React (useState, useEffect) para estado local de componentes y fetching de datos. `react-hook-form` para formularios.
*   **Futuro:** Evaluar TanStack Query (React Query) para simplificar el fetching, caching y sincronización del estado del servidor, especialmente si la complejidad aumenta con las nuevas funcionalidades.

## 5. Integración Frontend-Backend
*   **Flujo:** Componentes de página (`page.tsx`) usan `useEffect` para llamar al servicio API.
*   **Estado de Carga/Error:** Manejado con `useState` en los componentes para mostrar feedback.
*   **Autenticación:** Pendiente de implementación.

## 6. Mejoras de UI/UX
*   **Diseño Responsivo:** Base implementada con Tailwind CSS.
*   **Indicadores Visuales:**
    *   Carga: Mensajes de texto simples. Se pueden mejorar con spinners/skeletons.
    *   Feedback: Notificaciones/toasts implementadas con `sonner`.
    *   Confirmaciones: `window.confirm` usado para eliminar. Se puede mejorar con modales personalizados (ej: Shadcn Dialog).
*   **Accesibilidad (a11y):** A revisar y mejorar.

## 7. Estrategia de Pruebas
*   **Actual:** Mínima o inexistente.
*   **Plan:** Añadir pruebas unitarias (Jest/RTL) para componentes y servicios, pruebas de integración y E2E (Cypress/Playwright) para flujos críticos.

## 8. Preparación para Despliegue
*   **Variables de Entorno:** Usando `.env` para `NEXT_PUBLIC_API_URL`.
*   **Optimización:** Build de Next.js.
*   **Logging:** Básico con `console.error`. Evaluar Sentry u otro servicio para producción.

## 9. Resumen Implementación Reciente (CRUD Campañas)
Se implementaron las páginas y la lógica necesaria para gestionar completamente las campañas:
- **Detalle:** Creada la ruta dinámica `app/campaigns/[id]/page.tsx` que muestra la información de una campaña obtenida vía API.
- **Edición:** Creada la ruta `app/campaigns/[id]/edit/page.tsx` que reutiliza el componente `CampaignForm` con los datos iniciales de la campaña a editar.
- **Eliminación:** Añadida la funcionalidad de eliminar en la página de detalle, incluyendo un diálogo de confirmación y redirección.
- **Servicio API:** Verificadas y utilizadas las funciones `getCampaignById`, `updateCampaign`, y `deleteCampaign` en `campaignApi.ts`.
- **Componente Formulario:** `CampaignForm` se utiliza tanto para crear como para editar.
- **Manejo de Errores/Feedback:** Se añadieron estados de carga y se utiliza `sonner` para mostrar notificaciones de éxito/error.

## 10. Dependencias Clave
- React, Next.js, TypeScript
- Tailwind CSS, Shadcn/ui (implícito por `components.json`)
- Axios
- React Hook Form
- Sonner (para notificaciones)
- Lucide-react (iconos)
- Jest, React Testing Library, Cypress/Playwright (planeado para pruebas)
