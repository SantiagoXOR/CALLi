"use client";

import { useState } from "react";
import { toast } from "sonner";
import { CallList } from "./CallList";
import { CallDetail } from "./CallDetail";
import { CallFilter } from "./CallFilter";

type ViewMode = "list" | "detail";

export function CallsView() {
  const [viewMode, setViewMode] = useState<ViewMode>("list");
  const [selectedCallId, setSelectedCallId] = useState<string | null>(null);
  const [filters, setFilters] = useState({});

  // Función para ver detalles de una llamada
  const handleViewCall = (callId: string) => {
    setSelectedCallId(callId);
    setViewMode("detail");
  };

  // Función para volver a la lista
  const handleBack = () => {
    setViewMode("list");
    setSelectedCallId(null);
  };

  // Función para aplicar filtros
  const handleApplyFilters = (newFilters: any) => {
    setFilters(newFilters);
    toast.success("Filtros aplicados");
  };

  // Función para cancelar una llamada
  const handleCancelCall = async (callId: string) => {
    try {
      // Aquí iría la lógica para cancelar la llamada
      toast.success("Llamada cancelada correctamente");
      
      // Si estamos en la vista de detalle, volvemos a la lista
      if (viewMode === "detail") {
        handleBack();
      }
    } catch (error) {
      toast.error("Error al cancelar la llamada");
      console.error("Error canceling call:", error);
    }
  };

  // Función para reprogramar una llamada
  const handleRescheduleCall = async (callId: string, scheduledTime: Date) => {
    try {
      // Aquí iría la lógica para reprogramar la llamada
      toast.success(`Llamada reprogramada para ${scheduledTime.toLocaleString()}`);
    } catch (error) {
      toast.error("Error al reprogramar la llamada");
      console.error("Error rescheduling call:", error);
    }
  };

  return (
    <div className="container mx-auto py-6 space-y-6">
      {viewMode === "list" && (
        <>
          <CallFilter onApplyFilters={handleApplyFilters} />
          <CallList 
            filters={filters}
            onViewCall={handleViewCall}
            onCancelCall={handleCancelCall}
            onRescheduleCall={handleRescheduleCall}
          />
        </>
      )}

      {viewMode === "detail" && selectedCallId && (
        <CallDetail
          callId={selectedCallId}
          onBack={handleBack}
          onCancelCall={handleCancelCall}
          onRescheduleCall={handleRescheduleCall}
        />
      )}
    </div>
  );
}
