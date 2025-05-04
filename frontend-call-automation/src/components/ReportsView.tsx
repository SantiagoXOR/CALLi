"use client";

import { useState } from "react";
import { useGetCallMetrics, useGetCampaignPerformance } from "@/services/reportService";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { ReportFilter } from "./ReportFilter";
import { MetricsOverview } from "./MetricsOverview";
import { CampaignPerformance } from "./CampaignPerformance";
import { CallTimeline } from "./CallTimeline";
import { CallStatusDistribution } from "./CallStatusDistribution";
import { Download, RefreshCw } from "lucide-react";
import { toast } from "sonner";

export function ReportsView() {
  const [activeTab, setActiveTab] = useState("overview");
  const [filters, setFilters] = useState({
    start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 30 days ago
    end_date: new Date(),
    campaign_id: "",
    group_by: "day",
  });

  // Fetch metrics data
  const {
    data: metricsData,
    isLoading: isLoadingMetrics,
    isError: isErrorMetrics,
    refetch: refetchMetrics,
  } = useGetCallMetrics(filters);

  // Fetch campaign performance data
  const {
    data: campaignData,
    isLoading: isLoadingCampaigns,
    isError: isErrorCampaigns,
    refetch: refetchCampaigns,
  } = useGetCampaignPerformance(filters);

  // Handle filter changes
  const handleApplyFilters = (newFilters: any) => {
    setFilters({ ...filters, ...newFilters });
  };

  // Handle export
  const handleExport = async () => {
    try {
      // Build query parameters
      const params = new URLSearchParams();

      if (filters.campaign_id) {
        params.append("campaign_id", filters.campaign_id);
      }

      if (filters.start_date) {
        params.append("start_date", filters.start_date.toISOString());
      }

      if (filters.end_date) {
        params.append("end_date", filters.end_date.toISOString());
      }

      // Format (csv or excel)
      params.append("format", "excel");

      // Create URL
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const url = `${API_URL}/api/reports/export/calls?${params.toString()}`;

      // Open in new tab
      window.open(url, "_blank");

      toast.success("Exportación iniciada");
    } catch (error) {
      toast.error("Error al exportar los datos");
      console.error("Export error:", error);
    }
  };

  // Handle refresh
  const handleRefresh = () => {
    refetchMetrics();
    refetchCampaigns();
    toast.success("Datos actualizados");
  };

  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Reportes</h1>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={handleRefresh}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Actualizar
          </Button>
          <Button variant="outline" onClick={handleExport}>
            <Download className="h-4 w-4 mr-2" />
            Exportar
          </Button>
        </div>
      </div>

      <ReportFilter onApplyFilters={handleApplyFilters} />

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="overview">Resumen</TabsTrigger>
          <TabsTrigger value="campaigns">Campañas</TabsTrigger>
          <TabsTrigger value="timeline">Línea de tiempo</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6 mt-6">
          <MetricsOverview
            data={metricsData}
            isLoading={isLoadingMetrics}
            isError={isErrorMetrics}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Distribución por estado</CardTitle>
                <CardDescription>
                  Distribución de llamadas por estado
                </CardDescription>
              </CardHeader>
              <CardContent>
                <CallStatusDistribution
                  data={metricsData?.by_status}
                  isLoading={isLoadingMetrics}
                  isError={isErrorMetrics}
                />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Actividad reciente</CardTitle>
                <CardDescription>
                  Llamadas en los últimos días
                </CardDescription>
              </CardHeader>
              <CardContent>
                <CallTimeline
                  data={metricsData?.timeline?.slice(-7)}
                  isLoading={isLoadingMetrics}
                  isError={isErrorMetrics}
                />
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="campaigns" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Rendimiento de campañas</CardTitle>
              <CardDescription>
                Comparativa de rendimiento entre campañas
              </CardDescription>
            </CardHeader>
            <CardContent>
              <CampaignPerformance
                data={campaignData}
                isLoading={isLoadingCampaigns}
                isError={isErrorCampaigns}
              />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="timeline" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Línea de tiempo</CardTitle>
              <CardDescription>
                Evolución de llamadas a lo largo del tiempo
              </CardDescription>
            </CardHeader>
            <CardContent className="h-[500px]">
              <CallTimeline
                data={metricsData?.timeline}
                isLoading={isLoadingMetrics}
                isError={isErrorMetrics}
                showAll
              />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
