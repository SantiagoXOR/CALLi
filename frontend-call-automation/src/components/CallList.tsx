"use client";

import { useState } from "react";
import { useGetCalls } from "@/services/callService";
import { Call, CallStatus } from "@/types/call";
import { formatDistanceToNow } from "date-fns";
import { es } from "date-fns/locale";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import {
  Calendar,
  Clock,
  Eye,
  Phone,
  PhoneOff,
  RefreshCw,
  User,
} from "lucide-react";
import { DateTimePicker } from "./DateTimePicker";

interface CallListProps {
  filters: any;
  onViewCall: (callId: string) => void;
  onCancelCall: (callId: string) => void;
  onRescheduleCall: (callId: string, scheduledTime: Date) => void;
}

export function CallList({
  filters,
  onViewCall,
  onCancelCall,
  onRescheduleCall,
}: CallListProps) {
  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);
  const [callToReschedule, setCallToReschedule] = useState<string | null>(null);
  const [scheduledTime, setScheduledTime] = useState<Date>(
    new Date(Date.now() + 3600000) // Default to 1 hour from now
  );
  const [isRescheduleDialogOpen, setIsRescheduleDialogOpen] = useState(false);

  // Fetch calls data
  const { data, isLoading, isError } = useGetCalls(page, pageSize, filters);

  const calls = data?.data || [];
  const totalPages = data?.total_pages || 1;

  // Handle pagination
  const handlePageChange = (newPage: number) => {
    if (newPage > 0 && newPage <= totalPages) {
      setPage(newPage);
    }
  };

  // Open reschedule dialog
  const openRescheduleDialog = (callId: string) => {
    setCallToReschedule(callId);
    setIsRescheduleDialogOpen(true);
  };

  // Handle reschedule
  const handleReschedule = () => {
    if (callToReschedule) {
      onRescheduleCall(callToReschedule, scheduledTime);
      setIsRescheduleDialogOpen(false);
      setCallToReschedule(null);
    }
  };

  // Render status badge
  const renderStatusBadge = (status: CallStatus) => {
    const statusConfig = {
      [CallStatus.QUEUED]: { label: "En cola", variant: "secondary" },
      [CallStatus.RINGING]: { label: "Sonando", variant: "warning" },
      [CallStatus.IN_PROGRESS]: { label: "En progreso", variant: "default" },
      [CallStatus.COMPLETED]: { label: "Completada", variant: "success" },
      [CallStatus.FAILED]: { label: "Fallida", variant: "destructive" },
      [CallStatus.CANCELLED]: { label: "Cancelada", variant: "outline" },
      [CallStatus.UNKNOWN]: { label: "Desconocido", variant: "outline" },
    };

    const config = statusConfig[status] || statusConfig[CallStatus.UNKNOWN];

    return (
      <Badge variant={config.variant as any}>{config.label}</Badge>
    );
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold">Llamadas</h2>
        </div>
        <div className="border rounded-lg">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Contacto</TableHead>
                <TableHead>Estado</TableHead>
                <TableHead>Fecha</TableHead>
                <TableHead>Duración</TableHead>
                <TableHead>Acciones</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {Array(5)
                .fill(0)
                .map((_, i) => (
                  <TableRow key={i}>
                    <TableCell>
                      <Skeleton className="h-4 w-24" />
                    </TableCell>
                    <TableCell>
                      <Skeleton className="h-4 w-32" />
                    </TableCell>
                    <TableCell>
                      <Skeleton className="h-6 w-20" />
                    </TableCell>
                    <TableCell>
                      <Skeleton className="h-4 w-28" />
                    </TableCell>
                    <TableCell>
                      <Skeleton className="h-4 w-16" />
                    </TableCell>
                    <TableCell>
                      <div className="flex space-x-2">
                        <Skeleton className="h-8 w-8" />
                        <Skeleton className="h-8 w-8" />
                        <Skeleton className="h-8 w-8" />
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </div>
      </div>
    );
  }

  // Error state
  if (isError) {
    return (
      <div className="p-8 text-center">
        <h3 className="text-lg font-medium">Error al cargar las llamadas</h3>
        <p className="text-muted-foreground mt-2">
          Ha ocurrido un error al cargar las llamadas. Por favor, intenta de nuevo.
        </p>
        <Button
          variant="outline"
          className="mt-4"
          onClick={() => window.location.reload()}
        >
          Reintentar
        </Button>
      </div>
    );
  }

  // Empty state
  if (calls.length === 0) {
    return (
      <div className="p-8 text-center border rounded-lg">
        <Phone className="mx-auto h-12 w-12 text-muted-foreground" />
        <h3 className="text-lg font-medium mt-4">No hay llamadas</h3>
        <p className="text-muted-foreground mt-2">
          No se encontraron llamadas con los filtros actuales.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Llamadas</h2>
        <div className="text-sm text-muted-foreground">
          Mostrando {calls.length} de {data?.total || 0} llamadas
        </div>
      </div>

      <div className="border rounded-lg">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>ID</TableHead>
              <TableHead>Contacto</TableHead>
              <TableHead>Estado</TableHead>
              <TableHead>Fecha</TableHead>
              <TableHead>Duración</TableHead>
              <TableHead>Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {calls.map((call: Call) => (
              <TableRow key={call.id}>
                <TableCell className="font-mono text-xs">
                  {call.id.substring(0, 8)}...
                </TableCell>
                <TableCell>
                  <div className="flex items-center">
                    <User className="h-4 w-4 mr-2 text-muted-foreground" />
                    <span>{call.phone_number}</span>
                  </div>
                </TableCell>
                <TableCell>{renderStatusBadge(call.status)}</TableCell>
                <TableCell>
                  <div className="flex flex-col">
                    <span className="text-xs text-muted-foreground">
                      <Calendar className="h-3 w-3 inline mr-1" />
                      {new Date(call.created_at).toLocaleDateString()}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      <Clock className="h-3 w-3 inline mr-1" />
                      {new Date(call.created_at).toLocaleTimeString()}
                    </span>
                  </div>
                </TableCell>
                <TableCell>
                  {call.duration ? `${call.duration}s` : "-"}
                </TableCell>
                <TableCell>
                  <div className="flex space-x-2">
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => onViewCall(call.id)}
                      title="Ver detalles"
                    >
                      <Eye className="h-4 w-4" />
                    </Button>

                    {(call.status === CallStatus.QUEUED ||
                      call.status === CallStatus.RINGING ||
                      call.status === CallStatus.IN_PROGRESS) && (
                      <>
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <Button
                              variant="outline"
                              size="icon"
                              className="text-red-500 hover:text-red-600"
                              title="Cancelar llamada"
                            >
                              <PhoneOff className="h-4 w-4" />
                            </Button>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>
                                ¿Cancelar esta llamada?
                              </AlertDialogTitle>
                              <AlertDialogDescription>
                                Esta acción no se puede deshacer. La llamada será
                                cancelada inmediatamente.
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel>Cancelar</AlertDialogCancel>
                              <AlertDialogAction
                                onClick={() => onCancelCall(call.id)}
                                className="bg-red-500 hover:bg-red-600"
                              >
                                Confirmar
                              </AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>

                        <Button
                          variant="outline"
                          size="icon"
                          onClick={() => openRescheduleDialog(call.id)}
                          title="Reprogramar llamada"
                        >
                          <RefreshCw className="h-4 w-4" />
                        </Button>
                      </>
                    )}
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <Pagination className="mt-4">
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                onClick={() => handlePageChange(page - 1)}
                className={page === 1 ? "pointer-events-none opacity-50" : ""}
              />
            </PaginationItem>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map(
              (pageNum) => (
                <PaginationItem key={pageNum}>
                  <PaginationLink
                    isActive={pageNum === page}
                    onClick={() => handlePageChange(pageNum)}
                  >
                    {pageNum}
                  </PaginationLink>
                </PaginationItem>
              )
            )}
            <PaginationItem>
              <PaginationNext
                onClick={() => handlePageChange(page + 1)}
                className={
                  page === totalPages ? "pointer-events-none opacity-50" : ""
                }
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      )}

      {/* Reschedule Dialog */}
      <AlertDialog
        open={isRescheduleDialogOpen}
        onOpenChange={setIsRescheduleDialogOpen}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Reprogramar llamada</AlertDialogTitle>
            <AlertDialogDescription>
              Selecciona la nueva fecha y hora para la llamada.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <div className="py-4">
            <DateTimePicker
              date={scheduledTime}
              setDate={setScheduledTime}
              showTimePicker
            />
          </div>
          <AlertDialogFooter>
            <AlertDialogCancel
              onClick={() => {
                setIsRescheduleDialogOpen(false);
                setCallToReschedule(null);
              }}
            >
              Cancelar
            </AlertDialogCancel>
            <AlertDialogAction onClick={handleReschedule}>
              Reprogramar
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
