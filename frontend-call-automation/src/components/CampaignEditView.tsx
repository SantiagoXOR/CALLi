import React from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Textarea } from "./ui/textarea";

interface CampaignEditData {
  id: string;
  nombre: string;
  descripcion: string;
  estado: string;
  fechaInicio: string;
  fechaFin: string;
  horarioLlamadas: string;
  script: string;
}

interface CampaignEditViewProps {
  campaignId: string;
  onSave?: (campaña: CampaignEditData) => void;
  onCancel?: () => void;
}

export default function CampaignEditView({
  campaignId,
  onSave,
  onCancel
}: CampaignEditViewProps): JSX.Element {
  // Aquí normalmente cargarías los datos de la campaña usando el ID
  // Por ahora, usaremos un estado local simulado
  const [formData, setFormData] = React.useState<CampaignEditData>({
    id: campaignId,
    nombre: "Campaña de ejemplo",
    descripcion: "Descripción de la campaña",
    estado: "Borrador",
    fechaInicio: "",
    fechaFin: "",
    horarioLlamadas: "",
    script: ""
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSelectChange = (name: string, value: string): void => {
    setFormData(prev => ({ ...prev, [name]: value as string }));
  };

  const handleSubmit = (e: React.FormEvent): void => {
    e.preventDefault();
    if (onSave) {
      onSave(formData);
    }
  };

  return (
    <Card className="max-w-3xl mx-auto">
      <CardHeader>
        <CardTitle>Editar Campaña</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="nombre">Nombre de la campaña</Label>
            <Input
              id="nombre"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="descripcion">Descripción</Label>
            <Textarea
              id="descripcion"
              name="descripcion"
              value={formData.descripcion}
              onChange={handleChange}
              rows={3}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="estado">Estado</Label>
            <Select
              value={formData.estado}
              onValueChange={(value) => handleSelectChange("estado", value)}
            >
              <SelectTrigger>
                <SelectValue placeholder="Seleccionar estado" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="Borrador">Borrador</SelectItem>
                <SelectItem value="Activa">Activa</SelectItem>
                <SelectItem value="Pausada">Pausada</SelectItem>
                <SelectItem value="Completada">Completada</SelectItem>
                <SelectItem value="Archivada">Archivada</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="fechaInicio">Fecha de inicio</Label>
              <Input
                id="fechaInicio"
                name="fechaInicio"
                type="date"
                value={formData.fechaInicio}
                onChange={handleChange}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="fechaFin">Fecha de fin</Label>
              <Input
                id="fechaFin"
                name="fechaFin"
                type="date"
                value={formData.fechaFin}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="horarioLlamadas">Horario de llamadas</Label>
            <Input
              id="horarioLlamadas"
              name="horarioLlamadas"
              placeholder="Ej: L-V 9:00-18:00"
              value={formData.horarioLlamadas}
              onChange={handleChange}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="script">Script de llamada</Label>
            <Textarea
              id="script"
              name="script"
              value={formData.script}
              onChange={handleChange}
              rows={5}
              placeholder="Introduce el script que usará el agente durante la llamada..."
            />
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancelar
          </Button>
          <Button type="submit">
            Guardar Cambios
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
