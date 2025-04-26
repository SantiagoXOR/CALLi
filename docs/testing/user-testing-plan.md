# Plan de Pruebas de Usuario

## Objetivo

El objetivo de este plan es validar la usabilidad, funcionalidad y experiencia general del Sistema de Automatización de Llamadas con usuarios reales antes del lanzamiento del MVP.

## Participantes

Se recomienda incluir entre 5-8 participantes con los siguientes perfiles:

- 2-3 usuarios con experiencia en marketing/ventas
- 2-3 usuarios con experiencia en atención al cliente
- 1-2 usuarios con perfil técnico/administrativo

## Metodología

Las pruebas se realizarán en sesiones individuales de 60 minutos con la siguiente estructura:

1. **Introducción** (5 minutos)
   - Explicación del propósito de la prueba
   - Aclaración de que se está evaluando el sistema, no al usuario
   - Firma de acuerdo de confidencialidad

2. **Entrevista previa** (5 minutos)
   - Experiencia previa con sistemas similares
   - Expectativas sobre el sistema

3. **Tareas guiadas** (40 minutos)
   - Ejecución de escenarios predefinidos
   - Observación y registro de comportamiento
   - Método "pensar en voz alta"

4. **Entrevista posterior** (10 minutos)
   - Impresiones generales
   - Dificultades encontradas
   - Sugerencias de mejora

## Escenarios de Prueba

### Escenario 1: Gestión de Contactos

1. Crear un nuevo contacto manualmente
2. Editar un contacto existente
3. Importar contactos desde un archivo CSV
4. Buscar contactos por nombre o etiqueta
5. Eliminar un contacto

### Escenario 2: Gestión de Campañas

1. Crear una nueva campaña
2. Seleccionar contactos para la campaña
3. Configurar el script de la campaña
4. Programar la campaña
5. Editar una campaña existente

### Escenario 3: Monitoreo de Llamadas

1. Ver el listado de llamadas
2. Filtrar llamadas por estado
3. Ver detalles de una llamada específica
4. Escuchar la grabación de una llamada
5. Exportar resultados de llamadas

### Escenario 4: Reportes y Análisis

1. Ver el dashboard de métricas
2. Filtrar reportes por fecha
3. Exportar un reporte en formato CSV
4. Analizar resultados de una campaña específica

## Métricas a Evaluar

### Métricas Cuantitativas

1. **Eficiencia**
   - Tiempo para completar cada tarea
   - Número de clics para completar cada tarea
   - Tasa de éxito en la finalización de tareas

2. **Errores**
   - Número de errores por tarea
   - Tipos de errores cometidos
   - Capacidad de recuperación tras un error

### Métricas Cualitativas

1. **Satisfacción**
   - Facilidad de uso percibida (escala 1-5)
   - Utilidad percibida (escala 1-5)
   - Intención de uso futuro (escala 1-5)

2. **Comentarios Abiertos**
   - Aspectos positivos destacados
   - Puntos de fricción identificados
   - Sugerencias de mejora

## Formulario de Feedback

Se utilizará el siguiente formulario para recopilar feedback estructurado:

### Formulario Post-Prueba

**Evaluación General**

| Aspecto | 1 (Muy malo) | 2 (Malo) | 3 (Regular) | 4 (Bueno) | 5 (Muy bueno) |
|---------|--------------|----------|-------------|-----------|---------------|
| Facilidad de uso | | | | | |
| Diseño visual | | | | | |
| Velocidad/rendimiento | | | | | |
| Claridad de la información | | | | | |
| Utilidad general | | | | | |

**Preguntas Abiertas**

1. ¿Qué aspectos del sistema le resultaron más fáciles de usar?
2. ¿Qué aspectos del sistema le resultaron más difíciles o confusos?
3. ¿Encontró alguna funcionalidad que esperaba y no estaba disponible?
4. ¿Qué cambiaría o mejoraría del sistema?
5. ¿Utilizaría este sistema en su trabajo diario? ¿Por qué?

## Preparación del Entorno

Para las pruebas de usuario se utilizará:

1. **Entorno de Staging**
   - Precargar datos de ejemplo (contactos, campañas, llamadas)
   - Configurar integraciones en modo sandbox

2. **Herramientas de Registro**
   - Software de grabación de pantalla
   - Notas de observación
   - Cronómetro para medición de tiempos

3. **Documentación**
   - Guía de tareas para el moderador
   - Formularios de consentimiento
   - Cuestionarios pre y post prueba

## Cronograma

| Actividad | Duración | Fechas |
|-----------|----------|--------|
| Preparación de materiales | 1 semana | DD/MM/YYYY - DD/MM/YYYY |
| Reclutamiento de participantes | 1 semana | DD/MM/YYYY - DD/MM/YYYY |
| Sesiones de prueba | 2 días | DD/MM/YYYY - DD/MM/YYYY |
| Análisis de resultados | 2 días | DD/MM/YYYY - DD/MM/YYYY |
| Presentación de hallazgos | 1 día | DD/MM/YYYY |

## Análisis y Reporte

Después de completar todas las sesiones, se realizará:

1. **Compilación de Datos**
   - Consolidación de métricas cuantitativas
   - Transcripción de comentarios cualitativos
   - Identificación de patrones comunes

2. **Priorización de Hallazgos**
   - Clasificación por severidad (crítico, alto, medio, bajo)
   - Clasificación por esfuerzo de implementación
   - Matriz de impacto vs. esfuerzo

3. **Reporte Final**
   - Resumen ejecutivo
   - Hallazgos detallados por escenario
   - Recomendaciones específicas
   - Plan de acción propuesto

## Criterios de Éxito

El MVP se considerará listo para lanzamiento si:

1. Los usuarios completan al menos el 90% de las tareas sin asistencia
2. La puntuación promedio de satisfacción es ≥ 4 en una escala de 5
3. No se identifican problemas críticos de usabilidad
4. Los tiempos de ejecución de tareas están dentro de los rangos esperados

## Responsables

- **Coordinador de Pruebas**: [Nombre] - Responsable de la planificación y ejecución general
- **Moderador**: [Nombre] - Guía las sesiones con los usuarios
- **Observador**: [Nombre] - Toma notas y registra comportamientos
- **Analista**: [Nombre] - Procesa los datos y genera el reporte final

## Anexos

- Plantilla de consentimiento informado
- Guión detallado para el moderador
- Cuestionarios completos
- Datos de ejemplo para las pruebas
