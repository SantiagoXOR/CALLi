"use client";

import { useEffect, useState } from "react";
import { useSupabase } from "@/lib/supabase";
import { useSupabaseData } from "@/hooks/useSupabaseData";
import { Database } from "@/types/supabase";

// Tipo para los datos de la campaña
type Campaign = Database["public"]["Tables"]["campaigns"]["Row"];

export function SupabaseExample() {
  const supabase = useSupabase();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Usar el hook personalizado para interactuar con la tabla de campañas
  const campaignsData = useSupabaseData<Campaign>("campaigns");

  // Cargar campañas al montar el componente
  useEffect(() => {
    async function loadCampaigns() {
      try {
        // Método 1: Usando el hook personalizado
        const data = await campaignsData.getAll({
          orderBy: { column: "created_at", ascending: false },
          limit: 10,
        });
        setCampaigns(data);
      } catch (error) {
        console.error("Error al cargar campañas:", error);
      } finally {
        setLoading(false);
      }
    }

    loadCampaigns();
  }, []);

  // Ejemplo de cómo crear una nueva campaña
  const createCampaign = async () => {
    const newCampaign = {
      name: `Nueva Campaña ${new Date().toISOString()}`,
      description: "Campaña creada desde el ejemplo de Supabase",
      status: "draft" as const,
    };

    // Método 1: Usando el hook personalizado
    const created = await campaignsData.create(newCampaign);
    
    if (created) {
      setCampaigns([created, ...campaigns]);
    }

    // Método 2: Usando el cliente de Supabase directamente
    // const { data, error } = await supabase
    //   .from("campaigns")
    //   .insert([newCampaign])
    //   .select()
    //   .single();
    
    // if (error) {
    //   console.error("Error al crear campaña:", error);
    //   return;
    // }
    
    // setCampaigns([data as Campaign, ...campaigns]);
  };

  // Ejemplo de cómo eliminar una campaña
  const deleteCampaign = async (id: string) => {
    // Método 1: Usando el hook personalizado
    const success = await campaignsData.remove(id);
    
    if (success) {
      setCampaigns(campaigns.filter(campaign => campaign.id !== id));
    }

    // Método 2: Usando el cliente de Supabase directamente
    // const { error } = await supabase
    //   .from("campaigns")
    //   .delete()
    //   .eq("id", id);
    
    // if (error) {
    //   console.error("Error al eliminar campaña:", error);
    //   return;
    // }
    
    // setCampaigns(campaigns.filter(campaign => campaign.id !== id));
  };

  if (loading) {
    return <div>Cargando campañas...</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Ejemplo de Supabase</h2>
      
      <button
        onClick={createCampaign}
        className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded mb-4"
      >
        Crear Nueva Campaña
      </button>
      
      <div className="space-y-4">
        {campaigns.length === 0 ? (
          <p>No hay campañas disponibles</p>
        ) : (
          campaigns.map((campaign) => (
            <div
              key={campaign.id}
              className="border p-4 rounded shadow-sm flex justify-between items-center"
            >
              <div>
                <h3 className="font-semibold">{campaign.name}</h3>
                <p className="text-gray-600">{campaign.description}</p>
                <div className="flex space-x-2 mt-2">
                  <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                    Estado: {campaign.status}
                  </span>
                  <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                    Creada: {new Date(campaign.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
              
              <button
                onClick={() => deleteCampaign(campaign.id)}
                className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm"
              >
                Eliminar
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
