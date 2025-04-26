"use client";

import { useEffect, useRef } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { AlertCircle } from "lucide-react";
import { Chart, registerables } from "chart.js";
import { format, parseISO } from "date-fns";
import { es } from "date-fns/locale";

// Register Chart.js components
Chart.register(...registerables);

interface TimelineData {
  date: string;
  total: number;
  completed: number;
  failed: number;
}

interface CallTimelineProps {
  data: TimelineData[] | undefined;
  isLoading: boolean;
  isError: boolean;
  showAll?: boolean;
}

export function CallTimeline({
  data,
  isLoading,
  isError,
  showAll = false,
}: CallTimelineProps) {
  const chartRef = useRef<HTMLCanvasElement>(null);
  const chartInstance = useRef<Chart | null>(null);

  // Create or update chart
  useEffect(() => {
    if (isLoading || isError || !data || !chartRef.current) return;

    // Destroy existing chart
    if (chartInstance.current) {
      chartInstance.current.destroy();
    }

    // Format dates
    const labels = data.map((item) => {
      const date = parseISO(item.date);
      return format(date, "d MMM", { locale: es });
    });

    // Create new chart
    const ctx = chartRef.current.getContext("2d");
    if (ctx) {
      chartInstance.current = new Chart(ctx, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Total",
              data: data.map((item) => item.total),
              borderColor: "#3b82f6", // blue-500
              backgroundColor: "rgba(59, 130, 246, 0.1)",
              borderWidth: 2,
              tension: 0.3,
              fill: true,
            },
            {
              label: "Completadas",
              data: data.map((item) => item.completed),
              borderColor: "#22c55e", // green-500
              backgroundColor: "rgba(34, 197, 94, 0.1)",
              borderWidth: 2,
              tension: 0.3,
              fill: true,
            },
            {
              label: "Fallidas",
              data: data.map((item) => item.failed),
              borderColor: "#ef4444", // red-500
              backgroundColor: "rgba(239, 68, 68, 0.1)",
              borderWidth: 2,
              tension: 0.3,
              fill: true,
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
              ticks: {
                precision: 0,
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
            mode: "nearest",
            axis: "x",
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
    return <Skeleton className="h-full w-full min-h-[300px]" />;
  }

  // Error state
  if (isError || !data) {
    return (
      <div className="flex items-center justify-center h-full min-h-[300px] text-red-500">
        <AlertCircle className="h-5 w-5 mr-2" />
        <span>Error al cargar los datos</span>
      </div>
    );
  }

  // Empty state
  if (data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full min-h-[300px] text-muted-foreground">
        <span>No hay datos disponibles</span>
      </div>
    );
  }

  return (
    <div className="h-full min-h-[300px] relative">
      <canvas ref={chartRef} />
    </div>
  );
}
