'use client';

import { Badge } from '@/components/ui/badge'; // Assuming Badge component exists
import { Button } from '@/components/ui/button'; // Assuming Button component exists
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'; // Assuming Card components exist
import { campaignApi } from '@/services/campaignApi';
import { Campaign } from '@/types/campaign';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { toast } from 'sonner'; // Assuming sonner for toasts

export default function CampaignDetailPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string; // Get ID from route params

  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      setIsLoading(true);
      setError(null);
      campaignApi.getCampaignById(id)
        .then(data => {
          setCampaign(data);
        })
        .catch(err => {
          console.error('Error fetching campaign details:', err);
          setError('Error al cargar la campaña. Intente nuevamente.');
          toast.error('Error al cargar la campaña.');
        })
        .finally(() => {
          setIsLoading(false);
        });
    }
  }, [id]);

  const handleDelete = async () => {
    if (!campaign) return;

    // Basic confirmation dialog
    if (window.confirm(`¿Está seguro que desea eliminar la campaña "${campaign.name}"? Esta acción no se puede deshacer.`)) {
      try {
        await campaignApi.deleteCampaign(campaign.id);
        toast.success(`Campaña "${campaign.name}" eliminada correctamente.`);
        router.push('/'); // Redirect to campaign list after deletion
      } catch (err) {
        console.error('Error deleting campaign:', err);
        toast.error('Error al eliminar la campaña. Intente nuevamente.');
        setError('Error al eliminar la campaña.');
      }
    }
  };

  if (isLoading) {
    return <div className="container mx-auto p-4">Cargando detalles de la campaña...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-4 text-red-600">{error}</div>;
  }

  if (!campaign) {
    return <div className="container mx-auto p-4">No se encontró la campaña.</div>;
  }

  // Helper to format dates
  const formatDate = (dateString: string | Date | undefined) => {
    if (!dateString) return 'N/A';
    try {
      return new Date(dateString).toLocaleString();
    } catch {
      return 'Fecha inválida';
    }
  };

  return (
    <div className="container mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex justify-between items-center">
            {campaign.name}
            <Badge variant={campaign.status === 'ACTIVE' ? 'default' : campaign.status === 'PAUSED' ? 'secondary' : 'outline'}>
              {campaign.status || 'N/A'}
            </Badge>
          </CardTitle>
          <CardDescription>{campaign.description || 'Sin descripción.'}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div><strong>ID:</strong> {campaign.id}</div>
          <div><strong>Inicio Programado:</strong> {formatDate(campaign.schedule_start)}</div>
          <div><strong>Fin Programado:</strong> {formatDate(campaign.schedule_end)}</div>
          <div><strong>Plantilla Script:</strong> <pre className="bg-gray-100 p-2 rounded text-sm">{campaign.script_template || 'N/A'}</pre></div>
          <div><strong>Máx. Reintentos:</strong> {campaign.max_retries ?? 'N/A'}</div>
          <div><strong>Retraso Reintento (min):</strong> {campaign.retry_delay_minutes ?? 'N/A'}</div>
          <div><strong>Horario Llamadas:</strong> {campaign.calling_hours_start || 'N/A'} - {campaign.calling_hours_end || 'N/A'}</div>
          {/* Consider adding contact list display later */}
          {/* Consider adding stats display later */}
        </CardContent>
        <CardFooter className="flex justify-end space-x-2">
           <Link href={`/campaigns/${campaign.id}/edit`}>
             <Button variant="outline">Editar</Button>
           </Link>
           <Button variant="destructive" onClick={handleDelete}>Eliminar</Button>
        </CardFooter>
      </Card>
    </div>
  );
}
