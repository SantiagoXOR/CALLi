"use client";

import { useRouter } from 'next/navigation';
import { ContactForm } from '@/components/ContactForm';

export default function NewContactPage() {
  const router = useRouter();

  return (
    <ContactForm
      onCancel={() => router.push('/contacts')}
      onSuccess={() => {
        router.push('/contacts');
      }}
    />
  );
}
