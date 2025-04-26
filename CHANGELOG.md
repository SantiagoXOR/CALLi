# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1-MVP] - 2025-06-02

### Seguridad

#### Frontend
- Actualizado Next.js de 13.4.12 a 14.2.15 para solucionar vulnerabilidades críticas
- Actualizado eslint-config-next a 14.2.15 para mantener compatibilidad
- Actualizado postcss a 8.4.31 para solucionar vulnerabilidad moderada
- Actualizado zod a 3.22.4 para solucionar vulnerabilidad moderada
- Actualizado msw a 2.7.5 para solucionar vulnerabilidad en cookie

#### Backend
- Actualizado pip a 25.0.1 para solucionar vulnerabilidad
- Actualizado python-semantic-release a 9.8.8 para solucionar vulnerabilidades
- Reemplazado python-jose por PyJWT 2.10.1 para eliminar vulnerabilidades inherentes
- Eliminado ecdsa para solucionar vulnerabilidades

#### Infraestructura
- Implementado flujo de trabajo de GitHub Actions para verificaciones de seguridad automáticas
- Configurado Dependabot para actualizaciones automáticas de dependencias

## [1.0.0-MVP] - 2025-06-01

### Añadido

#### Backend
- Implementación de endpoints CRUD para gestión de contactos
- Refinamiento de endpoints de llamadas
- Implementación de endpoints para reportes básicos
- Sistema de caché con Redis para optimizar rendimiento
- Integración con Twilio para manejo de llamadas
- Integración con ElevenLabs para síntesis de voz
- Servicio de conversación con IA optimizado para diferentes tipos de campañas
- Sistema de autenticación con Supabase
- Configuración de roles y permisos
- Middleware de autenticación
- Manejo de webhooks de Twilio
- Caché de audio generado
- Configuración de voces predeterminadas por tipo de campaña

#### Frontend
- Vista de gestión de contactos (ContactList, ContactForm, ContactImport)
- Vista de campañas (CampaignListView, CampaignCreateView, CampaignDetailView)
- Vista de llamadas con filtros y detalles
- Vista de reportes básicos
- Implementación de estados de carga (skeletons)
- Sistema de notificaciones mejorado
- Validaciones de formularios
- Páginas de login/registro
- Gestión de perfil de usuario
- Componentes UI reutilizables con Radix UI

#### Infraestructura
- Configuración de Docker para desarrollo y producción
- Configuración de CI/CD con GitHub Actions
- Implementación de pruebas unitarias, de integración y end-to-end
- Monitoreo con Prometheus y Grafana
- Configuración de alertas para errores críticos

### Corregido
- Problemas de rendimiento en la generación de audio
- Errores de manejo de estado en componentes de React
- Problemas de concurrencia en el servicio de llamadas
- Validaciones de datos en formularios

### Seguridad
- Implementación de rate limiting
- Configuración adecuada de CORS
- Validación de datos avanzada
- Encriptación de datos sensibles
- Protección contra ataques comunes (XSS, CSRF)
