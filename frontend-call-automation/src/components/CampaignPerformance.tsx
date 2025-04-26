"use client";

import { useEffect, useRef } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle } from "lucide-react";
import { Chart, registerables } from "chart.js";

// Register Chart.js components
Chart.register(...registerables);

interface CampaignData {
  id: string;
  name: string;
  status: string;
  total_calls: number;
  success_rate: number;
  avg_duration: number;
}

interface CampaignPerformanceProps {
  data: CampaignData[] | undefined;
  isLoading: boolean;
  isError: boolean;
}

export function CampaignPerformance({
  data,
  isLoading,
  isError,
}: CampaignPerformanceProps) {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  // Create or update chart
  useEffect(() => {
    if (isLoading || isError || !data || !chartRef.current) return;

    // Destroy existing chart
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    // Sort data by success rate
    const sortedData = [...data].sort((a, b) => b.success_rate - a.success_rate);

    // Prepare data
    const labels = sortedData.map((item) => item.name);
    const successRates = sortedData.map((item) => item.success_rate);
    const totalCalls = sortedData.map((item) => item.total_calls);

    // Create new chart
    const ctx = chartRef.current.getContext("2d");
    if (ctx) {
      chartInstance.current = new Chart(ctx, {
        type: "bar",
        data: {
          labels,
          datasets: [
            {
              label: "Tasa de éxito (%)",
              data: successRates,
              backgroundColor: "rgba(34, 197, 94, 0.7)", // green-500
              borderColor: "rgba(34, 197, 94, 1)",
              borderWidth: 1,
              yAxisID: "y",
            },
            {
              label: "Total de llamadas",
              data: totalCalls,
              backgroundColor: "rgba(59, 130, 246, 0.7)", // blue-500
              borderColor: "rgba(59, 130, 246, 1)",
              borderWidth: 1,
              type: "line",
              yAxisID: "y1",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: {
                display: false,
              },
            },
            y: {
              beginAtZero: true,
              position: "left",
              title: {
                display: true,
                text: "Tasa de éxito (%)",
              },
              max: 100,
            },
            y1: {
              beginAtZero: true,
              position: "right",
              title: {
                display: true,
                text: "Total de llamadas",
              },
              grid: {
                drawOnChartArea: false,
              },
            },
          },
          plugins: {
            legend: {
              position: "top",
              labels: {
                boxWidth: 12,
                padding: 15,
                font: {
                  size: 11,
                },
              },
            },
            tooltip: {
              mode: "index",
              intersect: false,
            },
          },
          interaction: {
            mode: "index",
            intersect: false,
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
    return <Skeleton className="h-[400px] w-full" />;
  }

  // Error state
  if (isError || !data) {
    return (
      <div className="flex items-center justify-center h-[400px] text-red-500">
        <AlertCircle className="h-5 w-5 mr-2" />
        <span>Error al cargar los datos</span>
      </div>
    );
  }

  // Empty state
  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-[400px] text-muted-foreground">
        <span>No hay campañas disponibles</span>
      </div>
    );
  }

  return (
    <div className="h-[400px] relative">
      <canvas ref={chartRef} />
    </div>
  );
}
