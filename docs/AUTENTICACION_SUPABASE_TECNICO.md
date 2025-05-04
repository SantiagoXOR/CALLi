# Documentación Técnica: Sistema de Autenticación con Supabase

## Introducción

El Sistema de Autenticación con Supabase es una implementación integral que proporciona funcionalidades de autenticación, autorización y gestión de usuarios para la aplicación de Automatización de Llamadas. Este documento describe la arquitectura, componentes y consideraciones técnicas de esta implementación.

## Arquitectura

### Componentes Principales

1. **Backend**:
   - **AuthMiddleware**: Middleware para verificar tokens JWT en solicitudes HTTP.
   - **AuthService**: Servicio para gestionar usuarios, roles y permisos.
   - **AuthRouter**: Endpoints para operaciones de autenticación.

2. **Frontend**:
   - **AuthContext**: Contexto de React para gestionar el estado de autenticación.
   - **ProtectedRoute**: Componente para proteger rutas que requieren autenticación.
   - **UserProfile**: Componente para mostrar información del usuario actual.
   - **Páginas de Autenticación**: Login, Registro y Recuperación de contraseña.

3. **Supabase**:
   - **Auth API**: Servicio de autenticación de Supabase.
   - **Database**: Tablas para almacenar usuarios, roles y permisos.

### Diagrama de Flujo

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Frontend    │────▶│ AuthContext │────▶│ Supabase    │
│ Components  │     │             │     │ Auth API    │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
┌─────────────┐     ┌─────────────┐          │
│ Backend     │────▶│ AuthMiddle- │◀─────────┘
│ API         │     │ ware        │
└─────────────┘     └─────────────┘
      │                    │
      ▼                    ▼
┌─────────────┐     ┌─────────────┐
│ AuthService │────▶│ Supabase    │
│             │     │ Database    │
└─────────────┘     └─────────────┘
```

## Implementación Backend

### Middleware de Autenticación

El middleware `AuthMiddleware` verifica y valida tokens JWT en las solicitudes HTTP:

```python
class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        public_routes: List[str] = None,
        public_route_prefixes: List[str] = None,
        jwt_secret: str = None,
        jwt_algorithms: List[str] = None,
    ):
        # Inicialización...

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable]
    ):
        # Verificar si la ruta es pública
        # Verificar token de autenticación
        # Añadir información de usuario a la solicitud
        # Continuar con la solicitud o devolver error
```

### Servicio de Autenticación

El servicio `AuthService` proporciona métodos para gestionar usuarios, roles y permisos:

```python
class AuthService:
    def __init__(self, supabase_client: SupabaseClient):
        self.supabase = supabase_client

    async def get_user(self, user_id: str) -> Dict[str, Any]:
        # Obtener información de un usuario

    async def get_user_roles(self, user_id: str) -> List[str]:
        # Obtener roles de un usuario

    async def check_permission(self, user_id: str, permission: str) -> bool:
        # Verificar si un usuario tiene un permiso específico

    async def create_user(self, email: str, password: str, user_metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        # Crear un nuevo usuario

    async def assign_role(self, user_id: str, role: str) -> bool:
        # Asignar un rol a un usuario

    async def remove_role(self, user_id: str, role: str) -> bool:
        # Eliminar un rol de un usuario
```

### Router de Autenticación

El router `auth_router` define endpoints para operaciones de autenticación:

```python
@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> TokenResponse:
    # Iniciar sesión con email y contraseña

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> UserResponse:
    # Registrar un nuevo usuario

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str = Body(..., embed=True),
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> TokenResponse:
    # Refrescar un token de acceso

@router.post("/logout")
async def logout(
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> Dict[str, bool]:
    # Cerrar sesión

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    supabase_client: SupabaseClient = Depends(get_supabase_client)
) -> UserResponse:
    # Obtener información del usuario actual
```

## Implementación Frontend

### Contexto de Autenticación

El contexto `AuthContext` gestiona el estado de autenticación en el frontend:

```typescript
export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Obtener sesión inicial y suscribirse a cambios
  // Métodos para iniciar sesión, registrarse, cerrar sesión, etc.

  const value = {
    session,
    user,
    isLoading,
    signIn,
    signUp,
    signOut,
    resetPassword,
    updatePassword,
    updateProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
```

### Componente de Ruta Protegida

El componente `ProtectedRoute` protege rutas que requieren autenticación:

```typescript
export function ProtectedRoute({
  children,
  requiredRoles = [],
}: ProtectedRouteProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hasRequiredRoles, setHasRequiredRoles] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    // Verificar autenticación y roles
    // Redirigir si no está autenticado o no tiene los roles requeridos
  }, [pathname, router, requiredRoles]);

  // Mostrar loader, contenido o nada según el estado
}
```

### Páginas de Autenticación

Se implementaron las siguientes páginas de autenticación:

1. **Login**: Formulario para iniciar sesión con email y contraseña.
2. **Registro**: Formulario para crear una nueva cuenta.
3. **Recuperación de Contraseña**: Formulario para solicitar un correo de recuperación.

Todas las páginas utilizan:
- Validación con Zod
- Formularios con React Hook Form
- Componentes UI personalizados
- Notificaciones para feedback al usuario

## Modelo de Datos

### Tablas en Supabase

1. **auth.users**: Tabla gestionada por Supabase Auth con información de usuarios.
2. **user_roles**: Tabla personalizada para asignar roles a usuarios.
3. **roles**: Tabla con definiciones de roles disponibles.
4. **role_permissions**: Tabla que relaciona roles con permisos.
5. **permissions**: Tabla con definiciones de permisos disponibles.

### Esquema de Roles y Permisos

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ users       │────▶│ user_roles  │────▶│ roles       │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐     ┌─────────────┐
                                        │ role_permi- │────▶│ permissions │
                                        │ ssions      │     │             │
                                        └─────────────┘     └─────────────┘
```

## Seguridad

### Consideraciones de Seguridad

1. **Tokens JWT**: Se utilizan tokens JWT para autenticación, con tiempo de expiración limitado.
2. **Refresh Tokens**: Se implementa un sistema de refresh tokens para renovar sesiones.
3. **HTTPS**: Todas las comunicaciones se realizan sobre HTTPS.
4. **Validación**: Se validan todas las entradas de usuario en frontend y backend.
5. **Protección CSRF**: Supabase proporciona protección contra ataques CSRF.
6. **Almacenamiento Seguro**: Las contraseñas se almacenan con hash y salt.

### Buenas Prácticas Implementadas

1. **Principio de Menor Privilegio**: Los usuarios solo tienen acceso a lo que necesitan.
2. **Validación en Ambos Extremos**: Se valida tanto en cliente como en servidor.
3. **Mensajes de Error Genéricos**: No se revelan detalles específicos en errores de autenticación.
4. **Límite de Intentos**: Se limita el número de intentos de inicio de sesión fallidos.
5. **Auditoría**: Se registran eventos importantes de autenticación.

## Flujos de Autenticación

### Inicio de Sesión

1. Usuario ingresa email y contraseña.
2. Frontend envía credenciales a Supabase Auth.
3. Supabase verifica credenciales y devuelve tokens.
4. Frontend almacena tokens y actualiza estado de autenticación.
5. Se redirige al usuario a la página solicitada.

### Registro

1. Usuario ingresa datos de registro.
2. Frontend valida datos y envía a Supabase Auth.
3. Supabase crea usuario y envía correo de confirmación.
4. Backend asigna rol por defecto al nuevo usuario.
5. Se redirige al usuario a la página de login o dashboard.

### Verificación de Permisos

1. Usuario intenta acceder a un recurso protegido.
2. Middleware verifica token JWT.
3. Se extraen roles del usuario del token o base de datos.
4. Se verifica si el usuario tiene los permisos necesarios.
5. Se permite o deniega acceso según el resultado.

## Conclusiones

El Sistema de Autenticación con Supabase proporciona una solución robusta y segura para la gestión de usuarios y control de acceso en la aplicación. Su integración con Supabase ofrece ventajas significativas en términos de seguridad, escalabilidad y facilidad de mantenimiento.

## Referencias

- [Documentación de Supabase Auth](https://supabase.io/docs/guides/auth)
- [Mejores Prácticas de JWT](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [React Authentication Patterns](https://reactpatterns.com/#authentication)
