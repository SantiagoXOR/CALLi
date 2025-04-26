"use client";

import {
  Bot,
  Headphones,
  Pause,
  Play,
  Search,
  Settings,
  Square,
} from "lucide-react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

// Re-definimos tipos necesarios aquí o los importamos desde un archivo centralizado
type EstadoLlamada =
  | "pendiente"
  | "marcando"
  | "en-llamada"
  | "sin-respuesta"
  | "completada"
  | "buzon-voz"
  | "pausada"
  | "transferida"
  | "error"
  | "agendada";
type EstadoAgente =
  | "inactivo"
  | "marcando"
  | "en-llamada"
  | "pausado"
  | "error"
  | "transferida";
type EstadoCampaña =
  | "Borrador"
  | "Activa"
  | "Pausada"
  | "Completada"
  | "Archivada"; // Necesario para Campaña
interface Cliente {
  id: number | string;
  nombre: string;
  telefono?: string;
  intentos: number;
  estado: EstadoLlamada;
  ultimoIntento: string | null;
  duracion?: string;
  origen?: string;
  notas?: string;
}
interface Campaña {
  id: number | string;
  nombre: string;
  descripcion?: string;
  estado: EstadoCampaña;
  fechaInicio: string | null;
  fechaFin: string | null;
  horarioLlamadas?: string;
  progreso?: number;
  totalClientes?: number;
  clientesCompletados?: number;
  listaContactosIds?: (number | string)[];
  script?: string;
  maxReintentos?: number;
  delayReintentos?: number;
}
interface Agente {
  id: number | string;
  nombre: string;
  avatar: string;
  tipo?: "IA" | "Humano";
  estado?: string;
  rendimiento?: number;
}

// =========================================================================
// --- Subcomponente: Vista del Dashboard Operativo ---
// =========================================================================
interface DashboardViewProps {
  estadoAgenteIA: EstadoAgente;
  clienteActualIA: Cliente | null;
  tiempoLlamadaMostrado: string;
  clientes: Cliente[];
  agentes: Agente[];
  campañas: Campaña[];
  campañaActivaIA: Campaña | null;
  busquedaCliente: string;
  setBusquedaCliente: (value: string) => void;
  iniciarLlamadaIA: () => void;
  pausarLlamadaIA: () => void;
  detenerLlamadaIA: () => void;
  tomarLlamadaIA: () => void;
  seleccionarCampañaParaIA: (campaña: Campaña) => void;
}

function DashboardView({
  estadoAgenteIA,
  clienteActualIA,
  tiempoLlamadaMostrado,
  clientes,
  agentes,
  campañas,
  campañaActivaIA,
  busquedaCliente,
  setBusquedaCliente,
  iniciarLlamadaIA,
  pausarLlamadaIA,
  detenerLlamadaIA,
  tomarLlamadaIA,
  seleccionarCampañaParaIA,
}: DashboardViewProps): JSX.Element {
  // Filtra clientes para la tabla del dashboard
  const clientesFiltradosDashboard = clientes.filter(
    (cliente) =>
      cliente.nombre.toLowerCase().includes(busquedaCliente.toLowerCase()) ||
      (cliente.telefono && cliente.telefono.includes(busquedaCliente)) ||
      cliente.estado.toLowerCase().includes(busquedaCliente.toLowerCase())
  );

  // Función auxiliar para colores de estado de cliente
  const obtenerColorEstadoCliente = (estado: EstadoLlamada): string => {
    switch (estado) {
      case "completada":
        return "bg-green-100 text-green-800 border border-green-200";
      case "en-llamada":
        return "bg-blue-100 text-blue-800 border border-blue-200 animate-pulse";
      case "pendiente":
        return "bg-yellow-100 text-yellow-800 border border-yellow-200";
      case "transferida":
        return "bg-purple-100 text-purple-800 border border-purple-200";
      case "sin-respuesta":
        return "bg-red-100 text-red-800 border border-red-200";
      case "buzon-voz":
        return "bg-gray-200 text-gray-600 border border-gray-300"; // Ajustado color
      default:
        return "bg-gray-100 text-gray-800 border border-gray-200";
    }
  };

  return (
    // Layout del Dashboard: 3 columnas flexibles en pantallas grandes
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
      {/* Columna 1: Estado Agente IA (Ahora como Card estándar) */}
      <Card className="lg:col-span-1 flex flex-col bg-white shadow">
        {" "}
        {/* Fondo blanco estándar */}
        <CardHeader className="border-b h-16 flex flex-row items-center justify-between">
          <CardTitle className="text-base font-semibold">
            Estado Agente IA
          </CardTitle>
          {/* Indicador de conexión (puede ser más sofisticado) */}
          <div className="flex items-center gap-1.5">
            <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
            <span className="text-xs text-gray-500">Online</span>
          </div>
        </CardHeader>
        <CardContent className="flex-1 flex flex-col items-center justify-center p-4 relative text-center">
          {/* Visualizador (simplificado con icono) */}
          <div
            className={`relative w-28 h-28 flex items-center justify-center rounded-full border-4 p-1 mb-4 ${
              estadoAgenteIA === "inactivo"
                ? "border-gray-300"
                : estadoAgenteIA === "marcando"
                ? "border-yellow-400"
                : estadoAgenteIA === "en-llamada"
                ? "border-blue-500 animate-pulse"
                : estadoAgenteIA === "pausado"
                ? "border-orange-400"
                : estadoAgenteIA === "transferida"
                ? "border-purple-500"
                : "border-red-500"
            }`}
          >
            <div className="bg-gray-100 rounded-full w-full h-full flex flex-col items-center justify-center">
              {estadoAgenteIA === "inactivo" && (
                <Bot size={32} className="text-gray-400" />
              )}
              {estadoAgenteIA === "marcando" && (
                <Bot size={32} className="text-yellow-500 animate-ping" />
              )}
              {estadoAgenteIA === "en-llamada" && (
                <Bot size={32} className="text-blue-500" />
              )}
              {estadoAgenteIA === "pausado" && (
                <Pause size={32} className="text-orange-500" />
              )}
              {estadoAgenteIA === "transferida" && (
                <Headphones size={32} className="text-purple-500" />
              )}
              {estadoAgenteIA === "error" && (
                <Bot size={32} className="text-red-500" />
              )}
            </div>
          </div>
          {/* Texto Estado */}
          <div
            className={`text-lg font-semibold mb-2 ${
              estadoAgenteIA === "error" ? "text-red-600" : "text-gray-800"
            }`}
          >
            {estadoAgenteIA === "inactivo" && "Inactivo"}
            {estadoAgenteIA === "marcando" && "Marcando..."}
            {estadoAgenteIA === "en-llamada" && "En Llamada"}
            {estadoAgenteIA === "pausado" && "Pausado"}
            {estadoAgenteIA === "transferida" && "Llamada Transferida"}
            {estadoAgenteIA === "error" && "Error"}
          </div>
          {/* Info Campaña Activa IA */}
          <div
            className="text-xs text-gray-500 mb-2 h-4 truncate"
            title={
              campañaActivaIA
                ? `Campaña: ${campañaActivaIA.nombre}`
                : "Ninguna campaña activa"
            }
          >
            {campañaActivaIA
              ? `Campaña: ${campañaActivaIA.nombre}`
              : "Ninguna campaña activa"}
          </div>
          {/* Info Llamada Activa IA */}
          {clienteActualIA &&
            (estadoAgenteIA === "en-llamada" ||
              estadoAgenteIA === "transferida") && (
              <div className="text-center w-full px-2 mb-3 border-t pt-3 mt-2">
                <div className="text-xs text-gray-500 uppercase tracking-wide">
                  Llamada{" "}
                  {estadoAgenteIA === "transferida" ? "transferida" : "activa"}
                </div>
                <div
                  className="font-medium text-base truncate mt-1"
                  title={clienteActualIA.nombre}
                >
                  {clienteActualIA.nombre}
                </div>
                <div className="text-lg font-mono mt-1 text-blue-600">
                  {tiempoLlamadaMostrado}
                </div>
                {estadoAgenteIA === "en-llamada" && (
                  <Button
                    variant="outline"
                    size="sm"
                    className="mt-2 bg-purple-100 border-purple-300 text-purple-700 hover:bg-purple-200 w-full"
                    onClick={tomarLlamadaIA}
                  >
                    <Headphones className="h-3 w-3 mr-1" /> Tomar Llamada
                  </Button>
                )}
              </div>
            )}
          {/* Controles Principales IA */}
          <div className="w-full flex justify-center items-center gap-4 mt-auto pt-4">
            {" "}
            {/* Empuja controles abajo */}
            <TooltipProvider delayDuration={100}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="outline"
                    size="lg"
                    className={`rounded-full h-12 w-12 flex items-center justify-center ${
                      (estadoAgenteIA === "inactivo" ||
                        estadoAgenteIA === "pausado") &&
                      campañaActivaIA
                        ? "bg-green-100 border-green-300 text-green-700 hover:bg-green-200"
                        : "bg-gray-200 text-gray-400 cursor-not-allowed border-gray-300"
                    }`}
                    onClick={iniciarLlamadaIA}
                    disabled={
                      !campañaActivaIA ||
                      estadoAgenteIA === "en-llamada" ||
                      estadoAgenteIA === "marcando" ||
                      estadoAgenteIA === "transferida"
                    }
                  >
                    {" "}
                    <Play className="h-5 w-5" />{" "}
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>{estadoAgenteIA === "pausado" ? "Reanudar" : "Iniciar"}</p>
                </TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="outline"
                    size="lg"
                    className={`rounded-full h-12 w-12 flex items-center justify-center ${
                      estadoAgenteIA === "en-llamada" ||
                      estadoAgenteIA === "marcando"
                        ? "bg-orange-100 border-orange-300 text-orange-700 hover:bg-orange-200"
                        : "bg-gray-200 text-gray-400 cursor-not-allowed border-gray-300"
                    }`}
                    onClick={pausarLlamadaIA}
                    disabled={
                      estadoAgenteIA !== "en-llamada" &&
                      estadoAgenteIA !== "marcando"
                    }
                  >
                    {" "}
                    <Pause className="h-5 w-5" />{" "}
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Pausar</p>
                </TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="outline"
                    size="lg"
                    className={`rounded-full h-12 w-12 flex items-center justify-center ${
                      estadoAgenteIA !== "inactivo" &&
                      estadoAgenteIA !== "transferida"
                        ? "bg-red-100 border-red-300 text-red-700 hover:bg-red-200"
                        : "bg-gray-200 text-gray-400 cursor-not-allowed border-gray-300"
                    }`}
                    onClick={detenerLlamadaIA}
                    disabled={
                      estadoAgenteIA === "inactivo" ||
                      estadoAgenteIA === "transferida"
                    }
                  >
                    {" "}
                    <Square className="h-5 w-5" />{" "}
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Detener</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>
        </CardContent>
        <CardFooter className="p-4 border-t">
          <Button
            variant="ghost"
            className="w-full justify-start text-gray-500 hover:text-gray-700 hover:bg-gray-100"
          >
            <Settings className="h-4 w-4 mr-2" />
            <span>Configurar Agente IA</span>
          </Button>
        </CardFooter>
      </Card>

      {/* Columna 2: Lista Clientes */}
      <Card className="lg:col-span-1 flex flex-col shadow">
        <CardHeader className="h-16 flex flex-row items-center justify-between border-b">
          <CardTitle className="text-base font-semibold">
            Clientes Potenciales
          </CardTitle>
          {/* Podrían ir filtros aquí */}
        </CardHeader>
        <CardContent className="p-0 flex-1 flex flex-col">
          {/* Barra de búsqueda */}
          <div className="p-4 border-b">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Buscar cliente en dashboard..."
                className="pl-9"
                value={busquedaCliente}
                onChange={(e) => setBusquedaCliente(e.target.value)}
              />
            </div>
          </div>
          {/* Tabla */}
          <div className="flex-1 overflow-auto">
            {" "}
            {/* Scroll para la tabla */}
            <Table className="text-sm">
              <TableHeader className="sticky top-0 bg-gray-100 z-10">
                <TableRow>
                  <TableHead className="p-2 pl-4 w-2/5">Nombre</TableHead>
                  <TableHead className="p-2 w-1/4">Estado</TableHead>
                  <TableHead className="p-2 w-1/4 pr-4">Últ. Intento</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {clientesFiltradosDashboard.length > 0 ? (
                  clientesFiltradosDashboard.map((cliente) => (
                    <TableRow
                      key={cliente.id}
                      className={`hover:bg-gray-50 ${
                        cliente.estado === "en-llamada"
                          ? "bg-blue-50 font-medium"
                          : ""
                      }`}
                    >
                      <TableCell className="p-2 pl-4">
                        <div className="flex items-center gap-2">
                          {/* Indicador de estado visual */}
                          <div
                            className={`h-2 w-2 rounded-full flex-shrink-0 border ${
                              cliente.estado === "completada"
                                ? "bg-green-500 border-green-500"
                                : cliente.estado === "en-llamada"
                                ? "bg-blue-500 border-blue-500 animate-pulse"
                                : cliente.estado === "pendiente"
                                ? "bg-yellow-500 border-yellow-500"
                                : cliente.estado === "transferida"
                                ? "bg-purple-500 border-purple-500"
                                : cliente.estado === "sin-respuesta"
                                ? "bg-red-500 border-red-500"
                                : "bg-gray-400 border-gray-400"
                            }`}
                          ></div>
                          <span className="truncate">{cliente.nombre}</span>
                        </div>
                      </TableCell>
                      <TableCell className="p-2">
                        <Badge
                          variant="outline"
                          className={`text-xs ${obtenerColorEstadoCliente(
                            cliente.estado
                          )}`}
                        >
                          {cliente.estado}
                        </Badge>
                      </TableCell>
                      <TableCell className="p-2 pr-4 text-gray-600 text-xs">
                        {cliente.ultimoIntento || "-"}
                      </TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell
                      colSpan={3}
                      className="text-center p-6 text-gray-500"
                    >
                      No se encontraron clientes.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {/* Columna 3: Campañas y Agentes */}
      <Card className="lg:col-span-1 flex flex-col shadow">
        {/* Sección Selección Campaña IA */}
        <CardHeader className="h-16 border-b">
          <CardTitle className="text-base font-semibold">
            Seleccionar Campaña IA
          </CardTitle>
        </CardHeader>
        <CardContent className="p-4 border-b">
          {/* Lista scrollable de campañas */}
          <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
            {campañas
              .filter(
                (c) =>
                  c.estado === "Activa" ||
                  c.estado === "Pausada" ||
                  c.estado === "Borrador"
              )
              .map((campaña) => (
                <Card
                  key={campaña.id}
                  className={`border rounded-lg cursor-pointer hover:shadow-sm transition-shadow text-xs ${
                    campañaActivaIA?.id === campaña.id
                      ? "bg-blue-50 border-blue-300 ring-1 ring-blue-300"
                      : "bg-white hover:bg-gray-50"
                  }`}
                  onClick={() => seleccionarCampañaParaIA(campaña)}
                >
                  <CardContent className="p-2">
                    <div className="font-medium truncate mb-1">
                      {campaña.nombre}
                    </div>
                    <div className="flex justify-between items-center text-gray-500">
                      <Badge
                        variant={
                          campaña.estado === "Activa" ? "default" : "outline"
                        }
                        className={`text-[10px] px-1.5 py-0 ${
                          campaña.estado === "Activa"
                            ? "bg-green-100 text-green-800 border-green-200"
                            : campaña.estado === "Pausada"
                            ? "bg-orange-100 text-orange-800 border-orange-200"
                            : "bg-gray-100 text-gray-800 border-gray-200"
                        }`}
                      >
                        {campaña.estado}
                      </Badge>
                      <span>{campaña.progreso ?? 0}%</span>
                    </div>
                    <Progress
                      value={campaña.progreso ?? 0}
                      className="h-1 mt-1"
                    />
                  </CardContent>
                </Card>
              ))}
            {campañas.filter(
              (c) =>
                c.estado === "Activa" ||
                c.estado === "Pausada" ||
                c.estado === "Borrador"
            ).length === 0 && (
              <p className="text-xs text-gray-500 text-center py-4">
                No hay campañas activas o pausadas para seleccionar.
              </p>
            )}
          </div>
        </CardContent>
        {/* Sección Agentes */}
        <CardHeader className="border-b">
          <CardTitle className="text-base font-semibold">Agentes</CardTitle>
        </CardHeader>
        <CardContent className="p-4 flex-1 overflow-y-auto">
          <div className="space-y-3">
            {agentes.map((agente) => (
              <div
                key={agente.id}
                className="flex items-center gap-3 p-1 rounded-md hover:bg-gray-100 cursor-pointer"
              >
                <Avatar className="h-7 w-7">
                  <AvatarImage src={agente.avatar} alt={agente.nombre} />
                  <AvatarFallback>
                    {agente.nombre.substring(0, 1)}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 overflow-hidden">
                  <div className="text-xs font-medium truncate">
                    {agente.nombre}
                  </div>
                  <div className="text-xs text-gray-500">
                    {agente.tipo} - {agente.estado}
                  </div>
                </div>
                {/* Opcional: Rendimiento */}
                {/* <div className="w-12 text-right"><span className="text-xs font-medium">{agente.rendimiento}%</span></div> */}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default DashboardView;
