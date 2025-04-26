"use client";

import {
  Clock,
  Edit,
  FileText,
  Pause,
  Play,
  Trash2,
  Users,
} from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { useGetCampaign } from "@/services/campaignService";

// Componente Skeleton para CampaignDetail
function CampaignDetailSkeleton() {
  return (
    <div className="space-y-6">
      {/* Encabezado de la campaña - skeleton */}
      <div className="flex justify-between items-center">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="space-x-2 flex">
          <Skeleton className="h-10 w-24" />
          <Skeleton className="h-10 w-24" />
        </div>
      </div>

      {/* Estado y progreso - skeleton */}
      <Card>
        <CardHeader>
          <Skeleton className="h-6 w-48" />
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <Skeleton className="h-6 w-24" />
            <Skeleton className="h-10 w-24" />
          </div>
          <Skeleton className="h-4 w-full mb-2" />
          <Skeleton className="h-4 w-24" />
        </CardContent>
      </Card>

      {/* Estadísticas - skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <Skeleton className="h-8 w-8 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-6 w-16" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <Skeleton className="h-8 w-8 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-6 w-24" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <Skeleton className="h-8 w-8 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-32" />
                <Skeleton className="h-6 w-24" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

interface CampaignDetailProps {
  campaignId: string | number;
  onEdit: (id: string | number) => void;
  onDelete: (id: string | number) => void;
}

export default function CampaignDetail({
  campaignId,
  onEdit,
  onDelete,
}: CampaignDetailProps): JSX.Element {
  const {
    data: campaign,
    isLoading,
    error,
  } = useGetCampaign(campaignId.toString());

  if (isLoading) return <CampaignDetailSkeleton />;
  if (error)
    return (
      <div className="p-4 text-red-500">
        Error al cargar los detalles de la campaña
      </div>
    );
  if (!campaign)
    return <div className="p-4 text-amber-500">No se encontró la campaña</div>;

  const getStatusColor = (status: string): string => {
    const colors = {
      draft: "bg-gray-500",
      active: "bg-green-500",
      completed: "bg-blue-500",
      cancelled: "bg-purple-500",
    };
    return colors[status as keyof typeof colors] || "bg-gray-500";
  };

  return (
    <div className="space-y-6">
      {/* Encabezado de la campaña */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">{campaign.name}</h1>
          <p className="text-gray-500">{campaign.description}</p>
        </div>
        <div className="space-x-2">
          <Button variant="outline" onClick={() => onEdit(campaign.id)}>
            <Edit className="h-4 w-4 mr-2" />
            Editar
          </Button>
          <Button variant="destructive" onClick={() => onDelete(campaign.id)}>
            <Trash2 className="h-4 w-4 mr-2" />
            Eliminar
          </Button>
        </div>
      </div>

      {/* Estado y progreso */}
      <Card>
        <CardHeader>
          <CardTitle>Estado de la Campaña</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between mb-4">
            <Badge className={getStatusColor(campaign.status)}>
              {campaign.status}
            </Badge>
            <Button
              variant="outline"
              disabled={
                campaign.status === "completed" ||
                campaign.status === "cancelled"
              }
            >
              {campaign.status === "active" ? (
                <>
                  <Pause className="h-4 w-4 mr-2" />
                  Pausar
                </>
              ) : (
                <>
                  <Play className="h-4 w-4 mr-2" />
                  Iniciar
                </>
              )}
            </Button>
          </div>
          <Progress value={0} className="mb-2" />
          <p className="text-sm text-gray-500">Progreso: 0%</p>
        </CardContent>
      </Card>

      {/* Estadísticas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <Users className="h-8 w-8 text-blue-500" />
              <div>
                <p className="text-sm text-gray-500">Total Contactos</p>
                <h3 className="text-2xl font-bold">0</h3>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <Clock className="h-8 w-8 text-green-500" />
              <div>
                <p className="text-sm text-gray-500">Horario de Llamadas</p>
                <h3 className="text-lg font-semibold">No definido</h3>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-4">
              <FileText className="h-8 w-8 text-purple-500" />
              <div>
                <p className="text-sm text-gray-500">Script</p>
                <h3 className="text-lg font-semibold truncate max-w-[200px]">
                  Sin script
                </h3>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
