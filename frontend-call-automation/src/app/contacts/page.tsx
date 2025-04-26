"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ContactList } from '@/components/ContactList';
import { ContactForm } from '@/components/ContactForm';
import { ContactImport } from '@/components/ContactImport';

export default function ContactsPage() {
  const router = useRouter();
  const [showContactForm, setShowContactForm] = useState(false);
  const [showImportContacts, setShowImportContacts] = useState(false);
  const [selectedContactId, setSelectedContactId] = useState<string | null>(null);

  const handleCreateContact = () => {
    router.push('/contacts/new');
  };

  const handleEditContact = (id: string) => {
    router.push(`/contacts/${id}`);
  };

  const handleImportContacts = () => {
    setShowImportContacts(true);
  };

  const handleExportContacts = () => {
    // En una implementación real, esto llamaría al servicio para exportar contactos
    console.log("Exportando contactos...");
    alert("La exportación de contactos se ha iniciado. El archivo se descargará automáticamente.");
  };

  // Si estamos mostrando el formulario de importación de contactos
  if (showImportContacts) {
    return (
      <ContactImport
        onCancel={() => setShowImportContacts(false)}
        onSuccess={() => setShowImportContacts(false)}
      />
    );
  }

  // Vista principal de lista de contactos
  return (
    <ContactList
      onCreateContact={handleCreateContact}
      onEditContact={handleEditContact}
      onImportContacts={handleImportContacts}
      onExportContacts={handleExportContacts}
    />
  );
}
