# Instrucciones para la Ejecución del Despliegue del MVP

Este documento proporciona instrucciones detalladas para ejecutar los próximos pasos recomendados para el despliegue del MVP del Sistema de Automatización de Llamadas.

## Resumen de Pasos

1. Ejecutar el checklist de despliegue paso a paso
2. Realizar las pruebas con usuarios reales según el plan establecido
3. Implementar un despliegue gradual para minimizar riesgos
4. Mantener un monitoreo intensivo durante las primeras semanas
5. Priorizar y corregir rápidamente los problemas identificados

## Preparación Inicial

Antes de comenzar, asegúrate de tener los siguientes requisitos:

- Git instalado y configurado
- Docker y Docker Compose instalados
- Acceso a las cuentas de servicios externos (Supabase, Twilio, ElevenLabs, OpenAI)
- Permisos de administrador en el repositorio
- Acceso al servidor de producción

## 1. Ejecutar el Checklist de Despliegue

Hemos creado un script para automatizar algunas verificaciones del checklist de despliegue:

```bash
# Dar permisos de ejecución al script
chmod +x scripts/deployment_verification.sh

# Ejecutar el script
./scripts/deployment_verification.sh
```

Este script verificará:
- Que estás en la rama principal
- Que no hay cambios sin commitear
- Que CHANGELOG.md existe y está actualizado
- Que las pruebas unitarias pasan
- Que las variables de entorno están configuradas
- Que Docker y Docker Compose están instalados
- Que los archivos Docker existen

Después de ejecutar el script, sigue el checklist completo en `docs/deployment/deployment-checklist.md` para completar todas las verificaciones manuales.

Para un plan detallado de ejecución del despliegue, consulta `docs/PLAN_EJECUCION_DESPLIEGUE.md`.

## 2. Realizar Pruebas con Usuarios Reales

Hemos creado un script para preparar el entorno de staging para las pruebas de usuario:

```bash
# Dar permisos de ejecución al script
chmod +x scripts/prepare_staging_for_testing.sh

# Ejecutar el script
./scripts/prepare_staging_for_testing.sh
```

Este script:
- Crea un archivo `docker-compose.staging.yml`
- Configura un servicio para cargar datos de ejemplo
- Crea un archivo `.env.staging`
- Proporciona instrucciones para iniciar el entorno de staging

Después de preparar el entorno, sigue el plan de pruebas de usuario en `docs/testing/user-testing-plan.md` y utiliza el formulario de feedback en `docs/testing/user-feedback-form.md`.

## 3. Implementar un Despliegue Gradual

Para implementar un despliegue gradual, sigue estos pasos:

1. **Configurar Feature Flags**:
   
   Añade un sistema de feature flags al backend y frontend para controlar el acceso a las funcionalidades:

   ```bash
   # Ejemplo de implementación de feature flags en el backend
   cd backend-call-automation
   pip install flagsmith
   ```

2. **Definir Grupos de Usuarios**:
   
   Crea grupos de usuarios para el despliegue gradual:
   - Grupo 1: 10% de usuarios (equipo interno)
   - Grupo 2: 25% de usuarios (beta testers)
   - Grupo 3: 50% de usuarios (early adopters)
   - Grupo 4: 100% de usuarios

3. **Configurar Despliegue por Fases**:
   
   Utiliza el siguiente comando para desplegar cada fase:

   ```bash
   # Fase 1: 10% de usuarios
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   
   # Actualizar feature flags para la Fase 1
   # Monitorear y evaluar
   
   # Fase 2: 25% de usuarios
   # Actualizar feature flags para la Fase 2
   # Monitorear y evaluar
   
   # Y así sucesivamente...
   ```

## 4. Mantener un Monitoreo Intensivo

Hemos creado un script para configurar el monitoreo intensivo:

```bash
# Dar permisos de ejecución al script
chmod +x scripts/setup_monitoring.sh

# Ejecutar el script
./scripts/setup_monitoring.sh
```

Este script:
- Crea directorios para dashboards y configuración de Grafana
- Configura datasources para Prometheus
- Crea dashboards para monitoreo del sistema e integraciones
- Proporciona instrucciones para iniciar el entorno de monitoreo

Después de configurar el monitoreo, accede a los dashboards:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin_password)
- Alertmanager: http://localhost:9093

## 5. Priorizar y Corregir Problemas

Para priorizar y corregir problemas:

1. **Recopilar Feedback**:
   
   Utiliza los siguientes canales para recopilar feedback:
   - Formularios de feedback de usuario
   - Alertas del sistema de monitoreo
   - Reportes de errores
   - Métricas de rendimiento

2. **Clasificar Problemas**:
   
   Clasifica los problemas según:
   - Severidad (crítico, alto, medio, bajo)
   - Impacto (número de usuarios afectados)
   - Esfuerzo de corrección (alto, medio, bajo)

3. **Implementar Correcciones**:
   
   Para implementar correcciones rápidas:

   ```bash
   # Crear rama para la corrección
   git checkout -b hotfix/nombre-del-problema
   
   # Implementar corrección
   # Ejecutar pruebas
   
   # Fusionar con la rama principal
   git checkout main
   git merge hotfix/nombre-del-problema
   
   # Desplegar la corrección
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

## Cronograma Recomendado

| Semana | Actividad |
|--------|-----------|
| 1 | Pre-Despliegue y Despliegue |
| 2 | Post-Despliegue y Pruebas de Usuario |
| 3 | Despliegue Gradual (Fases 1 y 2) |
| 4 | Despliegue Gradual (Fases 3 y 4) |
| 5-6 | Monitoreo Intensivo |
| 7-8 | Iteración Rápida y Correcciones |

## Contactos de Soporte

En caso de problemas durante el despliegue, contacta a:

| Rol | Nombre | Contacto |
|-----|--------|----------|
| DevOps Lead | [Nombre] | [Teléfono/Email] |
| Backend Lead | [Nombre] | [Teléfono/Email] |
| Frontend Lead | [Nombre] | [Teléfono/Email] |
| QA Lead | [Nombre] | [Teléfono/Email] |
| Product Owner | [Nombre] | [Teléfono/Email] |

## Recursos Adicionales

- [Plan de Ejecución Detallado](./PLAN_EJECUCION_DESPLIEGUE.md)
- [Checklist de Despliegue](./deployment/deployment-checklist.md)
- [Plan de Pruebas de Usuario](./testing/user-testing-plan.md)
- [Formulario de Feedback](./testing/user-feedback-form.md)
- [Guía de Despliegue](./deployment/deployment-guide.md)
- [Variables de Entorno](./deployment/env-variables.md)
- [Guía de Monitoreo](./monitoring/monitoring-guide.md)
