"use client";

import { useGetContact, useDeleteContact } from "@/services/contactService";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Edit, Trash2, Phone, Mail, Tag, ArrowLeft, Calendar } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { es } from "date-fns/locale";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { useState } from "react";
import { toast } from "sonner";

interface ContactDetailProps {
  contactId: string;
  onEdit: (id: string) => void;
  onBack: () => void;
}

export function ContactDetail({ contactId, onEdit, onBack }: ContactDetailProps) {
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const { data: contact, isLoading, error } = useGetContact(contactId);
  const deleteMutation = useDeleteContact();

  const handleDelete = async () => {
    try {
      await deleteMutation.mutateAsync(contactId);
      toast.success("Contacto eliminado exitosamente");
      onBack();
    } catch (error) {
      console.error("Error al eliminar contacto:", error);
      toast.error("Error al eliminar el contacto");
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2">Cargando detalles del contacto...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error:</strong>
        <span className="block sm:inline"> Error al cargar los detalles del contacto</span>
      </div>
    );
  }

  if (!contact) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No se encontró el contacto</p>
        <Button onClick={onBack} variant="outline" className="mt-4">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a la lista
        </Button>
      </div>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Detalles del Contacto</CardTitle>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" onClick={() => onEdit(contactId)}>
            <Edit className="h-4 w-4 mr-2" />
            Editar
          </Button>
          <AlertDialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
            <AlertDialogTrigger asChild>
              <Button variant="outline" size="sm" className="text-red-500 border-red-200 hover:bg-red-50">
                <Trash2 className="h-4 w-4 mr-2" />
                Eliminar
              </Button>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle>¿Estás seguro?</AlertDialogTitle>
                <AlertDialogDescription>
                  Esta acción eliminará permanentemente el contacto {contact.name} y no se puede deshacer.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel>Cancelar</AlertDialogCancel>
                <AlertDialogAction
                  onClick={handleDelete}
                  className="bg-red-500 hover:bg-red-600"
                  disabled={deleteMutation.isPending}
                >
                  {deleteMutation.isPending ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Eliminando...
                    </>
                  ) : (
                    "Eliminar"
                  )}
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <h3 className="text-2xl font-semibold">{contact.name}</h3>
          <div className="flex items-center mt-2 text-gray-500">
            <Calendar className="h-4 w-4 mr-2" />
            <span className="text-sm">
              Creado {formatDistanceToNow(new Date(contact.created_at), { addSuffix: true, locale: es })}
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="text-sm font-medium text-gray-500">Información de contacto</div>
            <div className="flex items-center">
              <Phone className="h-4 w-4 mr-2 text-gray-400" />
              <span>{contact.phone_number}</span>
            </div>
            {contact.email && (
              <div className="flex items-center">
                <Mail className="h-4 w-4 mr-2 text-gray-400" />
                <span>{contact.email}</span>
              </div>
            )}
          </div>

          <div className="space-y-2">
            <div className="text-sm font-medium text-gray-500">Etiquetas</div>
            {contact.tags && contact.tags.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {contact.tags.map((tag, index) => (
                  <Badge key={index} variant="secondary" className="flex items-center gap-1">
                    <Tag className="h-3 w-3" />
                    {tag}
                  </Badge>
                ))}
              </div>
            ) : (
              <p className="text-sm text-gray-400">Sin etiquetas</p>
            )}
          </div>
        </div>

        {contact.notes && (
          <div className="space-y-2">
            <div className="text-sm font-medium text-gray-500">Notas</div>
            <div className="p-3 bg-gray-50 rounded-md text-sm">
              {contact.notes}
            </div>
          </div>
        )}

        {/* Aquí se pueden agregar más secciones como historial de llamadas, etc. */}
      </CardContent>
      <CardFooter>
        <Button variant="outline" onClick={onBack} className="flex items-center">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Volver a la lista
        </Button>
      </CardFooter>
    </Card>
  );
}
