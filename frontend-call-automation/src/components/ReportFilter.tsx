"use client";

import { useState } from "react";
import { useGetCampaigns } from "@/services/campaignService";
import { Button } from "@/components/ui/button";
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

interface ReportFilterProps {
  onApplyFilters: (filters: any) => void;
}

export function ReportFilter({ onApplyFilters }: ReportFilterProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [campaignId, setCampaignId] = useState<string>("");
  const [startDate, setStartDate] = useState<Date | undefined>(
    new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) // 30 days ago
  );
  const [endDate, setEndDate] = useState<Date | undefined>(new Date());
  const [groupBy, setGroupBy] = useState<string>("day");

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
    if (startDate) filters.start_date = startDate;
    if (endDate) filters.end_date = endDate;
    if (groupBy) filters.group_by = groupBy;

    onApplyFilters(filters);
  };

  // Reset filters
  const handleResetFilters = () => {
    setCampaignId("");
    setStartDate(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000));
    setEndDate(new Date());
    setGroupBy("day");
    
    onApplyFilters({
      start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
      end_date: new Date(),
      campaign_id: "",
      group_by: "day",
    });
  };

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex justify-between items-center">
          <div>
            <CardTitle>Filtros</CardTitle>
            <CardDescription>
              Filtra los reportes por diferentes criterios
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
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
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

            {/* Group by filter */}
            <div className="space-y-2">
              <Label htmlFor="groupBy">Agrupar por</Label>
              <Select
                value={groupBy}
                onValueChange={setGroupBy}
              >
                <SelectTrigger id="groupBy">
                  <SelectValue placeholder="Día" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="day">Día</SelectItem>
                  <SelectItem value="week">Semana</SelectItem>
                  <SelectItem value="month">Mes</SelectItem>
                </SelectContent>
              </Select>
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
