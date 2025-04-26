"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AuthUser, LoginCredentials, RegisterData, authMCPService } from "@/services/authMCPService";

interface AuthMCPContextType {
  user: AuthUser | null;
  loading: boolean;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  register: (data: RegisterData) => Promise<boolean>;
  logout: () => Promise<void>;
}

const AuthMCPContext = createContext<AuthMCPContextType | undefined>(undefined);

export function AuthMCPProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Verificar si hay un usuario autenticado al cargar la aplicación
    const checkUser = async () => {
      try {
        const currentUser = await authMCPService.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error("Error al verificar usuario:", error);
      } finally {
        setLoading(false);
      }
    };

    checkUser();
  }, []);

  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    try {
      const user = await authMCPService.login(credentials);
      if (user) {
        setUser(user);
        return true;
      }
      return false;
    } catch (error) {
      console.error("Error en login:", error);
      return false;
    }
  };

  const register = async (data: RegisterData): Promise<boolean> => {
    try {
      const user = await authMCPService.register(data);
      if (user) {
        setUser(user);
        return true;
      }
      return false;
    } catch (error) {
      console.error("Error en registro:", error);
      return false;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      const success = await authMCPService.logout();
      if (success) {
        setUser(null);
        router.push("/login");
      }
    } catch (error) {
      console.error("Error en logout:", error);
    }
  };

  return (
    <AuthMCPContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthMCPContext.Provider>
  );
}

export function useAuthMCP() {
  const context = useContext(AuthMCPContext);
  if (context === undefined) {
    throw new Error("useAuthMCP debe ser usado dentro de un AuthMCPProvider");
  }
  return context;
}
