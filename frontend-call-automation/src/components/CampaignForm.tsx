import { Loader2 } from "lucide-react";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { CampaignCreate, CampaignUpdate } from "../types/campaign";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Textarea } from "./ui/textarea";

// Esquema de validación con Zod
const campaignFormSchema = z
  .object({
    name: z
      .string()
      .min(3, { message: "El nombre debe tener al menos 3 caracteres" })
      .max(100, { message: "El nombre no puede exceder los 100 caracteres" }),
    description: z.string().optional(),
    status: z.string(),
    script_template: z.string().optional(),
    contact_list_ids: z.array(z.string()).optional(),
    schedule_start: z.string().refine((date) => !isNaN(Date.parse(date)), {
      message: "Fecha de inicio inválida",
    }),
    schedule_end: z.string().refine((date) => !isNaN(Date.parse(date)), {
      message: "Fecha de fin inválida",
    }),
    calling_hours_start: z.string().regex(/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/, {
      message: "Formato de hora inválido (HH:MM)",
    }),
    calling_hours_end: z.string().regex(/^([01]?[0-9]|2[0-3]):[0-5][0-9]$/, {
      message: "Formato de hora inválido (HH:MM)",
    }),
    max_retries: z.number().int().min(0).max(10).optional(),
    retry_delay_minutes: z.number().int().min(1).max(1440).optional(),
  })
  .refine(
    (data) => {
      const start = new Date(data.schedule_start);
      const end = new Date(data.schedule_end);
      return start <= end;
    },
    {
      message: "La fecha de fin debe ser posterior a la fecha de inicio",
      path: ["schedule_end"],
    }
  );

type CampaignFormData = z.infer<typeof campaignFormSchema>;

interface CampaignFormProps {
  initialData?: CampaignUpdate;
  onSubmit: (data: CampaignCreate | CampaignUpdate) => Promise<void>;
  isLoading: boolean;
}

export const CampaignForm: React.FC<CampaignFormProps> = ({
  initialData,
  onSubmit,
  isLoading,
}) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    watch,
    setError,
  } = useForm<CampaignFormData>({
    resolver: zodResolver(campaignFormSchema),
    defaultValues: initialData || {
      name: "",
      description: "",
      status: "DRAFT",
      script_template: "",
      contact_list_ids: [],
      schedule_start: new Date().toISOString().split("T")[0],
      schedule_end: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
        .toISOString()
        .split("T")[0],
      calling_hours_start: "09:00",
      calling_hours_end: "18:00",
      max_retries: 3,
      retry_delay_minutes: 60,
    },
  });

  const [contactLists, setContactLists] = useState<
    { id: string; name: string }[]
  >([
    { id: "1", name: "Lista de Clientes Potenciales" },
    { id: "2", name: "Clientes Existentes" },
    { id: "3", name: "Seguimiento de Ventas" },
  ]);

  const handleFormSubmit = async (data: CampaignFormData) => {
    try {
      // Validación adicional de fechas
      const startDate = new Date(data.schedule_start);
      const endDate = new Date(data.schedule_end);

      if (startDate > endDate) {
        setError("schedule_end", {
          type: "manual",
          message: "La fecha de fin debe ser posterior a la fecha de inicio",
        });
        return;
      }

      // Convertir los campos numéricos
      const formattedData = {
        ...data,
        max_retries: data.max_retries ? Number(data.max_retries) : 3,
        retry_delay_minutes: data.retry_delay_minutes
          ? Number(data.retry_delay_minutes)
          : 60,
      };

      await onSubmit(formattedData as CampaignCreate | CampaignUpdate);
      toast.success("Campaña guardada exitosamente");
    } catch (error) {
      console.error("Error al enviar el formulario:", error);
      toast.error("Error al guardar la campaña. Por favor, intenta de nuevo.");
    }
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="name">Nombre de la Campaña</Label>
            <Input
              id="name"
              {...register("name", { required: "El nombre es obligatorio" })}
              placeholder="Nombre de la campaña"
              className={errors.name ? "border-red-500" : ""}
            />
            {errors.name && (
              <p className="text-red-500 text-sm">{errors.name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Descripción</Label>
            <Textarea
              id="description"
              {...register("description")}
              placeholder="Descripción de la campaña"
              rows={3}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="status">Estado</Label>
            <Select
              defaultValue={initialData?.status || "DRAFT"}
              onValueChange={(value) => setValue("status", value)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecciona un estado" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="DRAFT">Borrador</SelectItem>
                <SelectItem value="ACTIVE">Activa</SelectItem>
                <SelectItem value="PAUSED">Pausada</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="script_template">Plantilla de Script</Label>
            <Textarea
              id="script_template"
              {...register("script_template")}
              placeholder="Plantilla de script para las llamadas"
              rows={5}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="schedule_start">Fecha de Inicio</Label>
              <Input
                id="schedule_start"
                type="date"
                {...register("schedule_start", {
                  required: "La fecha de inicio es obligatoria",
                })}
              />
              {errors.schedule_start && (
                <p className="text-red-500 text-sm">
                  {errors.schedule_start.message}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="schedule_end">Fecha de Fin</Label>
              <Input
                id="schedule_end"
                type="date"
                {...register("schedule_end", {
                  required: "La fecha de fin es obligatoria",
                })}
              />
              {errors.schedule_end && (
                <p className="text-red-500 text-sm">
                  {errors.schedule_end.message}
                </p>
              )}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="max_retries">Máximo de Reintentos</Label>
              <Input
                id="max_retries"
                type="number"
                {...register("max_retries")}
                placeholder="Número máximo de reintentos"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="retry_delay_minutes">
                Retraso entre Reintentos (minutos)
              </Label>
              <Input
                id="retry_delay_minutes"
                type="number"
                {...register("retry_delay_minutes")}
                placeholder="Minutos de retraso entre reintentos"
              />
            </div>
          </div>

          <Button type="submit" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Enviando...
              </>
            ) : (
              "Guardar Campaña"
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
};
