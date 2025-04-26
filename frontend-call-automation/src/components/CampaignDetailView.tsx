"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation"; // Para redirigir después de eliminar
import React, { useState } from "react";
import { toast } from "sonner";
import { campaignApi } from "../services/campaignApi";
import { Campaign } from "../types/campaign";

interface CampaignDetailViewProps {
  campaignId: string;
}

const CampaignDetailView: React.FC<CampaignDetailViewProps> = ({
  campaignId,
}) => {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  // Query para obtener detalles
  const {
    data: campaign,
    isLoading,
    error,
    isError,
  } = useQuery<Campaign, Error>(
    ["campaign", campaignId],
    () => campaignApi.getCampaignById(campaignId),
    { enabled: !!campaignId }
  );

  // Mutación para eliminar la campaña
  const {
    mutate: deleteMutate,
    isLoading: isDeleting,
    error: deleteError,
    isError: isDeleteError,
  } = useMutation<void, Error, string>( // Tipos: Retorno, Error, Variable (id)
    campaignApi.deleteCampaign, // La función del servicio API
    {
      onSuccess: () => {
        console.log(`Campaña ${campaignId} eliminada`);
        toast.success("¡Campaña eliminada exitosamente!");
        // Invalidar query de lista para refrescar
        queryClient.invalidateQueries(["campaigns"]);
        // Redirigir a la lista
        router.push("/campaigns");
      },
      onError: (err) => {
        console.error(`Error al eliminar campaña ${campaignId}:`, err);
        toast.error("Error al eliminar la campaña.");
        setIsDeleteModalOpen(false); // Cerrar modal en caso de error
      },
    }
  );

  const handleDeleteClick = () => {
    setIsDeleteModalOpen(true); // Abre el modal de confirmación
  };

  const handleConfirmDelete = () => {
    deleteMutate(campaignId); // Ejecuta la mutación de eliminación
    // El modal se cerrará en onSuccess o onError si es necesario, o manualmente aquí
    // setIsDeleteModalOpen(false);
  };

  // --- Renderizado ---

  if (!campaignId) {
    return <div>ID de campaña no proporcionado.</div>;
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2">Cargando detalles de la campaña...</span>
      </div>
    );
  }

  if (isError) {
    return (
      <div
        className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
        role="alert"
      >
        <strong className="font-bold">Error:</strong>
        <span className="block sm:inline">
          {" "}
          {error?.message || "Error desconocido"}
        </span>
      </div>
    );
  }

  if (!campaign) {
    return <div>No se encontraron detalles para esta campaña.</div>;
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">
        Detalle de Campaña: {campaign.name}
      </h2>
      <div className="space-y-2">
        <p>
          <strong>ID:</strong> {campaign.id}
        </p>
        <p>
          <strong>Nombre:</strong> {campaign.name}
        </p>
        <p>
          <strong>Descripción:</strong> {campaign.description || "N/A"}
        </p>
        <p>
          <strong>Estado:</strong>{" "}
          <span
            className={`px-2 py-1 rounded text-xs font-medium ${getStatusColor(
              campaign.status
            )}`}
          >
            {campaign.status}
          </span>
        </p>
        {/* TODO: Mostrar más detalles (configuración, métricas, contactos, etc.) */}
      </div>
      <div className="mt-6 space-x-3">
        <Button
          variant="default"
          onClick={() => router.push(`/campaigns/${campaign.id}/edit`)}
        >
          Editar
        </Button>

        <AlertDialog>
          <AlertDialogTrigger asChild>
            <Button variant="destructive" disabled={isDeleting}>
              {isDeleting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Eliminando...
                </>
              ) : (
                "Eliminar"
              )}
            </Button>
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>Confirmar Eliminación</AlertDialogTitle>
              <AlertDialogDescription>
                ¿Estás seguro de que deseas eliminar la campaña "
                {campaign?.name}"? Esta acción no se puede deshacer.
              </AlertDialogDescription>
            </AlertDialogHeader>
            {isDeleteError && (
              <p className="text-sm text-red-600 px-4">
                Error: {deleteError?.message}
              </p>
            )}
            <AlertDialogFooter>
              <AlertDialogCancel disabled={isDeleting}>
                Cancelar
              </AlertDialogCancel>
              <AlertDialogAction
                onClick={handleConfirmDelete}
                disabled={isDeleting}
                className="bg-red-500 hover:bg-red-600"
              >
                {isDeleting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Eliminando...
                  </>
                ) : (
                  "Sí, eliminar"
                )}
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>

        <Button variant="outline" onClick={() => router.push("/campaigns")}>
          Volver a la lista
        </Button>
      </div>
    </div>
  );
};

// Helper simple para dar color al estado (mejorar según diseño)
const getStatusColor = (status: Campaign["status"]): string => {
  switch (status) {
    case "active":
      return "bg-green-100 text-green-800";
    case "paused":
      return "bg-yellow-100 text-yellow-800";
    case "completed":
      return "bg-blue-100 text-blue-800";
    case "draft":
      return "bg-gray-100 text-gray-800";
    case "archived":
      return "bg-purple-100 text-purple-800";
    default:
      return "bg-gray-100 text-gray-800";
  }
};

export default CampaignDetailView;
