"use client";

import { useEffect, useState } from "react";
import { useSupabaseMCP } from "@/lib/supabase-mcp";
import { useSupabaseMCPData } from "@/hooks/useSupabaseMCPData";
import { Database } from "@/types/supabase";

// Tipo para los datos de la campaña
type Campaign = Database["public"]["Tables"]["campaigns"]["Row"];

export function SupabaseMCPExample() {
  const supabaseMCP = useSupabaseMCP();
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Usar el hook personalizado para interactuar con la tabla de campañas
  const campaignsData = useSupabaseMCPData<Campaign>("campaigns");

  // Cargar campañas al montar el componente
  useEffect(() => {
    async function loadCampaigns() {
      try {
        // Método 1: Usando el hook personalizado
        const data = await campaignsData.getAll({
          order: { column: "created_at", ascending: false },
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
      name: `Nueva Campaña MCP ${new Date().toISOString()}`,
      description: "Campaña creada desde el ejemplo de Supabase MCP",
      status: "draft" as const,
    };

    // Método 1: Usando el hook personalizado
    const created = await campaignsData.create(newCampaign);
    
    if (created) {
      setCampaigns([created, ...campaigns]);
    }

    // Método 2: Usando el cliente MCP directamente
    // const { data, error } = await supabaseMCP.insert("campaigns", newCampaign);
    
    // if (error) {
    //   console.error("Error al crear campaña:", error.message);
    //   return;
    // }
    
    // if (data) {
    //   setCampaigns([data as Campaign, ...campaigns]);
    // }
  };

  // Ejemplo de cómo eliminar una campaña
  const deleteCampaign = async (id: string) => {
    // Método 1: Usando el hook personalizado
    const success = await campaignsData.remove(id);
    
    if (success) {
      setCampaigns(campaigns.filter(campaign => campaign.id !== id));
    }

    // Método 2: Usando el cliente MCP directamente
    // const { error } = await supabaseMCP.delete("campaigns", { id });
    
    // if (error) {
    //   console.error("Error al eliminar campaña:", error.message);
    //   return;
    // }
    
    // setCampaigns(campaigns.filter(campaign => campaign.id !== id));
  };

  // Ejemplo de cómo ejecutar una consulta SQL personalizada
  const runCustomQuery = async () => {
    try {
      setLoading(true);
      
      const { data, error } = await supabaseMCP.query<Campaign[]>(
        "SELECT * FROM campaigns WHERE status = $1 ORDER BY created_at DESC LIMIT 5",
        ["active"]
      );
      
      if (error) {
        console.error("Error en consulta personalizada:", error.message);
        return;
      }
      
      if (data) {
        console.log("Resultado de consulta personalizada:", data);
        // Hacer algo con los datos
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Cargando campañas desde MCP...</div>;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Ejemplo de Supabase MCP</h2>
      
      <div className="flex space-x-4 mb-4">
        <button
          onClick={createCampaign}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Crear Nueva Campaña
        </button>
        
        <button
          onClick={runCustomQuery}
          className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded"
        >
          Ejecutar Consulta Personalizada
        </button>
      </div>
      
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
