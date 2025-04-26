# Documentación Frontend - Sistema de Automatización de Llamadas

## Introducción

Bienvenido a la documentación frontend del Sistema de Automatización de Llamadas. Esta documentación proporciona toda la información necesaria para entender, desarrollar y mantener el frontend del proyecto.

## Índice de Documentos

### Guías Principales

1. [**Guía de Desarrollo Frontend**](./frontend-development-guide.md)  
   Guía completa que cubre todos los aspectos del desarrollo frontend, desde la arquitectura hasta las mejores prácticas.

2. [**Guía de Configuración del Entorno**](./frontend-setup-guide.md)  
   Instrucciones detalladas para configurar el entorno de desarrollo frontend.

3. [**Guía de Estilo y Mejores Prácticas**](./frontend-style-guide.md)  
   Estándares de código, convenciones y mejores prácticas para el desarrollo frontend.

4. [**Referencia de Componentes**](./frontend-components-reference.md)  
   Documentación detallada de los componentes principales utilizados en el frontend.

### Documentación Adicional

5. [**Plan de Desarrollo Frontend**](./frontend-development-plan.md)  
   Plan detallado para el desarrollo del frontend, incluyendo funcionalidades implementadas y planeadas.

6. [**Arquitectura de Componentes**](../architecture/component-architecture.md)  
   Descripción de la arquitectura general de componentes del sistema.

## Tecnologías Principales

El frontend del Sistema de Automatización de Llamadas está construido con las siguientes tecnologías:

- **Next.js (App Router)**: Framework React para renderizado del lado del servidor y generación de sitios estáticos
- **TypeScript**: Superset tipado de JavaScript
- **Tailwind CSS**: Framework CSS de utilidades
- **Shadcn/ui**: Componentes UI reutilizables
- **React Hook Form**: Gestión de formularios
- **Axios**: Cliente HTTP para comunicación con el backend
- **TanStack Query (React Query)**: Gestión de estado del servidor y caché
- **Sonner**: Notificaciones toast
- **Lucide-react**: Iconos

## Estructura del Proyecto

```
frontend-call-automation/
├── public/                 # Archivos estáticos
├── src/                    # Código fuente
│   ├── app/                # Rutas y páginas (Next.js App Router)
│   ├── components/         # Componentes React
│   │   ├── ui/             # Componentes UI reutilizables (Shadcn)
│   │   └── ...             # Componentes específicos de la aplicación
│   ├── lib/                # Utilidades y funciones auxiliares
│   ├── providers/          # Proveedores de contexto
│   ├── services/           # Servicios para comunicación con API
│   └── types/              # Definiciones de tipos TypeScript
└── ...                     # Archivos de configuración
```

## Flujo de Trabajo de Desarrollo

1. **Configuración**: Sigue la [Guía de Configuración del Entorno](./frontend-setup-guide.md) para configurar tu entorno de desarrollo.
2. **Desarrollo**: Sigue la [Guía de Desarrollo Frontend](./frontend-development-guide.md) y la [Guía de Estilo](./frontend-style-guide.md) para desarrollar nuevas funcionalidades.
3. **Componentes**: Consulta la [Referencia de Componentes](./frontend-components-reference.md) para entender y utilizar los componentes existentes.
4. **Pruebas**: Escribe pruebas para tus componentes y funcionalidades siguiendo las mejores prácticas.
5. **Revisión**: Solicita revisión de código antes de integrar tus cambios.

## Recursos Adicionales

- [Documentación de Next.js](https://nextjs.org/docs)
- [Documentación de React](https://reactjs.org/docs)
- [Documentación de TypeScript](https://www.typescriptlang.org/docs)
- [Documentación de Tailwind CSS](https://tailwindcss.com/docs)
- [Documentación de Shadcn UI](https://ui.shadcn.com)
- [Documentación de React Hook Form](https://react-hook-form.com/get-started)
- [Documentación de TanStack Query](https://tanstack.com/query/latest)

## Contribución

Para contribuir al desarrollo del frontend:

1. Asegúrate de seguir las guías de estilo y mejores prácticas.
2. Crea una rama para tu funcionalidad o corrección.
3. Escribe pruebas para tu código.
4. Solicita una revisión de código mediante un Pull Request.
5. Aborda los comentarios de la revisión.

## Soporte

Si encuentras problemas o tienes preguntas:

1. Consulta la sección de [Solución de Problemas Comunes](./frontend-setup-guide.md#6-solución-de-problemas-comunes).
2. Revisa los issues existentes en el repositorio.
3. Crea un nuevo issue si es necesario, proporcionando detalles sobre el problema.
