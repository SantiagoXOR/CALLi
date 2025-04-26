"use client";

import { useState } from "react";
import { useGetCallDetail } from "@/services/callService";
import { CallStatus } from "@/types/call";
import { formatDistanceToNow, format } from "date-fns";
import { es } from "date-fns/locale";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
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
  ArrowLeft,
  Calendar,
  Clock,
  FileAudio,
  MessageSquare,
  PhoneCall,
  PhoneOff,
  RefreshCw,
  User,
} from "lucide-react";
import { DateTimePicker } from "./DateTimePicker";
import { CallTranscript } from "./CallTranscript";

interface CallDetailProps {
  callId: string;
  onBack: () => void;
  onCancelCall: (callId: string) => void;
  onRescheduleCall: (callId: string, scheduledTime: Date) => void;
}

export function CallDetail({
  callId,
  onBack,
  onCancelCall,
  onRescheduleCall,
}: CallDetailProps) {
  const [scheduledTime, setScheduledTime] = useState<Date>(
    new Date(Date.now() + 3600000) // Default to 1 hour from now
  );
  const [isRescheduleDialogOpen, setIsRescheduleDialogOpen] = useState(false);

  // Fetch call details
  const { data: call, isLoading, isError } = useGetCallDetail(callId);

  // Handle reschedule
  const handleReschedule = () => {
    onRescheduleCall(callId, scheduledTime);
    setIsRescheduleDialogOpen(false);
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
      <Badge variant={config.variant as any} className="ml-2">
        {config.label}
      </Badge>
    );
  };

  // Loading state
  if (isLoading) {
    return (
      <Card>
        <CardHeader className="pb-4">
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="sm"
              className="mr-2"
              onClick={onBack}
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Volver
            </Button>
            <Skeleton className="h-6 w-48" />
          </div>
        </CardHeader>
        <CardContent className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-8 w-full" />
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-8 w-full" />
            </div>
            <div className="space-y-4">
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-8 w-full" />
              <Skeleton className="h-4 w-24" />
              <Skeleton className="h-8 w-full" />
            </div>
          </div>
          <div>
            <Skeleton className="h-4 w-32 mb-4" />
            <Skeleton className="h-32 w-full" />
          </div>
        </CardContent>
      </Card>
    );
  }

  // Error state
  if (isError || !call) {
    return (
      <Card>
        <CardHeader>
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="sm"
              className="mr-2"
              onClick={onBack}
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Volver
            </Button>
            <CardTitle>Error al cargar los detalles</CardTitle>
          </div>
          <CardDescription>
            No se pudieron cargar los detalles de la llamada
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center py-8">
          <p className="text-muted-foreground mb-4">
            Ha ocurrido un error al cargar los detalles de la llamada. Por favor, intenta de nuevo.
          </p>
          <Button
            variant="outline"
            onClick={() => window.location.reload()}
          >
            Reintentar
          </Button>
        </CardContent>
      </Card>
    );
  }

  const canCancel =
    call.status === CallStatus.QUEUED ||
    call.status === CallStatus.RINGING ||
    call.status === CallStatus.IN_PROGRESS;

  const canReschedule = canCancel;

  const createdAt = new Date(call.created_at);
  const updatedAt = new Date(call.updated_at);

  return (
    <Card>
      <CardHeader className="pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="sm"
              className="mr-2"
              onClick={onBack}
            >
              <ArrowLeft className="h-4 w-4 mr-1" />
              Volver
            </Button>
            <div>
              <CardTitle className="flex items-center">
                Detalles de la llamada
                {renderStatusBadge(call.status)}
              </CardTitle>
              <CardDescription>
                ID: {call.id}
              </CardDescription>
            </div>
          </div>
          <div className="flex space-x-2">
            {canCancel && (
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-red-500 hover:text-red-600"
                  >
                    <PhoneOff className="h-4 w-4 mr-2" />
                    Cancelar
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
            )}

            {canReschedule && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsRescheduleDialogOpen(true)}
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Reprogramar
              </Button>
            )}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-8">
        {/* Call information */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-1">
                Contacto
              </h3>
              <div className="flex items-center">
                <User className="h-4 w-4 mr-2 text-muted-foreground" />
                <span>{call.contact_name || "Desconocido"}</span>
              </div>
              <div className="text-sm text-muted-foreground mt-1">
                {call.phone_number}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-1">
                Campaña
              </h3>
              <div>{call.campaign_name || "N/A"}</div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-1">
                Duración
              </h3>
              <div className="flex items-center">
                <Clock className="h-4 w-4 mr-2 text-muted-foreground" />
                <span>
                  {call.duration ? `${call.duration} segundos` : "N/A"}
                </span>
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-1">
                Fecha de creación
              </h3>
              <div className="flex items-center">
                <Calendar className="h-4 w-4 mr-2 text-muted-foreground" />
                <span>{format(createdAt, "PPP 'a las' p", { locale: es })}</span>
              </div>
              <div className="text-sm text-muted-foreground mt-1">
                {formatDistanceToNow(createdAt, { addSuffix: true, locale: es })}
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-1">
                Última actualización
              </h3>
              <div className="flex items-center">
                <RefreshCw className="h-4 w-4 mr-2 text-muted-foreground" />
                <span>{format(updatedAt, "PPP 'a las' p", { locale: es })}</span>
              </div>
              <div className="text-sm text-muted-foreground mt-1">
                {formatDistanceToNow(updatedAt, { addSuffix: true, locale: es })}
              </div>
            </div>

            {call.error_message && (
              <div>
                <h3 className="text-sm font-medium text-red-500 mb-1">
                  Error
                </h3>
                <div className="text-sm text-red-500 bg-red-50 p-2 rounded border border-red-100">
                  {call.error_message}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Tabs for transcript and recordings */}
        <Tabs defaultValue="transcript" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="transcript" className="flex items-center">
              <MessageSquare className="h-4 w-4 mr-2" />
              Transcripción
            </TabsTrigger>
            <TabsTrigger value="recordings" className="flex items-center">
              <FileAudio className="h-4 w-4 mr-2" />
              Grabaciones
            </TabsTrigger>
          </TabsList>
          <TabsContent value="transcript" className="mt-4">
            {call.transcript ? (
              <CallTranscript transcript={call.transcript} />
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <MessageSquare className="h-12 w-12 mx-auto mb-4 opacity-20" />
                <p>No hay transcripción disponible para esta llamada.</p>
              </div>
            )}
          </TabsContent>
          <TabsContent value="recordings" className="mt-4">
            {call.recording_url ? (
              <div className="p-4 border rounded-md">
                <h3 className="text-sm font-medium mb-2">Grabación de la llamada</h3>
                <audio
                  controls
                  className="w-full"
                  src={call.recording_url}
                >
                  Tu navegador no soporta el elemento de audio.
                </audio>
                <div className="mt-2 text-right">
                  <a
                    href={call.recording_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-500 hover:underline"
                  >
                    Descargar grabación
                  </a>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <FileAudio className="h-12 w-12 mx-auto mb-4 opacity-20" />
                <p>No hay grabaciones disponibles para esta llamada.</p>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>

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
    </Card>
  );
}
