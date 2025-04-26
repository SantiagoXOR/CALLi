"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabase";
import { toast } from "sonner";

/**
 * Hook personalizado para interactuar con la base de datos de Supabase
 * Proporciona funciones para operaciones CRUD comunes
 */
export function useSupabaseData<T>(tableName: string) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  /**
   * Obtiene todos los registros de una tabla
   * @param options Opciones de consulta (ordenamiento, filtros, etc.)
   * @returns Lista de registros
   */
  const getAll = async (options?: {
    orderBy?: { column: string; ascending?: boolean };
    limit?: number;
    filters?: Array<{ column: string; operator: string; value: any }>;
  }): Promise<T[]> => {
    setLoading(true);
    setError(null);

    try {
      let query = supabase.from(tableName).select("*");

      // Aplicar filtros si existen
      if (options?.filters) {
        for (const filter of options.filters) {
          query = query.filter(
            filter.column,
            filter.operator,
            filter.value
          );
        }
      }

      // Aplicar ordenamiento si existe
      if (options?.orderBy) {
        query = query.order(options.orderBy.column, {
          ascending: options.orderBy.ascending ?? true,
        });
      }

      // Aplicar límite si existe
      if (options?.limit) {
        query = query.limit(options.limit);
      }

      const { data, error } = await query;

      if (error) {
        throw error;
      }

      return data as T[];
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
      const { data, error } = await supabase
        .from(tableName)
        .select("*")
        .eq("id", id)
        .single();

      if (error) {
        throw error;
      }

      return data as T;
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
      const { data, error } = await supabase
        .from(tableName)
        .insert([record])
        .select()
        .single();

      if (error) {
        throw error;
      }

      toast.success("Registro creado correctamente");
      return data as T;
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
      const { data, error } = await supabase
        .from(tableName)
        .update(updates)
        .eq("id", id)
        .select()
        .single();

      if (error) {
        throw error;
      }

      toast.success("Registro actualizado correctamente");
      return data as T;
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
      const { error } = await supabase.from(tableName).delete().eq("id", id);

      if (error) {
        throw error;
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
