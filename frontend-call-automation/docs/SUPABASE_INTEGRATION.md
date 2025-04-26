# Integración con Supabase

## Visión General

Este documento describe la integración de Supabase en el frontend del proyecto de Automatización de Llamadas (CALLi). Supabase proporciona servicios de base de datos, autenticación, almacenamiento y funciones en tiempo real.

## Configuración

### Variables de Entorno

La configuración de Supabase se realiza a través de variables de entorno en el archivo `.env.local`:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### Cliente de Supabase

El cliente de Supabase se configura en el módulo `src/lib/supabase.ts`:

```typescript
import { createClient } from "@supabase/supabase-js";
import { Database } from "@/types/supabase";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || "";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "";

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    detectSessionInUrl: true,
    storageKey: "call-automation-auth",
  },
});

export function useSupabase() {
  return supabase;
}
```

## Autenticación

### Servicio de Autenticación

El servicio de autenticación (`src/services/authService.ts`) proporciona funciones para:

- Iniciar sesión con email y contraseña
- Registrar nuevos usuarios
- Cerrar sesión
- Obtener el usuario actual
- Verificar si el usuario está autenticado

### Contexto de Autenticación

El contexto de autenticación (`src/contexts/AuthContext.tsx`) proporciona:

- Estado del usuario actual
- Estado de carga
- Funciones para iniciar sesión, registrarse y cerrar sesión

### Uso del Contexto de Autenticación

```tsx
import { useAuth } from "@/contexts/AuthContext";

function MyComponent() {
  const { user, loading, login, register, logout } = useAuth();

  // Usar las funciones y el estado según sea necesario
}
```

## Acceso a Datos

### Hook Personalizado

El hook `useSupabaseData` (`src/hooks/useSupabaseData.ts`) proporciona funciones para:

- Obtener todos los registros de una tabla
- Obtener un registro por su ID
- Crear un nuevo registro
- Actualizar un registro existente
- Eliminar un registro

### Uso del Hook

```tsx
import { useSupabaseData } from "@/hooks/useSupabaseData";
import { Database } from "@/types/supabase";

type Campaign = Database["public"]["Tables"]["campaigns"]["Row"];

function CampaignList() {
  const campaignsData = useSupabaseData<Campaign>("campaigns");
  
  // Obtener todas las campañas
  const loadCampaigns = async () => {
    const campaigns = await campaignsData.getAll({
      orderBy: { column: "created_at", ascending: false },
    });
    // Hacer algo con las campañas
  };
  
  // Crear una nueva campaña
  const createCampaign = async (data) => {
    const newCampaign = await campaignsData.create(data);
    // Hacer algo con la nueva campaña
  };
}
```

### Cliente Directo

También puedes usar el cliente de Supabase directamente:

```tsx
import { supabase } from "@/lib/supabase";

async function fetchData() {
  const { data, error } = await supabase
    .from("campaigns")
    .select("*")
    .order("created_at", { ascending: false });
    
  if (error) {
    console.error("Error:", error);
    return;
  }
  
  // Hacer algo con los datos
}
```

## Tipos de Datos

Los tipos de datos para Supabase se definen en `src/types/supabase.ts`. Estos tipos proporcionan autocompletado y verificación de tipos para las operaciones de base de datos.

## Ejemplo Completo

Se proporciona un componente de ejemplo en `src/components/examples/SupabaseExample.tsx` que muestra cómo:

- Cargar datos de Supabase
- Crear nuevos registros
- Eliminar registros
- Manejar estados de carga y errores

## Mejores Prácticas

1. **Centralización**: Usa el cliente centralizado de Supabase en `src/lib/supabase.ts`
2. **Tipado**: Utiliza los tipos definidos en `src/types/supabase.ts`
3. **Hooks**: Usa el hook `useSupabaseData` para operaciones CRUD comunes
4. **Manejo de Errores**: Siempre maneja los errores de las operaciones de Supabase
5. **Autenticación**: Usa el contexto de autenticación para gestionar el estado del usuario

## Recursos Adicionales

- [Documentación de Supabase](https://supabase.io/docs)
- [Documentación de supabase-js](https://supabase.io/docs/reference/javascript/introduction)
- [Guía de Autenticación de Supabase](https://supabase.io/docs/guides/auth)
