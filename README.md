# CALLi - Sistema Avanzado de Automatización de Llamadas

<div align="center">
  <img src="docs/assets/calli-logo.png" alt="CALLi Logo" width="200"/>
  <p><strong>Transformando la comunicación telefónica con inteligencia artificial</strong></p>
</div>

## 🌟 Descripción

CALLi es una plataforma integral de automatización de llamadas que combina tecnologías de vanguardia para transformar la manera en que las empresas se comunican con sus clientes. Utilizando inteligencia artificial, síntesis de voz natural y análisis avanzado, CALLi permite crear, gestionar y analizar campañas telefónicas con una eficiencia sin precedentes.

### ¿Por qué CALLi?

- **Comunicación Natural**: Voces generadas por IA indistinguibles de humanos gracias a ElevenLabs
- **Flexibilidad Total**: Personalización completa de flujos de llamadas y respuestas
- **Análisis en Tiempo Real**: Métricas detalladas y insights accionables
- **Escalabilidad**: Desde pequeñas campañas hasta operaciones a gran escala
- **Integración Sencilla**: Conecta con tus sistemas existentes a través de APIs

Construido con Next.js para el frontend y FastAPI para el backend, con integraciones de Supabase, Twilio y ElevenLabs.

## 🏗️ Estructura del Proyecto

```bash
call-automation-project/
├── frontend-call-automation/    # Frontend en Next.js (App Router) + Shadcn/ui
├── backend-call-automation/     # Backend en Python/FastAPI
├── docs/                        # Documentación general del proyecto
├── scripts/                     # Scripts de utilidad y despliegue
└── .github/                     # Configuración de CI/CD y GitHub Actions
```

## 🛠️ Requisitos del Sistema

- **Frontend**:
  - [Bun](https://bun.sh/) (v1.0.0+) - Gestor de paquetes y entorno de ejecución
  - Node.js (v18+) - Alternativa a Bun si es necesario

- **Backend**:
  - Python 3.9+ - Lenguaje principal
  - FastAPI - Framework web
  - PostgreSQL - Base de datos (vía Supabase)

- **Opcional**:
  - Docker - Para contenedores y despliegue
  - Redis - Para caché y gestión de colas

## ✨ Características Destacadas

- **Campañas Inteligentes**: Crea campañas de llamadas con flujos de conversación dinámicos
- **Voces Naturales**: Integración con ElevenLabs para síntesis de voz de alta calidad
- **Análisis Detallado**: Métricas completas de rendimiento de campañas y llamadas
- **Interfaz Intuitiva**: Panel de control moderno y fácil de usar
- **Escalabilidad**: Arquitectura diseñada para manejar desde decenas hasta miles de llamadas
- **Seguridad**: Protección de datos y cumplimiento de normativas

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

## 🚀 Características Implementadas

- **Backend:**
  - API REST con FastAPI y documentación automática con Swagger/OpenAPI
  - Modelos de datos (Campaign, Call, Contact, etc.) con SQLAlchemy
  - Integración con Supabase para persistencia de datos
  - Servicios para lógica de negocio (Campañas, Llamadas, Contactos)
  - Integración con ElevenLabs para síntesis de voz natural
  - Integración con Twilio para gestión de llamadas telefónicas
  - Endpoints CRUD completos para gestión de campañas
  - Sistema de caché con Redis para optimización de rendimiento
  - Configuración de CORS, middleware y dependencias

- **Frontend:**
  - Interfaz moderna con Next.js (App Router) y TypeScript
  - Diseño responsive con Tailwind CSS y componentes Shadcn/ui
  - Servicio API centralizado con Axios para comunicación con backend
  - Gestión completa (CRUD) de campañas:
    - Listado de campañas con filtros y búsqueda
    - Formulario de creación con validación avanzada
    - Página de detalles con métricas y estadísticas
    - Edición y actualización de campañas existentes
    - Eliminación con confirmación para prevenir errores
  - Sistema de notificaciones con Sonner para feedback al usuario
  - Autenticación y gestión de sesiones con NextAuth

## 👥 Contribución

¿Quieres contribuir al proyecto? ¡Genial! Sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Configura pre-commit para verificar tu código:
   ```bash
   pip install pre-commit
   pre-commit install
   ```
4. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
5. Haz push a la rama (`git push origin feature/amazing-feature`)
6. Abre un Pull Request

Por favor, asegúrate de seguir nuestras [guías de contribución](./CONTRIBUTING.md) y el [código de conducta](./CODE_OF_CONDUCT.md).

### Verificación de código con pre-commit

Este proyecto utiliza pre-commit para verificar el código antes de hacer commits. Para configurarlo:

```bash
# Método 1: Usando nuestros scripts de instalación (recomendado)
# Windows
.\scripts\install_precommit_deps.ps1

# Linux/macOS
./scripts/install_precommit_deps.sh

# Método 2: Instalación manual
pip install pre-commit
pre-commit install

# Ejecutar pre-commit en todos los archivos (opcional)
pre-commit run --all-files
```

Los hooks de pre-commit verificarán automáticamente tu código cada vez que hagas un commit, asegurando que cumpla con los estándares del proyecto y detectando problemas de seguridad como:

- Secretos hardcodeados (con gitleaks)
- Vulnerabilidades de seguridad (con bandit)
- Problemas de configuración (con KICS)
- Vulnerabilidades en dependencias (con safety)

### Scripts de Verificación de Calidad

El proyecto incluye varios scripts para verificar y mejorar la calidad del código:

```bash
# Verificar y corregir formato con Ruff
.\scripts\run_ruff.ps1 --fix

# Verificar tipos con MyPy
.\scripts\run_mypy.ps1

# Verificar y generar docstrings
.\scripts\run_docstring_check.ps1
.\scripts\run_docstring_fix.ps1

# Corregir errores de tipo comunes
.\scripts\run_type_fixes.ps1

# Verificar y corregir problemas de seguridad
.\scripts\run_security_checks.ps1
.\scripts\fix_security_issues.ps1

# Ejecutar todas las verificaciones de calidad
.\scripts\run_all_quality_checks.ps1 [--fix]
```

Para más detalles sobre las mejoras de calidad implementadas, consulta [QUALITY_IMPROVEMENTS.md](./QUALITY_IMPROVEMENTS.md).

#### Solución de problemas comunes con pre-commit

Si encuentras errores al ejecutar pre-commit, prueba lo siguiente:

1. **Comando `check` obsoleto**: Si ves un error sobre el comando `check` obsoleto, actualiza pre-commit:
   ```bash
   pip install --upgrade pre-commit
   ```

2. **Herramientas faltantes**: Si faltan herramientas como `gitleaks` o `kics`, usa nuestro script:
   ```bash
   python scripts/install_precommit_deps.py
   ```

3. **Errores de manejo de excepciones**: Asegúrate de usar `logging.exception` en lugar de `logging.error` cuando captures excepciones, y usa `raise ... from err` para preservar el contexto de la excepción.

4. **Problemas con MyPy**: Si MyPy reporta errores sobre archivos duplicados, asegúrate de que todos los directorios de paquetes tengan un archivo `__init__.py`.

## 📚 Documentación

La documentación es una parte integral del proceso de desarrollo en este proyecto. Seguimos un enfoque de "documentación como código" donde la documentación se desarrolla y mantiene junto con el código.

### 📑 Índice de Documentación

Toda la documentación del proyecto está centralizada en el [Índice de Documentación](./docs/DOCUMENTATION_INDEX.md).

### 👨‍💻 Documentación para Desarrolladores

- **Guía de Inicio Rápido:** [QUICKSTART.md](./docs/QUICKSTART.md)
- **Estándares de Código:** [CODE_STANDARDS.md](./docs/CODE_STANDARDS.md)
- **Flujo de Trabajo de Desarrollo:** [DEVELOPMENT_WORKFLOW.md](./docs/DEVELOPMENT_WORKFLOW.md)
- **Integración CI/CD:** [CI_CD.md](./docs/CI_CD.md)

### 🧩 Documentación de Componentes

- **API Backend:** Documentación interactiva generada por FastAPI en `http://localhost:8000/docs` cuando el backend está corriendo
- **Arquitectura Frontend:** [frontend-call-automation/docs/ARCHITECTURE.md](./frontend-call-automation/docs/ARCHITECTURE.md)
- **Integración con Twilio:** [docs/integrations/TWILIO.md](./docs/integrations/TWILIO.md)
- **Integración con ElevenLabs:** [docs/integrations/ELEVENLABS.md](./docs/integrations/ELEVENLABS.md)

### 🔄 Flujos de Trabajo

- **Gestión de Campañas:** [docs/workflows/CAMPAIGN_MANAGEMENT.md](./docs/workflows/CAMPAIGN_MANAGEMENT.md)
- **Procesamiento de Llamadas:** [docs/workflows/CALL_PROCESSING.md](./docs/workflows/CALL_PROCESSING.md)
- **Análisis de Datos:** [docs/workflows/DATA_ANALYSIS.md](./docs/workflows/DATA_ANALYSIS.md)

## 🛡️ Seguridad

CALLi toma muy en serio la seguridad de los datos. Implementamos:

- Cifrado de datos sensibles en reposo y en tránsito
- Autenticación multifactor para acceso administrativo
- Auditoría completa de acciones de usuario
- Cumplimiento con regulaciones de protección de datos
- Verificación automática de seguridad con pre-commit
- Detección de secretos con gitleaks
- Análisis de vulnerabilidades en dependencias
- Verificación de encabezados HTTP de seguridad

### Herramientas de Seguridad

El proyecto incluye varias herramientas para verificar y mejorar la seguridad:

```bash
# Windows
.\scripts\run_security_checks.ps1
.\scripts\verify_config_security.ps1
.\scripts\run_security_headers_check.ps1
.\scripts\run_gitleaks.ps1

# Linux/macOS
./scripts/run_security_checks.sh
./scripts/verify_config_security.sh
./scripts/check_security_headers.py
./scripts/run_gitleaks.sh
```

Para configurar pre-commit con todas las verificaciones de seguridad:

```bash
# Windows
.\scripts\install_precommit_deps.ps1

# Linux/macOS
./scripts/install_precommit_deps.sh
```

Para más detalles sobre las herramientas de seguridad, consulta [docs/SECURITY_TOOLS_GUIDE.md](./docs/SECURITY_TOOLS_GUIDE.md) y [docs/SECURITY.md](./docs/SECURITY.md).

Para reportar vulnerabilidades de seguridad, por favor contacta a [santiago@xor.com.ar](mailto:santiago@xor.com.ar).

## 📊 Estado del Proyecto

CALLi está actualmente en fase beta. Estamos trabajando activamente en nuevas características y mejoras.

- ✅ API Core y funcionalidades básicas
- ✅ Integración con Twilio y ElevenLabs
- ✅ Panel de administración frontend
- 🔄 Análisis avanzado de llamadas (en progreso)
- 🔄 Integración con CRM (en progreso)
- 📅 Aplicación móvil (planificada)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">
  <p>Desarrollado con ❤️ por el equipo de CALLi</p>
  <p>© 2023-2024 CALLi - Todos los derechos reservados</p>
</div>
