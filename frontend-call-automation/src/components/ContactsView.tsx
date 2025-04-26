"use client";

import { useExportContacts } from "@/services/contactService";
import { Contact } from "@/types/contact";
import { useState } from "react";
import { toast } from "sonner";
import { ContactDetail } from "./ContactDetail";
import { ContactForm } from "./ContactForm";
import { ContactImport } from "./ContactImport";
import { ContactList } from "./ContactList";

type ViewMode = "list" | "create" | "edit" | "detail" | "import";

export function ContactsView() {
  const [viewMode, setViewMode] = useState<ViewMode>("list");
  const [selectedContactId, setSelectedContactId] = useState<string | null>(
    null
  );
  const exportContacts = useExportContacts();

  const handleCreateContact = () => {
    setViewMode("create");
    setSelectedContactId(null);
  };

  const handleEditContact = (id: string) => {
    setSelectedContactId(id);
    setViewMode("edit");
  };

  const handleViewContact = (id: string) => {
    setSelectedContactId(id);
    setViewMode("detail");
  };

  const handleImportContacts = () => {
    setViewMode("import");
  };

  const handleExportContacts = async () => {
    try {
      toast.loading("Exportando contactos...");
      const blob = await exportContacts.mutateAsync();

      // Crear URL para descargar el archivo
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `contactos_${new Date().toISOString().split("T")[0]}.csv`;
      document.body.appendChild(a);
      a.click();

      // Limpiar
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast.dismiss();
      toast.success("Contactos exportados correctamente");
    } catch (error) {
      console.error("Error al exportar contactos:", error);
      toast.dismiss();
      toast.error("Error al exportar contactos");
    }
  };

  const handleCancel = () => {
    setViewMode("list");
    setSelectedContactId(null);
  };

  const handleSuccess = () => {
    setViewMode("list");
    setSelectedContactId(null);
  };

  return (
    <div className="container mx-auto py-6 space-y-6">
      {viewMode === "list" && (
        <ContactList
          onCreateContact={handleCreateContact}
          onEditContact={handleEditContact}
          onViewContact={handleViewContact}
          onImportContacts={handleImportContacts}
          onExportContacts={handleExportContacts}
        />
      )}

      {viewMode === "create" && (
        <ContactForm onCancel={handleCancel} onSuccess={handleSuccess} />
      )}

      {viewMode === "edit" && selectedContactId && (
        <ContactForm
          contact={{ id: selectedContactId } as Contact}
          onCancel={handleCancel}
          onSuccess={handleSuccess}
        />
      )}

      {viewMode === "detail" && selectedContactId && (
        <ContactDetail
          contactId={selectedContactId}
          onEdit={handleEditContact}
          onBack={handleCancel}
        />
      )}

      {viewMode === "import" && (
        <ContactImport onCancel={handleCancel} onSuccess={handleSuccess} />
      )}
    </div>
  );
}
