# Estados de Carga (Skeletons)

## Descripción

Los estados de carga (skeletons) son componentes visuales que se muestran mientras se cargan datos asíncronos. Estos componentes mejoran la experiencia de usuario al proporcionar una representación visual de la estructura de la página antes de que los datos estén disponibles, reduciendo la percepción de tiempo de carga y evitando cambios bruscos en el layout.

## Implementación

En el Sistema de Automatización de Llamadas, hemos implementado estados de carga en los siguientes componentes:

### 1. ContactList

El componente `ContactList` muestra un skeleton loader mientras se cargan los contactos. Este loader consiste en filas de tabla con formas que representan los datos que se están cargando.

```tsx
{isLoading ? (
  // Skeleton loader para la tabla
  Array.from({ length: 5 }).map((_, index) => (
    <TableRow key={`skeleton-${index}`}>
      <TableCell>
        <Skeleton className="h-6 w-[150px]" />
      </TableCell>
      <TableCell>
        <Skeleton className="h-6 w-[120px]" />
      </TableCell>
      <TableCell>
        <Skeleton className="h-6 w-[180px]" />
      </TableCell>
      <TableCell>
        <div className="flex gap-1">
          <Skeleton className="h-6 w-[60px]" />
          <Skeleton className="h-6 w-[70px]" />
        </div>
      </TableCell>
      <TableCell className="text-right">
        <div className="flex justify-end space-x-2">
          <Skeleton className="h-8 w-8 rounded-full" />
          <Skeleton className="h-8 w-8 rounded-full" />
        </div>
      </TableCell>
    </TableRow>
  ))
) : (
  // Contenido real
)}
```

### 2. CampaignList

El componente `CampaignList` muestra un skeleton loader mientras se cargan las campañas. Este loader consiste en filas de tabla con formas que representan los datos de las campañas.

```tsx
function CampaignListSkeleton() {
  return (
    <div className="w-full">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Nombre</TableHead>
            <TableHead>Estado</TableHead>
            <TableHead>Fecha Inicio</TableHead>
            <TableHead>Fecha Fin</TableHead>
            <TableHead>Progreso</TableHead>
            <TableHead className="text-right">Acciones</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {Array.from({ length: 5 }).map((_, index) => (
            <TableRow key={`skeleton-${index}`}>
              <TableCell>
                <Skeleton className="h-6 w-[180px]" />
              </TableCell>
              <TableCell>
                <Skeleton className="h-6 w-[100px]" />
              </TableCell>
              <TableCell>
                <Skeleton className="h-6 w-[120px]" />
              </TableCell>
              <TableCell>
                <Skeleton className="h-6 w-[120px]" />
              </TableCell>
              <TableCell>
                <Skeleton className="h-6 w-[80px]" />
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end space-x-2">
                  <Skeleton className="h-8 w-8 rounded-full" />
                  <Skeleton className="h-8 w-8 rounded-full" />
                  <Skeleton className="h-8 w-8 rounded-full" />
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

### 3. CampaignDetail

El componente `CampaignDetail` muestra un skeleton loader mientras se cargan los detalles de una campaña. Este loader consiste en formas que representan los diferentes elementos de la vista de detalle.

```tsx
function CampaignDetailSkeleton() {
  return (
    <div className="space-y-6">
      {/* Encabezado de la campaña - skeleton */}
      <div className="flex justify-between items-center">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="space-x-2 flex">
          <Skeleton className="h-10 w-24" />
          <Skeleton className="h-10 w-24" />
        </div>
      </div>

      {/* Estado y progreso - skeleton */}
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-48" />
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <Skeleton className="h-6 w-24" />
            <Skeleton className="h-10 w-24" />
          </div>
          <Skeleton className="h-4 w-full mb-2" />
          <Skeleton className="h-4 w-24" />
        </CardContent>
      </Card>

      {/* Estadísticas - skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Repetido para cada tarjeta de estadísticas */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <Skeleton className="h-8 w-8 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-6 w-16" />
              </div>
            </div>
          </CardContent>
        </Card>
        {/* ... */}
      </div>
    </div>
  );
}
```

## Componente Base: Skeleton

Todos los estados de carga utilizan el componente base `Skeleton` de la biblioteca de componentes UI. Este componente proporciona una animación de pulso y un estilo consistente para todos los estados de carga.

```tsx
import { cn } from "@/lib/utils";

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  );
}

export { Skeleton };
```

## Uso

Para utilizar los estados de carga en un componente:

1. Importar el componente `Skeleton`:
   ```tsx
   import { Skeleton } from "@/components/ui/skeleton";
   ```

2. Crear un componente de skeleton que refleje la estructura del contenido real:
   ```tsx
   function MyComponentSkeleton() {
     return (
       <div>
         <Skeleton className="h-8 w-64 mb-4" />
         <Skeleton className="h-4 w-full mb-2" />
         <Skeleton className="h-4 w-3/4" />
       </div>
     );
   }
   ```

3. Utilizar el skeleton durante la carga:
   ```tsx
   function MyComponent() {
     const { data, isLoading } = useMyData();

     if (isLoading) return <MyComponentSkeleton />;

     return (
       <div>
         <h1>{data.title}</h1>
         <p>{data.description}</p>
       </div>
     );
   }
   ```

## Mejores Prácticas

1. **Reflejar la estructura real**: Los skeletons deben reflejar la estructura del contenido real para evitar cambios bruscos en el layout.

2. **Usar dimensiones aproximadas**: Las dimensiones de los skeletons deben ser aproximadas a las del contenido real.

3. **Mantener la consistencia**: Utilizar el mismo estilo de skeleton en toda la aplicación para mantener la consistencia visual.

4. **Evitar skeletons complejos**: Los skeletons deben ser simples y ligeros para no afectar el rendimiento.

5. **Considerar estados vacíos**: Después de mostrar el skeleton, asegurarse de manejar correctamente los estados vacíos o de error.

## Próximos Pasos

1. Implementar skeletons en componentes adicionales como:
   - Reportes
   - Dashboard principal
   - Vistas de configuración

2. Mejorar la accesibilidad de los skeletons añadiendo atributos ARIA apropiados.

3. Considerar la implementación de skeletons progresivos que muestren más detalles a medida que se cargan los datos.
