import {
  useMutation,
  useQuery,
  useQueryClient,
  UseQueryResult,
} from "@tanstack/react-query";
import axios from "axios";
import {
  Contact,
  ContactCreate,
  ContactFilter,
  ContactList,
  ContactListCreate,
  ContactUpdate,
} from "../types/contact";

// API URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Endpoints
const ENDPOINTS = {
  CONTACTS: "/api/contacts",
  CONTACT_BY_ID: (id: string) => `/api/contacts/${id}`,
  CONTACT_SEARCH: "/api/contacts/search",
  CONTACT_LISTS: "/api/contact-lists",
  CONTACT_LIST_BY_ID: (id: string) => `/api/contact-lists/${id}`,
  CONTACT_LIST_CONTACTS: (id: string) => `/api/contact-lists/${id}/contacts`,
  CONTACT_IMPORT: "/api/contacts/import",
  CONTACT_EXPORT: "/api/contacts/export",
};

export const contactService = {
  // Contactos
  async getContacts(
    page = 1,
    limit = 10,
    filters?: ContactFilter
  ): Promise<{ data: Contact[]; total: number }> {
    const skip = (page - 1) * limit;
    const params = { skip, limit, ...filters };

    const response = await axios.get(`${API_URL}/api/contacts`, { params });
    return response.data;
  },

  async getContact(id: string): Promise<Contact> {
    const response = await axios.get(`${API_URL}/api/contacts/${id}`);
    return response.data;
  },

  async createContact(contact: ContactCreate): Promise<Contact> {
    const response = await axios.post(`${API_URL}/api/contacts`, contact);
    return response.data;
  },

  async updateContact(id: string, contact: ContactUpdate): Promise<Contact> {
    const response = await axios.put(`${API_URL}/api/contacts/${id}`, contact);
    return response.data;
  },

  async deleteContact(id: string): Promise<{ success: boolean }> {
    const response = await axios.delete(`${API_URL}/api/contacts/${id}`);
    return response.data;
  },

  async searchContacts(query: string, limit = 10): Promise<Contact[]> {
    const response = await axios.get(`${API_URL}/api/contacts/search`, {
      params: { q: query, limit },
    });
    return response.data;
  },

  // Listas de contactos
  async getContactLists(): Promise<ContactList[]> {
    const response = await axios.get(`${API_URL}/api/contact-lists`);
    return response.data;
  },

  async createContactList(list: ContactListCreate): Promise<ContactList> {
    const response = await axios.post(`${API_URL}/api/contact-lists`, list);
    return response.data;
  },

  async addContactsToList(
    listId: string,
    contactIds: string[]
  ): Promise<{ success: boolean }> {
    const response = await axios.post(
      `${API_URL}/api/contact-lists/${listId}/contacts`,
      { contact_ids: contactIds }
    );
    return response.data;
  },

  // Importación y exportación
  async importContacts(
    file: File
  ): Promise<{ imported: number; errors: number }> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await axios.post(
      `${API_URL}/api/contacts/import`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data;
  },

  async exportContacts(listId?: string): Promise<Blob> {
    const params = listId ? { list_id: listId } : {};
    const response = await axios.get(`${API_URL}/api/contacts/export`, {
      params,
      responseType: "blob",
    });
    return response.data;
  },
};

// React Query hooks

export const useGetContacts = (
  page = 1,
  limit = 10,
  filters?: ContactFilter
): UseQueryResult<{ data: Contact[]; total: number }> => {
  return useQuery({
    queryKey: ["contacts", page, limit, filters],
    queryFn: () => contactService.getContacts(page, limit, filters),
  });
};

export const useGetContact = (id: string): UseQueryResult<Contact> => {
  return useQuery({
    queryKey: ["contact", id],
    queryFn: () => contactService.getContact(id),
    enabled: !!id,
  });
};

export const useCreateContact = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (contact: ContactCreate) =>
      contactService.createContact(contact),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contacts"] });
    },
  });
};

export const useUpdateContact = (id: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (contact: ContactUpdate) =>
      contactService.updateContact(id, contact),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contacts"] });
      queryClient.invalidateQueries({ queryKey: ["contact", id] });
    },
  });
};

export const useDeleteContact = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => contactService.deleteContact(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contacts"] });
    },
  });
};

export const useGetContactLists = (): UseQueryResult<ContactList[]> => {
  return useQuery({
    queryKey: ["contactLists"],
    queryFn: () => contactService.getContactLists(),
  });
};

export const useCreateContactList = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (list: ContactListCreate) =>
      contactService.createContactList(list),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contactLists"] });
    },
  });
};

export const useAddContactsToList = (listId: string) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (contactIds: string[]) =>
      contactService.addContactsToList(listId, contactIds),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contactLists"] });
    },
  });
};

export const useImportContacts = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (file: File) => contactService.importContacts(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["contacts"] });
    },
  });
};

export const useExportContacts = () => {
  return useMutation({
    mutationFn: (listId?: string) => contactService.exportContacts(listId),
  });
};
