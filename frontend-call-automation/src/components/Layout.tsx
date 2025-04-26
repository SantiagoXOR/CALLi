"use client";

import {
  BarChart3,
  Bell,
  Bot,
  Cog,
  Home,
  List,
  Phone,
  User,
} from "lucide-react"; // Iconos
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import React from "react";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"; // Componente Avatar (asumiendo shadcn/ui)
import { Button } from "@/components/ui/button"; // Componente Button (asumiendo shadcn/ui)
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"; // Componente DropdownMenu (asumiendo shadcn/ui)
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"; // Componente Tabs (asumiendo shadcn/ui) - Lo usaremos para la nav superior
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"; // Componente Tooltip (asumiendo shadcn/ui)

// Mapeo de rutas a valores de pestañas
const routeToTabValue = {
  "/": "dashboard",
  "/campaigns": "lista-campañas",
  "/contacts": "lista-contactos",
  "/calls": "llamadas",
  "/reports": "reportes",
  "/settings": "configuracion",
};

// Tipo para las rutas de navegación
type NavRoute =
  | "/"
  | "/campaigns"
  | "/contacts"
  | "/calls"
  | "/reports"
  | "/settings";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();

  // Determinar la pestaña activa basada en la ruta actual
  const getActiveTab = (): string => {
    // Verificar si la ruta actual coincide exactamente con alguna de las rutas definidas
    if (pathname in routeToTabValue) {
      return routeToTabValue[pathname as NavRoute];
    }

    // Si no hay coincidencia exacta, verificar si la ruta actual comienza con alguna de las rutas definidas
    for (const [route, value] of Object.entries(routeToTabValue)) {
      if (route !== "/" && pathname.startsWith(route)) {
        return value;
      }
    }

    // Si no hay coincidencia, devolver dashboard como valor predeterminado
    return "dashboard";
  };

  const activeTab = getActiveTab();

  // Función para navegar a una ruta basada en el valor de la pestaña
  const navigateToRoute = (value: string) => {
    switch (value) {
      case "dashboard":
        router.push("/");
        break;
      case "lista-campañas":
        router.push("/campaigns");
        break;
      case "lista-contactos":
        router.push("/contacts");
        break;
      case "llamadas":
        router.push("/calls");
        break;
      case "reportes":
        router.push("/reports");
        break;
      case "configuracion":
        router.push("/settings");
        break;
      default:
        router.push("/");
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 font-sans overflow-hidden">
      <header className="bg-white border-b flex-shrink-0 sticky top-0 z-20">
        <div className="px-4 h-16 flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center font-bold text-2xl text-blue-600"
          >
            <Bot className="h-7 w-7 mr-2" />
            <span>CALLi</span>
          </Link>

          <div className="flex items-center gap-3">
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon">
                    <Bell className="h-5 w-5 text-gray-500 hover:text-blue-600" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>
                  <p>Notificaciones</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  className="flex items-center gap-2 px-2 rounded-full"
                >
                  <Avatar className="h-8 w-8">
                    <AvatarImage
                      src="https://placehold.co/40x40/EFEFEF/grey?text=MP"
                      alt="Mi Perfil"
                    />
                    <AvatarFallback>MP</AvatarFallback>
                  </Avatar>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuItem>Perfil</DropdownMenuItem>
                <DropdownMenuItem onClick={() => router.push("/settings")}>
                  Configuración
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem>Cerrar sesión</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>

        <nav className="border-t">
          <Tabs
            value={activeTab}
            onValueChange={navigateToRoute}
            className="w-full"
          >
            <TabsList className="h-12 w-full justify-start rounded-none border-b-0 px-4 gap-1 bg-white">
              {[
                {
                  value: "dashboard",
                  label: "Dashboard",
                  icon: Home,
                  route: "/",
                },
                {
                  value: "lista-campañas",
                  label: "Campañas",
                  icon: List,
                  route: "/campaigns",
                },
                {
                  value: "lista-contactos",
                  label: "Contactos",
                  icon: User,
                  route: "/contacts",
                },
                {
                  value: "llamadas",
                  label: "Llamadas",
                  icon: Phone,
                  route: "/calls",
                },
                {
                  value: "reportes",
                  label: "Reportes",
                  icon: BarChart3,
                  route: "/reports",
                },
                {
                  value: "configuracion",
                  label: "Configuración",
                  icon: Cog,
                  route: "/settings",
                },
              ].map((item) => (
                <TabsTrigger
                  key={item.value}
                  value={item.value}
                  className="h-10 px-3 rounded-md data-[state=active]:bg-blue-50 data-[state=active]:text-blue-600 text-gray-600 hover:bg-gray-100 hover:text-gray-900"
                >
                  <item.icon className="h-4 w-4 mr-2" />
                  {item.label}
                </TabsTrigger>
              ))}
            </TabsList>
          </Tabs>
        </nav>
      </header>

      <main className="flex-1 overflow-y-auto p-6 bg-gray-50">{children}</main>
    </div>
  );
};

export default Layout;
