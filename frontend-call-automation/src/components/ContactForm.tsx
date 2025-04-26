"use client";

import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Contact, ContactCreate, ContactUpdate } from '../types/contact';
import { useCreateContact, useUpdateContact } from '../services/contactService';
import { toast } from 'sonner';
import { 
  Form, 
  FormControl, 
  FormField, 
  FormItem, 
  FormLabel, 
  FormMessage 
} from './ui/form';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from './ui/card';
import { X } from 'lucide-react';

// Esquema de validación con Zod
const formSchema = z.object({
  name: z.string().min(1, 'El nombre es obligatorio'),
  phone_number: z.string()
    .min(1, 'El número de teléfono es obligatorio')
    .regex(/^\+?[0-9]{9,15}$/, 'Formato de teléfono inválido. Debe tener entre 9 y 15 dígitos'),
  email: z.string().email('Email inválido').optional().or(z.literal('')),
  notes: z.string().optional(),
  tags: z.array(z.string()).optional(),
});

interface ContactFormProps {
  contact?: Contact;
  onCancel: () => void;
  onSuccess: () => void;
}

export const ContactForm: React.FC<ContactFormProps> = ({ 
  contact, 
  onCancel,
  onSuccess
}) => {
  const isEditing = !!contact;
  const createContact = useCreateContact();
  const updateContact = useUpdateContact(contact?.id || '');
  
  // Estado para manejar las etiquetas como strings
  const [tagInput, setTagInput] = React.useState('');
  
  // Configurar el formulario
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      phone_number: '',
      email: '',
      notes: '',
      tags: [],
    },
  });
  
  // Cargar datos del contacto si estamos editando
  useEffect(() => {
    if (contact) {
      form.reset({
        name: contact.name,
        phone_number: contact.phone_number,
        email: contact.email || '',
        notes: contact.notes || '',
        tags: contact.tags || [],
      });
    }
  }, [contact, form]);
  
  // Manejar envío del formulario
  const onSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      if (isEditing) {
        // Actualizar contacto existente
        await updateContact.mutateAsync(values as ContactUpdate);
        toast.success('Contacto actualizado correctamente');
      } else {
        // Crear nuevo contacto
        await createContact.mutateAsync(values as ContactCreate);
        toast.success('Contacto creado correctamente');
      }
      onSuccess();
    } catch (error) {
      console.error('Error al guardar contacto:', error);
      toast.error(`Error al ${isEditing ? 'actualizar' : 'crear'} el contacto`);
    }
  };
  
  // Manejar adición de etiquetas
  const handleAddTag = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && tagInput.trim()) {
      e.preventDefault();
      const currentTags = form.getValues('tags') || [];
      if (!currentTags.includes(tagInput.trim())) {
        form.setValue('tags', [...currentTags, tagInput.trim()]);
      }
      setTagInput('');
    }
  };
  
  // Eliminar etiqueta
  const handleRemoveTag = (tagToRemove: string) => {
    const currentTags = form.getValues('tags') || [];
    form.setValue(
      'tags',
      currentTags.filter(tag => tag !== tagToRemove)
    );
  };
  
  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>{isEditing ? 'Editar Contacto' : 'Nuevo Contacto'}</CardTitle>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nombre</FormLabel>
                  <FormControl>
                    <Input placeholder="Nombre del contacto" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="phone_number"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Número de Teléfono</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="+123456789" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input 
                      placeholder="email@ejemplo.com" 
                      type="email"
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="notes"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Notas</FormLabel>
                  <FormControl>
                    <Textarea 
                      placeholder="Notas adicionales sobre el contacto" 
                      {...field} 
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <div className="space-y-2">
              <FormLabel>Etiquetas</FormLabel>
              <div className="flex flex-wrap gap-2 mb-2">
                {form.watch('tags')?.map((tag, index) => (
                  <div 
                    key={index}
                    className="bg-secondary text-secondary-foreground px-3 py-1 rounded-full text-sm flex items-center"
                  >
                    {tag}
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="h-4 w-4 p-0 ml-2"
                      onClick={() => handleRemoveTag(tag)}
                    >
                      <X className="h-3 w-3" />
                    </Button>
                  </div>
                ))}
              </div>
              <Input
                placeholder="Añadir etiqueta (presiona Enter)"
                value={tagInput}
                onChange={(e) => setTagInput(e.target.value)}
                onKeyDown={handleAddTag}
              />
            </div>
            
            <CardFooter className="flex justify-end space-x-2 px-0 pt-4">
              <Button 
                type="button" 
                variant="outline" 
                onClick={onCancel}
              >
                Cancelar
              </Button>
              <Button 
                type="submit"
                disabled={createContact.isPending || updateContact.isPending}
              >
                {createContact.isPending || updateContact.isPending
                  ? 'Guardando...'
                  : isEditing ? 'Actualizar' : 'Crear'}
              </Button>
            </CardFooter>
          </form>
        </Form>
      </CardContent>
    </Card>
  );
};
