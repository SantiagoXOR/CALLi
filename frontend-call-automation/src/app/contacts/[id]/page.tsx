"use client";

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ContactForm } from '@/components/ContactForm';
import { contactService } from '@/services/contactService';
import { Contact } from '@/types/contact';
import { useParams } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

export default function ContactDetailPage() {
  const router = useRouter();
  const params = useParams();
  const contactId = params.id as string;

  const [contact, setContact] = useState<Contact | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContact = async () => {
      try {
        setLoading(true);
        const data = await contactService.getContact(contactId);
        setContact(data);
        setError(null);
      } catch (err) {
        console.error('Error al cargar el contacto:', err);
        setError('No se pudo cargar la información del contacto. Por favor, intenta de nuevo.');
      } finally {
        setLoading(false);
      }
    };

    if (contactId) {
      fetchContact();
    }
  }, [contactId]);

  if (loading) {
    return (
      <Card className="w-full max-w-2xl mx-auto mt-8">
        <CardHeader>
          <CardTitle>Cargando contacto...</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full max-w-2xl mx-auto mt-8">
        <CardHeader>
          <CardTitle>Error</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-500">{error}</p>
          <Button
            variant="outline"
            className="mt-4"
            onClick={() => router.push('/contacts')}
          >
            <ArrowLeft className="mr-2 h-4 w-4" /> Volver a la lista de contactos
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="container mx-auto py-6">
      <Button
        variant="outline"
        className="mb-6"
        onClick={() => router.push('/contacts')}
      >
        <ArrowLeft className="mr-2 h-4 w-4" /> Volver a la lista de contactos
      </Button>

      {contact ? (
        <ContactForm
          contact={contact}
          onCancel={() => router.push('/contacts')}
          onSuccess={() => router.push('/contacts')}
        />
      ) : (
        <Card className="w-full max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Contacto no encontrado</CardTitle>
          </CardHeader>
          <CardContent>
            <p>No se pudo encontrar el contacto solicitado.</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
