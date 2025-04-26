"use client";

import { useState } from "react";
import { useGetCampaigns } from "@/services/campaignService";
import { CallStatus } from "@/types/call";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { DateTimePicker } from "./DateTimePicker";
import { Filter, RefreshCw, X } from "lucide-react";

interface CallFilterProps {
  onApplyFilters: (filters: any) => void;
}

export function CallFilter({ onApplyFilters }: CallFilterProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [campaignId, setCampaignId] = useState<string>("");
  const [contactId, setContactId] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [startDate, setStartDate] = useState<Date | undefined>(undefined);
  const [endDate, setEndDate] = useState<Date | undefined>(undefined);
  const [phoneNumber, setPhoneNumber] = useState<string>("");

  // Fetch campaigns for filter dropdown
  const { data: campaigns } = useGetCampaigns();

  // Toggle filter panel
  const toggleFilters = () => {
    setIsExpanded(!isExpanded);
  };

  // Apply filters
  const handleApplyFilters = () => {
    const filters: any = {};

    if (campaignId) filters.campaign_id = campaignId;
    if (contactId) filters.contact_id = contactId;
    if (status) filters.status = status;
    if (startDate) filters.start_date = startDate.toISOString();
    if (endDate) filters.end_date = endDate.toISOString();
    if (phoneNumber) filters.phone_number = phoneNumber;

    onApplyFilters(filters);
  };

  // Reset filters
  const handleResetFilters = () => {
    setCampaignId("");
    setContactId("");
    setStatus("");
    setStartDate(undefined);
    setEndDate(undefined);
    setPhoneNumber("");
    onApplyFilters({});
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Filtros</CardTitle>
            <CardDescription>
              Filtra las llamadas por diferentes criterios
            </CardDescription>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleFilters}
            className="h-8 w-8 p-0"
          >
            {isExpanded ? (
              <X className="h-4 w-4" />
            ) : (
              <Filter className="h-4 w-4" />
            )}
          </Button>
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent className="grid gap-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* Campaign filter */}
            <div className="space-y-2">
              <Label htmlFor="campaign">Campaña</Label>
              <Select
                value={campaignId}
                onValueChange={setCampaignId}
              >
                <SelectTrigger id="campaign">
                  <SelectValue placeholder="Todas las campañas" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todas las campañas</SelectItem>
                  {campaigns?.map((campaign: any) => (
                    <SelectItem key={campaign.id} value={campaign.id}>
                      {campaign.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Status filter */}
            <div className="space-y-2">
              <Label htmlFor="status">Estado</Label>
              <Select
                value={status}
                onValueChange={setStatus}
              >
                <SelectTrigger id="status">
                  <SelectValue placeholder="Todos los estados" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Todos los estados</SelectItem>
                  <SelectItem value={CallStatus.QUEUED}>En cola</SelectItem>
                  <SelectItem value={CallStatus.RINGING}>Sonando</SelectItem>
                  <SelectItem value={CallStatus.IN_PROGRESS}>
                    En progreso
                  </SelectItem>
                  <SelectItem value={CallStatus.COMPLETED}>
                    Completada
                  </SelectItem>
                  <SelectItem value={CallStatus.FAILED}>Fallida</SelectItem>
                  <SelectItem value={CallStatus.CANCELLED}>
                    Cancelada
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Phone number filter */}
            <div className="space-y-2">
              <Label htmlFor="phone">Número de teléfono</Label>
              <Input
                id="phone"
                placeholder="Ej: +34612345678"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </div>

            {/* Date range filter */}
            <div className="space-y-2">
              <Label>Fecha inicio</Label>
              <DateTimePicker
                date={startDate}
                setDate={setStartDate}
                showTimePicker={false}
              />
            </div>

            <div className="space-y-2">
              <Label>Fecha fin</Label>
              <DateTimePicker
                date={endDate}
                setDate={setEndDate}
                showTimePicker={false}
              />
            </div>

            {/* Contact ID filter */}
            <div className="space-y-2">
              <Label htmlFor="contact">ID de contacto</Label>
              <Input
                id="contact"
                placeholder="ID del contacto"
                value={contactId}
                onChange={(e) => setContactId(e.target.value)}
              />
            </div>
          </div>
        </CardContent>
      )}

      {isExpanded && (
        <CardFooter className="flex justify-between">
          <Button
            variant="outline"
            size="sm"
            onClick={handleResetFilters}
            className="text-xs"
          >
            <RefreshCw className="mr-2 h-3 w-3" />
            Reiniciar filtros
          </Button>
          <Button size="sm" onClick={handleApplyFilters} className="text-xs">
            Aplicar filtros
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}
