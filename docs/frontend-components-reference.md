# Referencia de Componentes Frontend

Este documento proporciona una referencia detallada de los componentes principales utilizados en el frontend del Sistema de Automatización de Llamadas.

## Índice

1. [Componentes de Página](#1-componentes-de-página)
2. [Componentes de Layout](#2-componentes-de-layout)
3. [Componentes de Campaña](#3-componentes-de-campaña)
4. [Componentes UI](#4-componentes-ui)
5. [Componentes de Formulario](#5-componentes-de-formulario)
6. [Componentes de Visualización](#6-componentes-de-visualización)

## 1. Componentes de Página

Los componentes de página son los puntos de entrada principales para cada ruta en la aplicación.

### 1.1 Dashboard (`app/page.tsx`)

**Descripción**: Página principal que muestra un resumen de las campañas, métricas y actividad reciente.

**Props**: Ninguna (componente de página)

**Estado**:
- Métricas de campañas
- Campañas recientes
- Actividad del sistema

**Dependencias**:
- `DashboardView`
- `PanelSistemaLlamadas`

**Ejemplo de uso**:
```tsx
// Este componente se renderiza automáticamente en la ruta raíz (/)
export default function HomePage() {
  return <PanelSistemaLlamadas vistaInicial="dashboard" />;
}
```

### 1.2 Lista de Campañas (`app/campaigns/page.tsx`)

**Descripción**: Página que muestra la lista de todas las campañas con opciones de filtrado y ordenamiento.

**Props**: Ninguna (componente de página)

**Estado**:
- Lista de campañas
- Filtros aplicados
- Estado de carga

**Dependencias**:
- `CampaignListView`
- `PanelSistemaLlamadas`

### 1.3 Detalle de Campaña (`app/campaigns/[id]/page.tsx`)

**Descripción**: Página que muestra los detalles de una campaña específica.

**Props**:
- `params`: Parámetros de ruta (incluye el ID de la campaña)

**Estado**:
- Detalles de la campaña
- Estado de carga

**Dependencias**:
- `CampaignDetailView`
- `PanelSistemaLlamadas`

### 1.4 Crear Campaña (`app/campaigns/create/page.tsx`)

**Descripción**: Página para crear una nueva campaña.

**Props**: Ninguna (componente de página)

**Estado**:
- Formulario de campaña
- Estado de envío

**Dependencias**:
- `CampaignCreateView`
- `PanelSistemaLlamadas`

### 1.5 Editar Campaña (`app/campaigns/[id]/edit/page.tsx`)

**Descripción**: Página para editar una campaña existente.

**Props**:
- `params`: Parámetros de ruta (incluye el ID de la campaña)

**Estado**:
- Formulario de campaña con datos precargados
- Estado de envío

**Dependencias**:
- `CampaignEditView`
- `PanelSistemaLlamadas`

## 2. Componentes de Layout

### 2.1 Layout Principal (`Layout.tsx`)

**Descripción**: Componente que define la estructura general de la aplicación, incluyendo la barra de navegación y el contenido principal.

**Props**:
- `vistaActual`: Vista actual seleccionada
- `navegarA`: Función para navegar entre vistas
- `children`: Contenido a renderizar dentro del layout

**Ejemplo de uso**:
```tsx
<Layout vistaActual="dashboard" navegarA={handleNavigation}>
  <DashboardContent />
</Layout>
```

**Estructura**:
- Header con logo y título
- Barra de navegación con pestañas
- Área de contenido principal
- Footer (opcional)

## 3. Componentes de Campaña

### 3.1 CampaignList (`CampaignList.tsx`)

**Descripción**: Componente contenedor que maneja la lógica para obtener y mostrar la lista de campañas.

**Props**: Ninguna

**Estado**:
- `campaigns`: Lista de campañas
- `isLoading`: Estado de carga
- `error`: Error (si existe)

**Métodos**:
- `handleDelete`: Maneja la eliminación de una campaña
- `handleFilter`: Aplica filtros a la lista de campañas

**Dependencias**:
- `CampaignListView`
- `campaignService`

### 3.2 CampaignListView (`CampaignListView.tsx`)

**Descripción**: Componente de presentación que muestra la lista de campañas.

**Props**:
- `campaigns`: Lista de campañas a mostrar
- `isLoading`: Indica si los datos están cargando
- `onDelete`: Función para manejar la eliminación
- `onFilter`: Función para aplicar filtros

**Ejemplo de uso**:
```tsx
<CampaignListView
  campaigns={campaigns}
  isLoading={isLoading}
  onDelete={handleDelete}
  onFilter={handleFilter}
/>
```

### 3.3 CampaignDetail (`CampaignDetail.tsx`)

**Descripción**: Componente contenedor que maneja la lógica para obtener y mostrar los detalles de una campaña.

**Props**:
- `id`: ID de la campaña

**Estado**:
- `campaign`: Detalles de la campaña
- `isLoading`: Estado de carga
- `error`: Error (si existe)

**Dependencias**:
- `CampaignDetailView`
- `campaignService`

### 3.4 CampaignDetailView (`CampaignDetailView.tsx`)

**Descripción**: Componente de presentación que muestra los detalles de una campaña.

**Props**:
- `campaign`: Datos de la campaña
- `isLoading`: Indica si los datos están cargando
- `onEdit`: Función para navegar a la edición
- `onDelete`: Función para eliminar la campaña

### 3.5 CampaignForm (`CampaignForm.tsx`)

**Descripción**: Formulario reutilizable para crear y editar campañas.

**Props**:
- `initialData`: Datos iniciales para edición (opcional)
- `onSubmit`: Función a llamar al enviar el formulario
- `isSubmitting`: Indica si el formulario está siendo enviado

**Estado**:
- Estado del formulario gestionado por React Hook Form

**Validación**:
- Nombre requerido
- Descripción opcional
- Fecha de inicio válida
- Fecha de fin posterior a la fecha de inicio

**Ejemplo de uso**:
```tsx
<CampaignForm
  initialData={campaignData}
  onSubmit={handleSubmit}
  isSubmitting={isSubmitting}
/>
```

## 4. Componentes UI

Estos componentes son adaptaciones de Shadcn UI y se encuentran en `src/components/ui/`.

### 4.1 Button (`button.tsx`)

**Descripción**: Componente de botón con diferentes variantes y estados.

**Props**:
- `variant`: Variante visual ('default', 'destructive', 'outline', 'secondary', 'ghost', 'link')
- `size`: Tamaño ('default', 'sm', 'lg', 'icon')
- `asChild`: Renderizar como hijo (para composición)
- Todas las props de HTMLButtonElement

**Ejemplo de uso**:
```tsx
<Button variant="destructive" onClick={handleDelete}>
  Eliminar
</Button>
```

### 4.2 Card (`card.tsx`)

**Descripción**: Componente de tarjeta para agrupar contenido relacionado.

**Componentes**:
- `Card`: Contenedor principal
- `CardHeader`: Encabezado de la tarjeta
- `CardTitle`: Título de la tarjeta
- `CardDescription`: Descripción de la tarjeta
- `CardContent`: Contenido principal
- `CardFooter`: Pie de la tarjeta

**Ejemplo de uso**:
```tsx
<Card>
  <CardHeader>
    <CardTitle>Campaña de Verano</CardTitle>
    <CardDescription>Promoción especial de verano</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Detalles de la campaña...</p>
  </CardContent>
  <CardFooter>
    <Button>Editar</Button>
  </CardFooter>
</Card>
```

### 4.3 Dialog (`dialog.tsx`)

**Descripción**: Componente de diálogo modal para mostrar contenido que requiere atención.

**Componentes**:
- `Dialog`: Contenedor principal
- `DialogTrigger`: Elemento que abre el diálogo
- `DialogContent`: Contenido del diálogo
- `DialogHeader`: Encabezado del diálogo
- `DialogTitle`: Título del diálogo
- `DialogDescription`: Descripción del diálogo
- `DialogFooter`: Pie del diálogo
- `DialogClose`: Botón para cerrar el diálogo

**Ejemplo de uso**:
```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Abrir Diálogo</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Confirmar Acción</DialogTitle>
      <DialogDescription>
        ¿Estás seguro de que deseas realizar esta acción?
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline" onClick={onCancel}>Cancelar</Button>
      <Button onClick={onConfirm}>Confirmar</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### 4.4 Form (`form.tsx`)

**Descripción**: Componentes para construir formularios con React Hook Form.

**Componentes**:
- `Form`: Contenedor del formulario
- `FormField`: Campo de formulario
- `FormItem`: Elemento de formulario
- `FormLabel`: Etiqueta del campo
- `FormControl`: Control del campo
- `FormDescription`: Descripción del campo
- `FormMessage`: Mensaje de error/validación

**Ejemplo de uso**:
```tsx
<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField
      control={form.control}
      name="name"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Nombre</FormLabel>
          <FormControl>
            <Input placeholder="Nombre de la campaña" {...field} />
          </FormControl>
          <FormDescription>
            Ingresa un nombre descriptivo para la campaña.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
    <Button type="submit">Guardar</Button>
  </form>
</Form>
```

## 5. Componentes de Formulario

### 5.1 Input (`input.tsx`)

**Descripción**: Campo de entrada de texto.

**Props**:
- Todas las props de HTMLInputElement

**Ejemplo de uso**:
```tsx
<Input
  type="text"
  placeholder="Nombre de la campaña"
  value={name}
  onChange={handleChange}
/>
```

### 5.2 Select (`select.tsx`)

**Descripción**: Componente de selección desplegable.

**Componentes**:
- `Select`: Contenedor principal
- `SelectTrigger`: Elemento que abre el menú
- `SelectValue`: Valor seleccionado
- `SelectContent`: Contenido del menú
- `SelectItem`: Elemento seleccionable
- `SelectGroup`: Grupo de elementos
- `SelectLabel`: Etiqueta para un grupo

**Ejemplo de uso**:
```tsx
<Select onValueChange={handleStatusChange} defaultValue="active">
  <SelectTrigger>
    <SelectValue placeholder="Seleccionar estado" />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="active">Activa</SelectItem>
    <SelectItem value="draft">Borrador</SelectItem>
    <SelectItem value="completed">Completada</SelectItem>
    <SelectItem value="paused">Pausada</SelectItem>
  </SelectContent>
</Select>
```

### 5.3 Textarea (`textarea.tsx`)

**Descripción**: Campo de texto multilínea.

**Props**:
- Todas las props de HTMLTextAreaElement

**Ejemplo de uso**:
```tsx
<Textarea
  placeholder="Descripción de la campaña"
  value={description}
  onChange={handleChange}
  rows={4}
/>
```

## 6. Componentes de Visualización

### 6.1 Table (`table.tsx`)

**Descripción**: Componente de tabla para mostrar datos estructurados.

**Componentes**:
- `Table`: Contenedor principal
- `TableHeader`: Encabezado de la tabla
- `TableBody`: Cuerpo de la tabla
- `TableFooter`: Pie de la tabla
- `TableRow`: Fila de la tabla
- `TableHead`: Celda de encabezado
- `TableCell`: Celda de datos
- `TableCaption`: Leyenda de la tabla

**Ejemplo de uso**:
```tsx
<Table>
  <TableCaption>Lista de campañas activas</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Nombre</TableHead>
      <TableHead>Estado</TableHead>
      <TableHead>Fecha de inicio</TableHead>
      <TableHead>Acciones</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {campaigns.map((campaign) => (
      <TableRow key={campaign.id}>
        <TableCell>{campaign.name}</TableCell>
        <TableCell>{campaign.status}</TableCell>
        <TableCell>{formatDate(campaign.startDate)}</TableCell>
        <TableCell>
          <Button variant="outline" size="sm" onClick={() => onEdit(campaign.id)}>
            Editar
          </Button>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>
```

### 6.2 Tabs (`tabs.tsx`)

**Descripción**: Componente de pestañas para organizar contenido en secciones.

**Componentes**:
- `Tabs`: Contenedor principal
- `TabsList`: Lista de pestañas
- `TabsTrigger`: Pestaña seleccionable
- `TabsContent`: Contenido de la pestaña

**Ejemplo de uso**:
```tsx
<Tabs defaultValue="general" className="w-full">
  <TabsList>
    <TabsTrigger value="general">General</TabsTrigger>
    <TabsTrigger value="contacts">Contactos</TabsTrigger>
    <TabsTrigger value="calls">Llamadas</TabsTrigger>
  </TabsList>
  <TabsContent value="general">
    <CampaignGeneralInfo campaign={campaign} />
  </TabsContent>
  <TabsContent value="contacts">
    <CampaignContacts campaignId={campaign.id} />
  </TabsContent>
  <TabsContent value="calls">
    <CampaignCalls campaignId={campaign.id} />
  </TabsContent>
</Tabs>
```

### 6.3 Progress (`progress.tsx`)

**Descripción**: Barra de progreso para mostrar el avance de una tarea.

**Props**:
- `value`: Valor actual (0-100)
- Todas las props de HTMLProgressElement

**Ejemplo de uso**:
```tsx
<Progress value={75} className="w-full" />
```

### 6.4 Badge (`badge.tsx`)

**Descripción**: Etiqueta para mostrar estados o categorías.

**Props**:
- `variant`: Variante visual ('default', 'secondary', 'destructive', 'outline')

**Ejemplo de uso**:
```tsx
<Badge variant="secondary">Borrador</Badge>
```

### 6.5 Skeleton (`skeleton.tsx`)

**Descripción**: Componente de carga para mostrar mientras se cargan los datos.

**Props**:
- `className`: Clases CSS para personalizar el tamaño y forma

**Ejemplo de uso**:
```tsx
<Skeleton className="h-12 w-full rounded-md" />
```
