import { ToastProvider } from "@/components/ui/toast-provider";
import { AuthProvider } from "@/contexts/AuthContext";
import QueryProvider from "@/providers/QueryProvider";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Sistema de Automatización de Llamadas",
  description:
    "Plataforma para gestión y automatización de campañas de llamadas",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return (
    <html lang="es" className="h-full">
      <body className={`${inter.className} h-full bg-background`}>
        <QueryProvider>
          <ToastProvider />
          <AuthProvider>{children}</AuthProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
