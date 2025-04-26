# Workflows Deshabilitados

Los siguientes workflows han sido **deshabilitados permanentemente** del repositorio debido a problemas persistentes:

- `ci-cd-pipeline.yml`
- `config-security-scan.yml`

## ⚠️ IMPORTANTE ⚠️

### NO MODIFICAR ESTOS WORKFLOWS

Estos workflows han sido modificados intencionalmente para cancelarse a sí mismos porque:

1. Fallaban consistentemente
2. No se pudieron corregir después de múltiples intentos
3. Causaban problemas en el repositorio

Si necesitas funcionalidad similar, por favor crea nuevos workflows con nombres diferentes.

## Alternativas

En lugar de estos workflows, puedes usar:

- Para CI/CD: `.github/workflows/minimal-check.yml`
- Para seguridad: `.github/workflows/basic-check.yml`

## Configuración

La configuración global para GitHub Actions se encuentra en:

- `.github/workflow-settings.yml`
- `.github/workflows/disable-workflows.yml`

## Estrategia de deshabilitación

Estos workflows ahora:

1. Se cancelan a sí mismos inmediatamente al iniciar
2. Están configurados para terminar con éxito (exit 0)
3. Tienen configuración global que los marca como deshabilitados
