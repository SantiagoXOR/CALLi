import { toast } from 'sonner';
import { supabaseMCPClient } from '@/lib/supabase-mcp';

export interface AuthUser {
  id: string;
  email: string;
  name?: string;
  role?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
}

export const authMCPService = {
  // Iniciar sesión con email y contraseña
  async login({ email, password }: LoginCredentials): Promise<AuthUser | null> {
    try {
      const { data, error } = await supabaseMCPClient.auth.signInWithPassword(email, password);

      if (error) {
        console.error('Error de inicio de sesión:', error.message);
        toast.error(`Error de inicio de sesión: ${error.message}`);
        return null;
      }

      if (!data || !data.user) {
        toast.error('No se pudo iniciar sesión');
        return null;
      }

      // Obtener datos adicionales del usuario desde la tabla de perfiles
      const { data: profileData, error: profileError } = await supabaseMCPClient.select(
        'profiles',
        {
          filter: { id: data.user.id },
          columns: 'name, role',
        }
      );

      if (profileError) {
        console.error('Error al obtener perfil:', profileError.message);
      }

      const profile = profileData && profileData.length > 0 ? profileData[0] : null;

      const user: AuthUser = {
        id: data.user.id,
        email: data.user.email || '',
        name: profile?.name,
        role: profile?.role,
      };

      toast.success('Inicio de sesión exitoso');
      return user;
    } catch (error) {
      console.error('Error inesperado:', error);
      toast.error('Error inesperado al iniciar sesión');
      return null;
    }
  },

  // Registrar un nuevo usuario
  async register({ email, password, name }: RegisterData): Promise<AuthUser | null> {
    try {
      const { data, error } = await supabaseMCPClient.auth.signUp(email, password);

      if (error) {
        console.error('Error de registro:', error.message);
        toast.error(`Error de registro: ${error.message}`);
        return null;
      }

      if (!data || !data.user) {
        toast.error('No se pudo completar el registro');
        return null;
      }

      // Crear perfil de usuario
      const { error: profileError } = await supabaseMCPClient.insert('profiles', {
        id: data.user.id,
        name,
        role: 'user', // Rol por defecto
        created_at: new Date().toISOString(),
      });

      if (profileError) {
        console.error('Error al crear perfil:', profileError.message);
        toast.error(`Error al crear perfil: ${profileError.message}`);
      }

      const user: AuthUser = {
        id: data.user.id,
        email: data.user.email || '',
        name,
        role: 'user',
      };

      toast.success('Registro exitoso');
      return user;
    } catch (error) {
      console.error('Error inesperado:', error);
      toast.error('Error inesperado al registrar');
      return null;
    }
  },

  // Cerrar sesión
  async logout(): Promise<boolean> {
    try {
      const { error } = await supabaseMCPClient.auth.signOut();
      
      if (error) {
        console.error('Error al cerrar sesión:', error.message);
        toast.error(`Error al cerrar sesión: ${error.message}`);
        return false;
      }
      
      toast.success('Sesión cerrada correctamente');
      return true;
    } catch (error) {
      console.error('Error inesperado:', error);
      toast.error('Error inesperado al cerrar sesión');
      return false;
    }
  },

  // Obtener usuario actual
  async getCurrentUser(): Promise<AuthUser | null> {
    try {
      const { data, error } = await supabaseMCPClient.auth.getUser();
      
      if (error || !data || !data.user) {
        return null;
      }

      // Obtener datos adicionales del usuario desde la tabla de perfiles
      const { data: profileData } = await supabaseMCPClient.select(
        'profiles',
        {
          filter: { id: data.user.id },
          columns: 'name, role',
        }
      );

      const profile = profileData && profileData.length > 0 ? profileData[0] : null;

      const user: AuthUser = {
        id: data.user.id,
        email: data.user.email || '',
        name: profile?.name,
        role: profile?.role,
      };

      return user;
    } catch (error) {
      console.error('Error al obtener usuario actual:', error);
      return null;
    }
  },

  // Verificar si el usuario está autenticado
  async isAuthenticated(): Promise<boolean> {
    const user = await this.getCurrentUser();
    return !!user;
  }
};
