"use client";

import { useForm } from 'react-hook-form';

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useCreateCampaign } from "@/services/campaignService";

interface CampaignFormData {
  name: string;
  description: string;
  horarioLlamadas: string;
  maxReintentos: number;
  delayReintentos: number;
  script: string;
}

interface CampaignCreateProps {
  onSuccess: () => void;
  onCancel: () => void;
}

export default function CampaignCreate({ onSuccess, onCancel }: CampaignCreateProps): JSX.Element {
  const { register, handleSubmit, formState: { errors } } = useForm<CampaignFormData>();
  const createCampaignMutation = useCreateCampaign();

  const onSubmit = async (data: CampaignFormData): Promise<void> => {
    try {
      await createCampaignMutation.mutateAsync({
        ...data,
        status: "draft",
        start_date: "",  
        end_date: ""    
      });
      onSuccess();
    } catch (error) {
      console.error('Error al crear la campaña:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Crear Nueva Campaña</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Nombre de la Campaña</Label>
            <Input
              id="name"
              {...register("name", { required: "El nombre es requerido" })}
              placeholder="Ingrese el nombre de la campaña"
            />
            {errors.name && (
              <p className="text-sm text-red-500">{errors.name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Descripción</Label>
            <Textarea
              id="description"
              {...register("description")}
              placeholder="Describa el propósito de la campaña"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="horarioLlamadas">Horario de Llamadas</Label>
            <Input
              id="horarioLlamadas"
              {...register("horarioLlamadas")}
              placeholder="Ej: L-V 09:00-18:00"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="maxReintentos">Máximo de Reintentos</Label>
              <Input
                id="maxReintentos"
                type="number"
                {...register("maxReintentos", { 
                  valueAsNumber: true,
                  min: { value: 0, message: "Debe ser mayor o igual a 0" }
                })}
                placeholder="3"
              />
              {errors.maxReintentos && (
                <p className="text-sm text-red-500">{errors.maxReintentos.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="delayReintentos">Delay entre Reintentos (min)</Label>
              <Input
                id="delayReintentos"
                type="number"
                {...register("delayReintentos", { 
                  valueAsNumber: true,
                  min: { value: 1, message: "Debe ser mayor a 0" }
                })}
                placeholder="60"
              />
              {errors.delayReintentos && (
                <p className="text-sm text-red-500">{errors.delayReintentos.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="script">Script de Llamada</Label>
            <Textarea
              id="script"
              {...register("script")}
              placeholder="Ingrese el script que utilizarán los agentes"
              rows={5}
            />
          </div>

          <div className="flex justify-end space-x-2 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={createCampaignMutation.isLoading}
            >
              {createCampaignMutation.isLoading ? 'Creando...' : 'Crear Campaña'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </form>
  );
}