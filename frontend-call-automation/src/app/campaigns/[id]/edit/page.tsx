'use client';

import { CampaignForm } from '@/components/CampaignForm'; // Import the form component
import { campaignApi } from '@/services/campaignApi';
import { Campaign, CampaignCreate, CampaignUpdate } from '@/types/campaign'; // Import CampaignCreate
import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { toast } from 'sonner';

export default function EditCampaignPage() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [isLoadingData, setIsLoadingData] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      setIsLoadingData(true);
      setError(null);
      campaignApi.getCampaignById(id)
        .then(data => {
          // Format dates for input type="date"
          const formattedData = {
            ...data,
            schedule_start: data.schedule_start ? new Date(data.schedule_start).toISOString().split('T')[0] : '',
            schedule_end: data.schedule_end ? new Date(data.schedule_end).toISOString().split('T')[0] : '',
          };
          setCampaign(formattedData);
        })
        .catch(err => {
          console.error('Error fetching campaign data for edit:', err);
          setError('Error al cargar los datos de la campaña para editar.');
          toast.error('Error al cargar los datos de la campaña.');
        })
        .finally(() => {
          setIsLoadingData(false);
        });
    }
  }, [id]);

  // Adjust signature to match CampaignFormProps['onSubmit']
  const handleUpdateSubmit = async (data: CampaignCreate | CampaignUpdate) => {
    // We know in edit context, 'data' will conform to CampaignUpdate, but TS needs the broader type
    if (!id) return;
    setIsSubmitting(true);
    setError(null);
    try {
      // Ensure dates are sent in a compatible format if needed, or handle in backend/service
      // The form uses 'YYYY-MM-DD', which might be fine depending on backend expectation
      // Assert 'data' as CampaignUpdate for the API call
      const updatedCampaign = await campaignApi.updateCampaign(id, data as CampaignUpdate);
      toast.success(`Campaña "${updatedCampaign.name}" actualizada correctamente.`);
      router.push(`/campaigns/${id}`); // Redirect to detail page after successful update
    } catch (err) {
      console.error('Error updating campaign:', err);
      toast.error('Error al actualizar la campaña. Intente nuevamente.');
      setError('Error al actualizar la campaña.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoadingData) {
    return <div className="container mx-auto p-4">Cargando datos para editar...</div>;
  }

  if (error) {
    return <div className="container mx-auto p-4 text-red-600">{error}</div>;
  }

  if (!campaign) {
    return <div className="container mx-auto p-4">No se encontró la campaña para editar.</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Editar Campaña: {campaign.name}</h1>
      <CampaignForm
        initialData={campaign}
        onSubmit={handleUpdateSubmit}
        isLoading={isSubmitting}
      />
    </div>
  );
}
