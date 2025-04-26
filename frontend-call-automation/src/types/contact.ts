/**
 * Tipos de datos para la gestión de contactos
 */

export interface Contact {
  id: string;
  name: string;
  phone_number: string;
  email?: string;
  notes?: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface ContactCreate {
  name: string;
  phone_number: string;
  email?: string;
  notes?: string;
  tags?: string[];
}

export interface ContactUpdate {
  name?: string;
  phone_number?: string;
  email?: string;
  notes?: string;
  tags?: string[];
}

export interface ContactList {
  id: string;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface ContactListCreate {
  name: string;
  description?: string;
}

export interface ContactListUpdate {
  name?: string;
  description?: string;
}

export interface ContactFilter {
  search?: string;
  tags?: string[];
  list_id?: string;
}

export interface ContactPagination {
  page: number;
  limit: number;
  total: number;
}
