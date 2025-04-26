# Guía de Configuración del Entorno de Desarrollo Frontend

Esta guía proporciona instrucciones detalladas para configurar el entorno de desarrollo frontend del Sistema de Automatización de Llamadas.

## Índice

1. [Requisitos Previos](#1-requisitos-previos)
2. [Instalación](#2-instalación)
3. [Configuración del Editor](#3-configuración-del-editor)
4. [Configuración del Proyecto](#4-configuración-del-proyecto)
5. [Ejecución del Proyecto](#5-ejecución-del-proyecto)
6. [Solución de Problemas Comunes](#6-solución-de-problemas-comunes)

## 1. Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

### 1.1 Node.js y npm

Se recomienda Node.js v18.0.0 o superior.

**Windows**:
- Descarga e instala desde [nodejs.org](https://nodejs.org/)

**macOS**:
```bash
# Con Homebrew
brew install node
```

**Linux**:
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Fedora
sudo dnf install nodejs
```

### 1.2 Bun (Recomendado)

Bun es un runtime y gestor de paquetes más rápido que npm.

**Instalación**:
```bash
# Windows (requiere WSL), macOS, Linux
curl -fsSL https://bun.sh/install | bash
```

### 1.3 Git

**Windows**:
- Descarga e instala desde [git-scm.com](https://git-scm.com/download/win)

**macOS**:
```bash
# Con Homebrew
brew install git
```

**Linux**:
```bash
# Ubuntu/Debian
sudo apt-get install git

# Fedora
sudo dnf install git
```

### 1.4 Editor de Código

Se recomienda Visual Studio Code (VS Code).

- Descarga e instala desde [code.visualstudio.com](https://code.visualstudio.com/)

## 2. Instalación

### 2.1 Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/call-automation-project.git
cd call-automation-project
```

### 2.2 Instalar Dependencias del Frontend

```bash
cd frontend-call-automation

# Con npm
npm install

# Con Bun (recomendado)
bun install
```

### 2.3 Configurar Variables de Entorno

1. Copia el archivo de ejemplo de variables de entorno:
   ```bash
   cp .env.example .env.local
   ```

2. Edita `.env.local` con los valores correctos:
   ```
   # API Configuration
   NEXT_PUBLIC_API_URL=http://localhost:8000/api

   # Supabase Configuration (si aplica)
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

   # Authentication (si aplica)
   NEXTAUTH_URL=http://localhost:3000
   NEXTAUTH_SECRET=your_nextauth_secret

   # Feature Flags
   NEXT_PUBLIC_ENABLE_ANALYTICS=false
   NEXT_PUBLIC_MAINTENANCE_MODE=false
   ```

## 3. Configuración del Editor

### 3.1 Extensiones Recomendadas para VS Code

Instala las siguientes extensiones para mejorar tu experiencia de desarrollo:

1. **ESLint**: Integración de ESLint
   - ID: `dbaeumer.vscode-eslint`

2. **Prettier - Code formatter**: Formateador de código
   - ID: `esbenp.prettier-vscode`

3. **Tailwind CSS IntelliSense**: Autocompletado para clases de Tailwind
   - ID: `bradlc.vscode-tailwindcss`

4. **TypeScript Hero**: Organización de importaciones
   - ID: `rbbit.typescript-hero`

5. **Error Lens**: Resalta errores y advertencias
   - ID: `usernamehw.errorlens`

6. **Path Intellisense**: Autocompletado de rutas
   - ID: `christian-kohler.path-intellisense`

7. **Import Cost**: Muestra el tamaño de los paquetes importados
   - ID: `wix.vscode-import-cost`

8. **GitLens**: Mejoras para Git
   - ID: `eamodio.gitlens`

### 3.2 Configuración de VS Code

Crea o edita el archivo `.vscode/settings.json` en la raíz del proyecto:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.tabSize": 2,
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "tailwindCSS.includeLanguages": {
    "typescript": "javascript",
    "typescriptreact": "javascript"
  },
  "tailwindCSS.experimental.classRegex": [
    ["cva\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"],
    ["cn\\(([^)]*)\\)", "[\"'`]([^\"'`]*).*?[\"'`]"]
  ],
  "files.associations": {
    "*.css": "tailwindcss"
  }
}
```

## 4. Configuración del Proyecto

### 4.1 ESLint y Prettier

El proyecto ya viene configurado con ESLint y Prettier. Los archivos de configuración son:

- `.eslintrc.js`: Configuración de ESLint
- `.prettierrc`: Configuración de Prettier

### 4.2 TypeScript

La configuración de TypeScript se encuentra en `tsconfig.json`. No es necesario modificarla a menos que necesites añadir rutas personalizadas o cambiar opciones específicas.

### 4.3 Tailwind CSS

La configuración de Tailwind CSS se encuentra en `tailwind.config.js`. Puedes personalizar temas, plugins y otras opciones según sea necesario.

### 4.4 Next.js

La configuración de Next.js se encuentra en `next.config.js`. Puedes modificarla para añadir redirecciones, reescrituras, optimización de imágenes, etc.

## 5. Ejecución del Proyecto

### 5.1 Iniciar el Servidor de Desarrollo

```bash
# Con npm
npm run dev

# Con Bun
bun dev
```

Esto iniciará el servidor de desarrollo en `http://localhost:3000`.

### 5.2 Construir para Producción

```bash
# Con npm
npm run build

# Con Bun
bun run build
```

### 5.3 Iniciar en Modo Producción

```bash
# Con npm
npm run start

# Con Bun
bun start
```

### 5.4 Ejecutar Pruebas

```bash
# Con npm
npm run test
npm run test:watch  # Modo observador

# Con Bun
bun test
bun test:watch
```

### 5.5 Ejecutar Linting

```bash
# Con npm
npm run lint

# Con Bun
bun lint
```

## 6. Solución de Problemas Comunes

### 6.1 Errores de Dependencias

Si encuentras errores relacionados con dependencias:

```bash
# Limpiar caché de npm
npm cache clean --force

# Eliminar node_modules y reinstalar
rm -rf node_modules
rm -rf .next
npm install
```

### 6.2 Errores de TypeScript

Si encuentras errores de TypeScript que no puedes resolver:

```bash
# Verificar tipos
npm run type-check

# Reiniciar el servidor de TypeScript en VS Code
# Presiona Ctrl+Shift+P y escribe "TypeScript: Restart TS Server"
```

### 6.3 Problemas con Next.js

Si encuentras problemas con Next.js:

```bash
# Limpiar caché de Next.js
rm -rf .next

# Reconstruir
npm run build
```

### 6.4 Problemas con Tailwind CSS

Si las clases de Tailwind no se aplican correctamente:

1. Asegúrate de que los archivos estén incluidos en la configuración de contenido en `tailwind.config.js`
2. Reinicia el servidor de desarrollo
3. Verifica que no haya errores en la consola

### 6.5 Problemas con el Backend

Si no puedes conectarte al backend:

1. Verifica que el backend esté en ejecución
2. Comprueba que la URL en `.env.local` sea correcta
3. Verifica que no haya problemas de CORS

### 6.6 Problemas con Docker

Si estás utilizando Docker y encuentras problemas:

```bash
# Reconstruir la imagen
docker-compose build frontend

# Reiniciar el contenedor
docker-compose restart frontend

# Ver logs
docker-compose logs -f frontend
```

## 7. Recursos Adicionales

- [Documentación de Next.js](https://nextjs.org/docs)
- [Documentación de React](https://reactjs.org/docs)
- [Documentación de TypeScript](https://www.typescriptlang.org/docs)
- [Documentación de Tailwind CSS](https://tailwindcss.com/docs)
- [Documentación de Shadcn UI](https://ui.shadcn.com)
- [Documentación de React Hook Form](https://react-hook-form.com/get-started)
- [Documentación de TanStack Query](https://tanstack.com/query/latest)
