"use client";

import { useEffect, useRef } from "react";
import { CallStatus } from "@/types/call";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle } from "lucide-react";
import { Chart, registerables } from "chart.js";

// Register Chart.js components
Chart.register(...registerables);

interface CallStatusDistributionProps {
  data: Record<CallStatus, number> | undefined;
  isLoading: boolean;
  isError: boolean;
}

export function CallStatusDistribution({
  data,
  isLoading,
  isError,
}: CallStatusDistributionProps) {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  // Status colors
  const statusColors = {
    [CallStatus.QUEUED]: "#94a3b8", // slate-400
    [CallStatus.RINGING]: "#fbbf24", // amber-400
    [CallStatus.IN_PROGRESS]: "#3b82f6", // blue-500
    [CallStatus.COMPLETED]: "#22c55e", // green-500
    [CallStatus.FAILED]: "#ef4444", // red-500
    [CallStatus.CANCELLED]: "#6b7280", // gray-500
    [CallStatus.UNKNOWN]: "#d1d5db", // gray-300
  };

  // Status labels
  const statusLabels = {
    [CallStatus.QUEUED]: "En cola",
    [CallStatus.RINGING]: "Sonando",
    [CallStatus.IN_PROGRESS]: "En progreso",
    [CallStatus.COMPLETED]: "Completada",
    [CallStatus.FAILED]: "Fallida",
    [CallStatus.CANCELLED]: "Cancelada",
    [CallStatus.UNKNOWN]: "Desconocido",
  };

  // Create or update chart
  useEffect(() => {
    if (isLoading || isError || !data || !chartRef.current) return;

    // Destroy existing chart
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    // Prepare data
    const labels = Object.keys(data).map(
      (key) => statusLabels[key as CallStatus] || key
    );
    const values = Object.values(data);
    const backgroundColor = Object.keys(data).map(
      (key) => statusColors[key as CallStatus] || "#d1d5db"
    );

    // Create new chart
    const ctx = chartRef.current.getContext("2d");
    if (ctx) {
      chartInstance.current = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels,
          datasets: [
            {
              data: values,
              backgroundColor,
              borderWidth: 1,
              borderColor: "#ffffff",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "right",
              labels: {
                boxWidth: 12,
                padding: 15,
                font: {
                  size: 11,
                },
              },
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const label = context.label || "";
                  const value = context.raw as number;
                  const total = values.reduce((a, b) => a + b, 0);
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${label}: ${value} (${percentage}%)`;
                },
              },
            },
          },
        },
      });
    }

    // Cleanup
    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
        chartInstance.current = null;
      }
    };
  }, [data, isLoading, isError]);

  // Loading state
  if (isLoading) {
    return <Skeleton className="h-[300px] w-full" />;
  }

  // Error state
  if (isError || !data) {
    return (
      <div className="flex items-center justify-center h-[300px] text-red-500">
        <AlertCircle className="h-5 w-5 mr-2" />
        <span>Error al cargar los datos</span>
      </div>
    );
  }

  // Empty state
  const total = Object.values(data).reduce((a, b) => a + b, 0);
  if (total === 0) {
    return (
      <div className="flex items-center justify-center h-[300px] text-muted-foreground">
        <span>No hay datos disponibles</span>
      </div>
    );
  }

  return (
    <div className="h-[300px] relative">
      <canvas ref={chartRef} />
    </div>
  );
}
