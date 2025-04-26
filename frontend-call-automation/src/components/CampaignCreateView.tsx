"use client";

import { useRouter } from "next/navigation"; // Para redirigir después de crear
import React, { useState } from "react";
import { SubmitHandler } from "react-hook-form";
import { toast } from "sonner";
import { campaignApi } from "../services/campaignApi";
import { CampaignForm } from "./CampaignForm";

const CampaignCreateView: React.FC = () => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleCreateSubmit: SubmitHandler<CampaignCreate> = async (data) => {
    setIsLoading(true);
    setError(null);
    try {
      const newCampaign = await campaignApi.createCampaign(data);
      console.log("Campaña creada:", newCampaign);
      toast.success("¡Campaña creada exitosamente!");
      // Redirigir a la lista de campañas o al detalle de la nueva campaña
      router.push("/campaigns"); // Asumiendo que '/campaigns' es la ruta de la lista
      // O redirigir al detalle: router.push(`/campaigns/${newCampaign.id}`);
    } catch (err) {
      console.error("Error al crear la campaña:", err);
      setError(
        "Error al crear la campaña. Verifique los datos e intente nuevamente."
      );
      toast.error("Error al crear la campaña.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Crear Nueva Campaña</h2>
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 border border-red-300 rounded">
          {error}
        </div>
      )}
      <CampaignForm onSubmit={handleCreateSubmit} isLoading={isLoading} />
    </div>
  );
};

export default CampaignCreateView;
