"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { CallMetrics } from "@/types/call";
import { AlertCircle, CheckCircle, Clock, PhoneCall, PhoneOff, Percent } from "lucide-react";

interface MetricsOverviewProps {
  data: CallMetrics | undefined;
  isLoading: boolean;
  isError: boolean;
}

export function MetricsOverview({
  data,
  isLoading,
  isError,
}: MetricsOverviewProps) {
  // Loading state
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Array(6)
          .fill(0)
          .map((_, i) => (
            <Card key={i}>
              <CardHeader className="pb-2">
                <Skeleton className="h-4 w-24" />
              </CardHeader>
              <CardContent>
                <Skeleton className="h-10 w-20" />
                <Skeleton className="h-4 w-32 mt-2" />
              </CardContent>
            </Card>
          ))}
      </div>
    );
  }

  // Error state
  if (isError || !data) {
    return (
      <Card className="p-6">
        <div className="flex items-center space-x-2 text-red-500">
          <AlertCircle className="h-5 w-5" />
          <h3 className="font-medium">Error al cargar las métricas</h3>
        </div>
        <p className="text-muted-foreground mt-2">
          Ha ocurrido un error al cargar las métricas. Por favor, intenta de nuevo.
        </p>
      </Card>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {/* Total calls */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Total de llamadas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center">
            <PhoneCall className="h-5 w-5 mr-2 text-primary" />
            <div className="text-2xl font-bold">{data.total_calls}</div>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            En el período seleccionado
          </p>
        </CardContent>
      </Card>

      {/* Completed calls */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Llamadas completadas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 mr-2 text-green-500" />
            <div className="text-2xl font-bold">{data.completed_calls}</div>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Llamadas finalizadas correctamente
          </p>
        </CardContent>
      </Card>

      {/* Failed calls */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Llamadas fallidas
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center">
            <PhoneOff className="h-5 w-5 mr-2 text-red-500" />
            <div className="text-2xl font-bold">{data.failed_calls}</div>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Llamadas que no se completaron
          </p>
        </CardContent>
      </Card>

      {/* Success rate */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Tasa de éxito
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center">
            <Percent className="h-5 w-5 mr-2 text-blue-500" />
            <div className="text-2xl font-bold">{data.success_rate.toFixed(1)}%</div>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Porcentaje de llamadas completadas
          </p>
        </CardContent>
      </Card>

      {/* Average duration */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Duración promedio
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center">
            <Clock className="h-5 w-5 mr-2 text-yellow-500" />
            <div className="text-2xl font-bold">
              {data.avg_duration ? `${data.avg_duration.toFixed(0)}s` : "N/A"}
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Duración promedio de llamadas completadas
          </p>
        </CardContent>
      </Card>

      {/* Calls per day */}
      <Card>
        <CardHeader className="pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            Llamadas por día
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center">
            <PhoneCall className="h-5 w-5 mr-2 text-purple-500" />
            <div className="text-2xl font-bold">
              {data.timeline && data.timeline.length > 0
                ? (
                    data.total_calls / data.timeline.length
                  ).toFixed(1)
                : "0"}
            </div>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Promedio diario de llamadas
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
