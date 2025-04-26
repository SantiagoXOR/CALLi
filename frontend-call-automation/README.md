# Proyecto de Automatización de Llamadas - Frontend

Este repositorio contiene el frontend del proyecto de automatización de llamadas, una aplicación web para gestionar campañas de llamadas telefónicas automatizadas.

## Características

- Gestión de contactos (crear, editar, eliminar, importar)
- Gestión de campañas de llamadas (crear, editar, eliminar)
- Programación de llamadas
- Seguimiento de resultados
- Informes y análisis

## Tecnologías

- **Framework**: Next.js
- **Lenguaje**: TypeScript
- **Estilos**: Tailwind CSS
- **Gestión de Estado**: React Query
- **Formularios**: React Hook Form + Zod
- **Componentes UI**: Shadcn UI
- **Pruebas**: Jest, React Testing Library, Cypress

## Requisitos

- Node.js 18.x o superior
- npm 9.x o superior

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/frontend-call-automation.git
   cd frontend-call-automation
   ```

2. Instalar dependencias:
   ```bash
   npm install
   ```

3. Configurar variables de entorno:
   ```bash
   cp .env.example .env.local
   ```
   Editar `.env.local` con los valores adecuados.

4. Iniciar el servidor de desarrollo:
   ```bash
   npm run dev
   ```

5. Abrir [http://localhost:3000](http://localhost:3000) en el navegador.

## Estructura del Proyecto

```
frontend-call-automation/
├── public/              # Archivos estáticos
├── src/                 # Código fuente
│   ├── app/             # Rutas de Next.js
│   ├── components/      # Componentes React
│   ├── hooks/           # Hooks personalizados
│   ├── lib/             # Utilidades y configuraciones
│   ├── services/        # Servicios de API
│   ├── styles/          # Estilos globales
│   └── types/           # Definiciones de tipos
├── cypress/             # Pruebas end-to-end
├── docs/                # Documentación
└── __tests__/           # Utilidades para pruebas
```

## Scripts Disponibles

- `npm run dev`: Inicia el servidor de desarrollo
- `npm run build`: Construye la aplicación para producción
- `npm start`: Inicia la aplicación en modo producción
- `npm run lint`: Ejecuta el linter
- `npm test`: Ejecuta las pruebas unitarias y de integración
- `npm run test:watch`: Ejecuta las pruebas en modo watch
- `npm run test:coverage`: Genera un informe de cobertura
- `npm run cypress`: Abre Cypress en modo interactivo
- `npm run cypress:run`: Ejecuta las pruebas de Cypress en modo headless
- `npm run test:e2e`: Ejecuta las pruebas end-to-end con el servidor de desarrollo

## Pruebas

El proyecto utiliza diferentes niveles de pruebas para garantizar la calidad del código:

1. **Pruebas Unitarias**: Prueban componentes y servicios de forma aislada.
2. **Pruebas de Integración**: Prueban la interacción entre componentes.
3. **Pruebas End-to-End**: Prueban flujos completos de la aplicación.

Para más información sobre las pruebas, consulta [TESTING.md](./TESTING.md) y [docs/writing-tests.md](./docs/writing-tests.md).

## Integración Continua

El proyecto utiliza GitHub Actions para ejecutar pruebas automáticamente en cada push y pull request. La configuración se encuentra en `.github/workflows/tests.yml`.

## Contribuir

1. Crear una rama para la nueva funcionalidad:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. Realizar cambios y asegurarse de que las pruebas pasen:
   ```bash
   npm test
   ```

3. Enviar un pull request a la rama principal.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
