/**
 * Tipos para la base de datos de Supabase
 * Estos tipos representan la estructura de la base de datos en Supabase
 */
export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[];

export interface Database {
  public: {
    Tables: {
      campaigns: {
        Row: {
          id: string;
          name: string;
          description: string | null;
          status: 'draft' | 'scheduled' | 'active' | 'paused' | 'completed' | 'cancelled';
          schedule_start: string | null;
          schedule_end: string | null;
          script_template: string | null;
          max_retries: number;
          retry_delay_minutes: number;
          total_calls: number;
          successful_calls: number;
          failed_calls: number;
          pending_calls: number;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          name: string;
          description?: string | null;
          status?: 'draft' | 'scheduled' | 'active' | 'paused' | 'completed' | 'cancelled';
          schedule_start?: string | null;
          schedule_end?: string | null;
          script_template?: string | null;
          max_retries?: number;
          retry_delay_minutes?: number;
          total_calls?: number;
          successful_calls?: number;
          failed_calls?: number;
          pending_calls?: number;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          name?: string;
          description?: string | null;
          status?: 'draft' | 'scheduled' | 'active' | 'paused' | 'completed' | 'cancelled';
          schedule_start?: string | null;
          schedule_end?: string | null;
          script_template?: string | null;
          max_retries?: number;
          retry_delay_minutes?: number;
          total_calls?: number;
          successful_calls?: number;
          failed_calls?: number;
          pending_calls?: number;
          created_at?: string;
          updated_at?: string;
        };
      };
      contacts: {
        Row: {
          id: string;
          phone_number: string;
          name: string | null;
          email: string | null;
          additional_data: Json | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          phone_number: string;
          name?: string | null;
          email?: string | null;
          additional_data?: Json | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          phone_number?: string;
          name?: string | null;
          email?: string | null;
          additional_data?: Json | null;
          created_at?: string;
          updated_at?: string;
        };
      };
      calls: {
        Row: {
          id: string;
          campaign_id: string;
          contact_id: string;
          status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
          duration_seconds: number | null;
          attempt_count: number;
          last_attempt_at: string | null;
          next_attempt_at: string | null;
          notes: string | null;
          recording_url: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          campaign_id: string;
          contact_id: string;
          status?: 'pending' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
          duration_seconds?: number | null;
          attempt_count?: number;
          last_attempt_at?: string | null;
          next_attempt_at?: string | null;
          notes?: string | null;
          recording_url?: string | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          campaign_id?: string;
          contact_id?: string;
          status?: 'pending' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
          duration_seconds?: number | null;
          attempt_count?: number;
          last_attempt_at?: string | null;
          next_attempt_at?: string | null;
          notes?: string | null;
          recording_url?: string | null;
          created_at?: string;
          updated_at?: string;
        };
      };
      profiles: {
        Row: {
          id: string;
          name: string | null;
          role: string | null;
          created_at: string | null;
          updated_at: string | null;
        };
        Insert: {
          id: string;
          name?: string | null;
          role?: string | null;
          created_at?: string | null;
          updated_at?: string | null;
        };
        Update: {
          id?: string;
          name?: string | null;
          role?: string | null;
          created_at?: string | null;
          updated_at?: string | null;
        };
      };
    };
    Views: {
      [_ in never]: never;
    };
    Functions: {
      [_ in never]: never;
    };
    Enums: {
      [_ in never]: never;
    };
  };
}
