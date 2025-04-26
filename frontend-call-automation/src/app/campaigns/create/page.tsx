import { CampaignForm } from '@/components/CampaignForm';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { campaignApi } from '@/services/campaignApi';
import { CampaignCreate } from '@/types/campaign';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import React from 'react';

const CampaignCreatePage: React.FC = () => {
  const router = useRouter();
  const [isLoading, setIsLoading] = React.useState(false);

  const handleCreateCampaign = async (data: CampaignCreate) => {
    setIsLoading(true);
    try {
      await campaignApi.createCampaign(data);
      router.push('/campaigns');
    } catch (error) {
      console.error('Error al crear la campaña:', error);
      alert('Error al crear la campaña. Por favor, inténtalo de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-10">
      <Card className="w-full max-w-3xl mx-auto">
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle className="text-2xl">Crear Nueva Campaña</CardTitle>
            <Link href="/campaigns">
              <Button variant="outline">
                Volver a la Lista
              </Button>
            </Link>
          </div>
        </CardHeader>
        <CampaignForm onSubmit={handleCreateCampaign} isLoading={isLoading} />
      </Card>
    </div>
  );
};

export default CampaignCreatePage;
