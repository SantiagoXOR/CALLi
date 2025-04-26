"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { Loader2 } from "lucide-react";

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRoles?: string[];
}

export function ProtectedRoute({
  children,
  requiredRoles = [],
}: ProtectedRouteProps) {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hasRequiredRoles, setHasRequiredRoles] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Verificar si hay una sesión activa
        const { data, error } = await supabase.auth.getSession();

        if (error || !data.session) {
          // No hay sesión, redirigir a login
          setIsAuthenticated(false);
          router.push(`/login?redirect=${encodeURIComponent(pathname)}`);
          return;
        }

        setIsAuthenticated(true);

        // Si no se requieren roles específicos, permitir acceso
        if (requiredRoles.length === 0) {
          setHasRequiredRoles(true);
          setIsLoading(false);
          return;
        }

        // Verificar roles del usuario
        const { data: userData } = await supabase.auth.getUser();
        const userRoles = userData.user?.app_metadata?.roles || [];

        // Verificar si el usuario tiene alguno de los roles requeridos
        const hasRole = requiredRoles.some((role) => userRoles.includes(role));

        if (!hasRole) {
          // No tiene los roles requeridos, redirigir a página de acceso denegado
          router.push("/access-denied");
          return;
        }

        setHasRequiredRoles(true);
        setIsLoading(false);
      } catch (error) {
        console.error("Error checking auth:", error);
        setIsAuthenticated(false);
        router.push(`/login?redirect=${encodeURIComponent(pathname)}`);
      }
    };

    checkAuth();

    // Suscribirse a cambios de autenticación
    const { data: authListener } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        if (event === "SIGNED_OUT") {
          setIsAuthenticated(false);
          router.push(`/login?redirect=${encodeURIComponent(pathname)}`);
        } else if (event === "SIGNED_IN" && session) {
          setIsAuthenticated(true);
          checkAuth(); // Verificar roles
        }
      }
    );

    return () => {
      authListener.subscription.unsubscribe();
    };
  }, [pathname, router, requiredRoles]);

  // Mostrar loader mientras se verifica la autenticación
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2 text-lg">Verificando autenticación...</span>
      </div>
    );
  }

  // Si está autenticado y tiene los roles requeridos, mostrar el contenido
  if (isAuthenticated && hasRequiredRoles) {
    return <>{children}</>;
  }

  // Por defecto, no mostrar nada mientras se redirige
  return null;
}
