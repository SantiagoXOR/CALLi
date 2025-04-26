'use client'; // Provider debe ser un Client Component

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React, { useState } from 'react';
// Opcional: Importar React Query DevTools para desarrollo
// import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

interface QueryProviderProps {
  children: React.ReactNode;
}

const QueryProvider: React.FC<QueryProviderProps> = ({ children }) => {
  // Usamos useState para asegurar que QueryClient solo se cree una vez por instancia del provider
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            // Configuraciones globales opcionales para las queries
            // staleTime: 1000 * 60 * 5, // 5 minutos
            // refetchOnWindowFocus: false, // Deshabilitar refetch al enfocar ventana
          },
        },
      })
  );

  return (
    // Proporcionar el cliente a la aplicación
    <QueryClientProvider client={queryClient}>
      {children}
      {/* Opcional: Añadir DevTools solo en desarrollo */}
      {/* <ReactQueryDevtools initialIsOpen={false} /> */}
    </QueryClientProvider>
  );
};

export default QueryProvider;
