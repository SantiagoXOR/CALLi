# Integración con Supabase MCP

## Visión General

Este documento describe la integración de Supabase a través del Model Context Protocol (MCP) en el proyecto de Automatización de Llamadas (CALLi). El MCP permite una integración más profunda con Supabase y proporciona funcionalidades adicionales.

## ¿Qué es el MCP?

El Model Context Protocol (MCP) es un protocolo que permite a las aplicaciones comunicarse con servicios externos a través de un servidor intermedio. En el caso de Supabase, el MCP proporciona una capa de abstracción sobre la API de Supabase, lo que facilita la interacción con la base de datos y otros servicios.

## Configuración

### Servidor MCP

El servidor MCP para Supabase se configura con los siguientes parámetros:

- **Nombre**: SUPABASE_CALLi
- **Comando**: `npx -y @supabase/mcp-server-supabase@latest --access-token=sbp_3a4f85271977213912b98db6f5c4eaf`
- **Variables de entorno**:
  - `NEXT_PUBLIC_SUPABASE_URL`: URL de la instancia de Supabase
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Clave anónima de Supabase
  - `SUPABASE_SERVICE_ROLE_KEY`: Clave de servicio de Supabase

### Cliente MCP

El cliente MCP se configura en el módulo `src/lib/supabase-mcp.ts`:

```typescript
import { Database } from "@/types/supabase";

// Nombre del servidor MCP configurado
const MCP_SERVER_NAME = "SUPABASE_CALLi";

// Ejecuta una consulta en Supabase a través del MCP
export async function supabaseMCP<T = any>(
  method: "select" | "insert" | "update" | "delete",
  table: string,
  params: Record<string, any> = {}
): Promise<SupabaseMCPResponse<T>> {
  // Implementación...
}

// Cliente MCP con funciones para interactuar con Supabase
export const supabaseMCPClient = {
  select: async <T = any>(table: string, options = {}) => { /* ... */ },
  insert: async <T = any>(table: string, records) => { /* ... */ },
  update: async <T = any>(table: string, updates, filter) => { /* ... */ },
  delete: async <T = any>(table: string, filter) => { /* ... */ },
  rpc: async <T = any>(functionName: string, params = {}) => { /* ... */ },
  query: async <T = any>(query: string, params = []) => { /* ... */ },
  auth: {
    signInWithPassword: async (email: string, password: string) => { /* ... */ },
    signUp: async (email: string, password: string, options = {}) => { /* ... */ },
    signOut: async () => { /* ... */ },
    getUser: async () => { /* ... */ },
    getSession: async () => { /* ... */ },
  },
};

// Hook para usar el cliente MCP
export function useSupabaseMCP() {
  return supabaseMCPClient;
}
```

## Autenticación

### Servicio de Autenticación MCP

El servicio de autenticación MCP (`src/services/authMCPService.ts`) proporciona funciones para:

- Iniciar sesión con email y contraseña
- Registrar nuevos usuarios
- Cerrar sesión
- Obtener el usuario actual
- Verificar si el usuario está autenticado

### Contexto de Autenticación MCP

El contexto de autenticación MCP (`src/contexts/AuthMCPContext.tsx`) proporciona:

- Estado del usuario actual
- Estado de carga
- Funciones para iniciar sesión, registrarse y cerrar sesión

### Uso del Contexto de Autenticación MCP

```tsx
import { useAuthMCP } from "@/contexts/AuthMCPContext";

function MyComponent() {
  const { user, loading, login, register, logout } = useAuthMCP();

  // Usar las funciones y el estado según sea necesario
}
```

## Acceso a Datos

### Hook Personalizado

El hook `useSupabaseMCPData` (`src/hooks/useSupabaseMCPData.ts`) proporciona funciones para:

- Obtener todos los registros de una tabla
- Obtener un registro por su ID
- Crear un nuevo registro
- Actualizar un registro existente
- Eliminar un registro

### Uso del Hook

```tsx
import { useSupabaseMCPData } from "@/hooks/useSupabaseMCPData";
import { Database } from "@/types/supabase";

type Campaign = Database["public"]["Tables"]["campaigns"]["Row"];

function CampaignList() {
  const campaignsData = useSupabaseMCPData<Campaign>("campaigns");
  
  // Obtener todas las campañas
  const loadCampaigns = async () => {
    const campaigns = await campaignsData.getAll({
      order: { column: "created_at", ascending: false },
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

También puedes usar el cliente MCP directamente:

```tsx
import { useSupabaseMCP } from "@/lib/supabase-mcp";

function MyComponent() {
  const supabaseMCP = useSupabaseMCP();
  
  async function fetchData() {
    const { data, error } = await supabaseMCP.select("campaigns", {
      order: { column: "created_at", ascending: false },
      limit: 10,
    });
    
    if (error) {
      console.error("Error:", error.message);
      return;
    }
    
    // Hacer algo con los datos
  }
}
```

## Consultas SQL Personalizadas

El cliente MCP permite ejecutar consultas SQL personalizadas:

```tsx
import { useSupabaseMCP } from "@/lib/supabase-mcp";

function MyComponent() {
  const supabaseMCP = useSupabaseMCP();
  
  async function runCustomQuery() {
    const { data, error } = await supabaseMCP.query(
      "SELECT * FROM campaigns WHERE status = $1 ORDER BY created_at DESC LIMIT 5",
      ["active"]
    );
    
    if (error) {
      console.error("Error:", error.message);
      return;
    }
    
    // Hacer algo con los datos
  }
}
```

## Ejemplo Completo

Se proporciona un componente de ejemplo en `src/components/examples/SupabaseMCPExample.tsx` que muestra cómo:

- Cargar datos de Supabase a través del MCP
- Crear nuevos registros
- Eliminar registros
- Ejecutar consultas SQL personalizadas
- Manejar estados de carga y errores

## Ventajas del MCP

1. **Seguridad**: El MCP proporciona una capa adicional de seguridad al no exponer directamente las credenciales de Supabase en el cliente.
2. **Flexibilidad**: Permite ejecutar consultas SQL personalizadas y funciones RPC.
3. **Rendimiento**: Puede mejorar el rendimiento al optimizar las consultas y reducir la cantidad de datos transferidos.
4. **Integración**: Se integra perfectamente con el entorno de desarrollo y proporciona una experiencia de desarrollo más fluida.

## Mejores Prácticas

1. **Centralización**: Usa el cliente MCP centralizado en `src/lib/supabase-mcp.ts`
2. **Tipado**: Utiliza los tipos definidos en `src/types/supabase.ts`
3. **Hooks**: Usa el hook `useSupabaseMCPData` para operaciones CRUD comunes
4. **Manejo de Errores**: Siempre maneja los errores de las operaciones del MCP
5. **Autenticación**: Usa el contexto de autenticación MCP para gestionar el estado del usuario

## Recursos Adicionales

- [Documentación de Supabase](https://supabase.io/docs)
- [Documentación del MCP](https://supabase.io/docs/guides/mcp)
- [Guía de Autenticación de Supabase](https://supabase.io/docs/guides/auth)
