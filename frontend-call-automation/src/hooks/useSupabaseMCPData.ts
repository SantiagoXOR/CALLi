"use client";

import { useState } from "react";
import { supabaseMCPClient } from "@/lib/supabase-mcp";
import { toast } from "sonner";

/**
 * Hook personalizado para interactuar con la base de datos de Supabase a través del MCP
 * Proporciona funciones para operaciones CRUD comunes
 */
export function useSupabaseMCPData<T>(tableName: string) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  /**
   * Obtiene todos los registros de una tabla
   * @param options Opciones de consulta (ordenamiento, filtros, etc.)
   * @returns Lista de registros
   */
  const getAll = async (options?: {
    columns?: string;
    filter?: Record<string, any>;
    order?: { column: string; ascending?: boolean };
    limit?: number;
    offset?: number;
  }): Promise<T[]> => {
    setLoading(true);
    setError(null);

    try {
      const { data, error } = await supabaseMCPClient.select<T[]>(tableName, options);

      if (error) {
        throw new Error(error.message);
      }

      return data || [];
    } catch (err) {
      const error = err as Error;
      setError(error);
      toast.error(`Error al obtener datos: ${error.message}`);
      return [];
    } finally {
      setLoading(false);
    }
  };

  /**
   * Obtiene un registro por su ID
   * @param id ID del registro
   * @returns Registro encontrado o null
   */
  const getById = async (id: string): Promise<T | null> => {
    setLoading(true);
    setError(null);

    try {
      const { data, error } = await supabaseMCPClient.select<T[]>(tableName, {
        filter: { id },
        limit: 1,
      });

      if (error) {
        throw new Error(error.message);
      }

      return data && data.length > 0 ? data[0] : null;
    } catch (err) {
      const error = err as Error;
      setError(error);
      toast.error(`Error al obtener registro: ${error.message}`);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Crea un nuevo registro
   * @param record Datos del nuevo registro
   * @returns Registro creado o null
   */
  const create = async (record: Partial<T>): Promise<T | null> => {
    setLoading(true);
    setError(null);

    try {
      const { data, error } = await supabaseMCPClient.insert<T>(tableName, record);

      if (error) {
        throw new Error(error.message);
      }

      toast.success("Registro creado correctamente");
      return data;
    } catch (err) {
      const error = err as Error;
      setError(error);
      toast.error(`Error al crear registro: ${error.message}`);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Actualiza un registro existente
   * @param id ID del registro a actualizar
   * @param updates Datos a actualizar
   * @returns Registro actualizado o null
   */
  const update = async (
    id: string,
    updates: Partial<T>
  ): Promise<T | null> => {
    setLoading(true);
    setError(null);

    try {
      const { data, error } = await supabaseMCPClient.update<T>(
        tableName,
        updates,
        { id }
      );

      if (error) {
        throw new Error(error.message);
      }

      toast.success("Registro actualizado correctamente");
      return data;
    } catch (err) {
      const error = err as Error;
      setError(error);
      toast.error(`Error al actualizar registro: ${error.message}`);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Elimina un registro
   * @param id ID del registro a eliminar
   * @returns true si se eliminó correctamente, false en caso contrario
   */
  const remove = async (id: string): Promise<boolean> => {
    setLoading(true);
    setError(null);

    try {
      const { error } = await supabaseMCPClient.delete(tableName, { id });

      if (error) {
        throw new Error(error.message);
      }

      toast.success("Registro eliminado correctamente");
      return true;
    } catch (err) {
      const error = err as Error;
      setError(error);
      toast.error(`Error al eliminar registro: ${error.message}`);
      return false;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    getAll,
    getById,
    create,
    update,
    remove,
  };
}
