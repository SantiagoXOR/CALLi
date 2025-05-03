import { Loader2 } from 'lucide-react';
import { useRouter } from 'next/navigation';
import React, { useEffect, useState } from 'react';
import { campaignApi } from '../services/campaignApi';
import { Campaign } from '../types/campaign';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

export const CampaignListView: React.FC = () => {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        setLoading(true);
        const data = await campaignApi.getCampaigns();
        setCampaigns(data);
        setError(null);
      } catch (err) {
        setError('Error al cargar las campañas. Por favor, intenta de nuevo.');
        console.error('Error fetching campaigns:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  const handleCreateCampaign = () => {
    router.push('/campaigns/create');
  };

  const handleViewCampaign = (id: string) => {
    router.push(`/campaigns/${id}`);
  };

  const getStatusBadge = (status: string) => {
    const statusMap: Record<string, { color: string; label: string }> = {
      DRAFT: { color: 'bg-gray-200 text-gray-800', label: 'Borrador' },
      ACTIVE: { color: 'bg-green-200 text-green-800', label: 'Activa' },
      PAUSED: { color: 'bg-yellow-200 text-yellow-800', label: 'Pausada' },
      COMPLETED: { color: 'bg-blue-200 text-blue-800', label: 'Completada' },
      CANCELLED: { color: 'bg-red-200 text-red-800', label: 'Cancelada' }
    };

    const { color, label } = statusMap[status] || { color: 'bg-gray-200 text-gray-800', label: status };
    return <Badge className={color}>{label}</Badge>;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2">Cargando campañas...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Error:</strong>
        <span className="block sm:inline"> {error}</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto py-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Campañas de Llamadas</h1>
        <Button onClick={handleCreateCampaign}>Crear Nueva Campaña</Button>
      </div>

      {campaigns.length === 0 ? (
        <div className="text-center py-10 bg-gray-50 rounded-lg">
          <p className="text-gray-500">No hay campañas disponibles.</p>
          <Button onClick={handleCreateCampaign} className="mt-4">
            Crear tu primera campaña
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {campaigns.map((campaign) => (
            <Card key={campaign.id} className="cursor-pointer hover:shadow-md transition-shadow"
                  onClick={() => handleViewCampaign(campaign.id)}>
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg">{campaign.name}</CardTitle>
                  {getStatusBadge(campaign.status)}
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-500 mb-4 line-clamp-2">{campaign.description}</p>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>
                    <p className="text-gray-500">Llamadas:</p>
                    <p>{campaign.total_calls || 0}</p>
                  </div>
                  <div>
                    <p className="text-gray-500">Completadas:</p>
                    <p>{campaign.successful_calls || 0}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
