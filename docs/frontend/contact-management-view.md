# Vista de Gestión de Contactos

## Descripción

La vista de gestión de contactos permite a los usuarios crear, editar, eliminar, importar y exportar contactos. Esta vista es fundamental para la gestión de campañas de llamadas, ya que los contactos son los destinatarios de las llamadas automatizadas.

## Componentes

### ContactsView

Componente principal que gestiona el estado de la vista y coordina los diferentes subcomponentes.

**Funcionalidades:**
- Cambio entre diferentes modos de vista (lista, creación, edición, detalle, importación)
- Gestión del contacto seleccionado
- Exportación de contactos a CSV

### ContactList

Muestra la lista de contactos con opciones para filtrar, buscar, editar y eliminar.

**Funcionalidades:**
- Visualización paginada de contactos
- Búsqueda de contactos
- Acciones rápidas (editar, eliminar)
- Estados de carga (skeletons) durante la carga de datos

### ContactForm

Formulario para crear o editar contactos.

**Funcionalidades:**
- Validación de campos con React Hook Form y Zod
- Gestión de etiquetas (tags)
- Manejo de errores y mensajes de éxito

### ContactDetail

Muestra los detalles completos de un contacto.

**Funcionalidades:**
- Visualización de información detallada
- Opciones para editar o eliminar
- Estados de carga durante la obtención de datos

### ContactImport

Permite importar contactos desde un archivo CSV.

**Funcionalidades:**
- Selección de archivo
- Visualización del progreso de carga
- Resumen de resultados (contactos importados y errores)

## Flujo de Trabajo

1. El usuario accede a la vista de contactos y ve la lista de contactos existentes
2. Puede buscar contactos específicos o filtrar por criterios
3. Puede crear un nuevo contacto, editar uno existente o ver detalles
4. Puede importar contactos desde un archivo CSV
5. Puede exportar la lista de contactos a un archivo CSV

## Servicios API

La vista utiliza los siguientes servicios de API:

- `useGetContacts`: Obtiene la lista paginada de contactos
- `useGetContact`: Obtiene los detalles de un contacto específico
- `useCreateContact`: Crea un nuevo contacto
- `useUpdateContact`: Actualiza un contacto existente
- `useDeleteContact`: Elimina un contacto
- `useImportContacts`: Importa contactos desde un archivo CSV
- `useExportContacts`: Exporta contactos a un archivo CSV

## Estados de Carga

Se han implementado estados de carga (skeletons) para mejorar la experiencia de usuario durante las operaciones asíncronas:

- Skeletons en la lista de contactos durante la carga inicial
- Indicadores de carga durante la creación, actualización y eliminación
- Barra de progreso durante la importación de contactos

## Mejoras Futuras

- Implementar filtros avanzados (por etiquetas, fecha de creación, etc.)
- Añadir selección múltiple para operaciones por lotes
- Mejorar la visualización de historial de llamadas por contacto
- Implementar gestión de listas de contactos
- Añadir estadísticas y métricas por contacto
