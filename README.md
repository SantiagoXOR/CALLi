# Sistema de Automatización de Llamadas

Este proyecto implementa un sistema de automatización de llamadas utilizando Next.js para el frontend y FastAPI para el backend, con integraciones de Supabase, Twilio y ElevenLabs.

## Estructura del Proyecto

```
call-automation-project/
├── frontend-call-automation/    # Frontend en Next.js (App Router) + Shadcn/ui
└── backend-call-automation/     # Backend en Python/FastAPI
```

## Requisitos del Sistema

- Bun (https://bun.sh/) - Para el frontend
- Python 3.9+ - Para el backend
- Docker (opcional, para facilitar despliegue/dependencias como Redis)

## Tecnologías Principales

- **Frontend**:
  - Next.js (App Router)
  - TypeScript
  - Tailwind CSS
  - Shadcn/ui
  - Axios (Peticiones API)
  - React Hook Form (Gestión de formularios)
  - Sonner (Notificaciones/Toasts)
  - Lucide-react (Iconos)

- **Backend**:
  - Python / FastAPI
  - SQLAlchemy (ORM)
  - Supabase (Base de datos PostgreSQL)
  - Twilio (API de Telefonía)
  - ElevenLabs (API de Síntesis de Voz - TTS)
  - Redis (Caché, opcionalmente vía Docker)

## Configuración Inicial

### Frontend (`frontend-call-automation`)

1.  Navegar al directorio:
    ```bash
    cd frontend-call-automation
    ```
2.  Instalar dependencias:
    ```bash
    bun install
    ```
3.  Copiar variables de entorno de ejemplo:
    ```bash
    cp .env.example .env.local
    ```
4.  Configurar las variables en `.env.local` (ver sección "Variables de Entorno").
5.  Iniciar servidor de desarrollo:
    ```bash
    bun dev
    ```
    La aplicación estará disponible en `http://localhost:3000`.

### Backend (`backend-call-automation`)

1.  Navegar al directorio:
    ```bash
    cd backend-call-automation
    ```
2.  Crear y activar entorno virtual:
    ```bash
    python -m venv venv
    # Linux/macOS:
    source venv/bin/activate
    # Windows:
    # .\venv\Scripts\activate
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Copiar variables de entorno de ejemplo:
    ```bash
    cp .env.example .env
    ```
5.  Configurar las variables en `.env` (ver sección "Variables de Entorno").
6.  Iniciar servidor:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    La API estará disponible en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

## Variables de Entorno

Crear los archivos `.env.local` (frontend) y `.env` (backend) con las siguientes variables:

### Frontend (`frontend-call-automation/.env.local`)

```dotenv
NEXT_PUBLIC_API_URL=http://localhost:8000 # URL base del backend (sin /api)
# NEXT_PUBLIC_SUPABASE_URL=your_supabase_url # Si se usa Supabase directamente desde el frontend
# NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key # Si se usa Supabase directamente desde el frontend
```

### Backend (`backend-call-automation/.env`)

```dotenv
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_key # ¡Clave de servicio, mantener segura!
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number # Número de Twilio para realizar llamadas
ELEVENLABS_API_KEY=your_elevenlabs_api_key
# REDIS_URL=redis://localhost:6379 # Opcional, si se usa Redis para caché
# DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname # Alternativa a Supabase Key si se conecta directamente
```

## Características Implementadas

*   **Backend:**
    *   API REST con FastAPI.
    *   Modelos de datos (Campaign, Call, Contact, etc.) con SQLAlchemy.
    *   Integración con Supabase para persistencia.
    *   Servicios para lógica de negocio (Campañas, Llamadas, Contactos, IA, TTS con ElevenLabs, Telefonía con Twilio).
    *   Endpoints CRUD para Campañas.
    *   Sistema básico de caché con Redis (opcional).
    *   Configuración de CORS, dependencias, etc.
*   **Frontend:**
    *   Interfaz con Next.js (App Router) y TypeScript.
    *   Estilos con Tailwind CSS y componentes Shadcn/ui.
    *   Servicio API (`axios`) para comunicarse con el backend.
    *   Gestión completa (CRUD) de Campañas:
        *   Listado de campañas.
        *   Formulario de creación con validación (`react-hook-form`).
        *   Página de detalles de campaña.
        *   Formulario de edición reutilizando el componente de creación.
        *   Funcionalidad de eliminación con confirmación.
    *   Notificaciones de feedback (`sonner`).

## Documentación

La documentación es una parte integral del proceso de desarrollo en este proyecto. Seguimos un enfoque de "documentación como código" donde la documentación se desarrolla y mantiene junto con el código.

### Índice de Documentación

Toda la documentación del proyecto está centralizada en el [Índice de Documentación](./docs/DOCUMENTATION_INDEX.md).

### Documentación para Desarrolladores

- **Estándares de Documentación:** [DOCUMENTATION_STANDARDS.md](./docs/DOCUMENTATION_STANDARDS.md)
- **Flujo de Trabajo de Documentación:** [DOCUMENTATION_WORKFLOW.md](./docs/DOCUMENTATION_WORKFLOW.md)
- **Documentación como Código:** [DOCUMENTATION_AS_CODE.md](./docs/DOCUMENTATION_AS_CODE.md)
- **Integración CI/CD:** [CI_CD_DOCUMENTATION.md](./docs/CI_CD_DOCUMENTATION.md)

### Documentación de Componentes

- **Plan de Desarrollo Frontend:** [`frontend-call-automation/docs/frontend-development-plan.md`](./frontend-call-automation/docs/frontend-development-plan.md)
- **Documentación Backend/API:** Ver la documentación interactiva generada por FastAPI en `/docs` cuando el backend está corriendo, o los archivos dentro de [`backend-call-automation/docs/`](./backend-call-automation/docs/).

### Contribución y Calidad

- **Contribución:** [`CONTRIBUTING.md`](./CONTRIBUTING.md)
- **Calidad del Código:** [`QUALITY.md`](./QUALITY.md) (Si existe)

## Licencia

MIT
