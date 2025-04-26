"use client";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle, CheckCircle2, FileText, Upload } from "lucide-react";
import React, { useState } from "react";
import { toast } from "sonner";
import { useImportContacts } from "../services/contactService";
import { Button } from "./ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./ui/card";
import { Input } from "./ui/input";
import { Progress } from "./ui/progress";

interface ContactImportProps {
  onCancel: () => void;
  onSuccess: () => void;
}

export const ContactImport: React.FC<ContactImportProps> = ({
  onCancel,
  onSuccess,
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadResult, setUploadResult] = useState<{
    imported: number;
    errors: number;
  } | null>(null);

  const importContacts = useImportContacts();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];

      // Verificar que sea un archivo CSV
      if (
        selectedFile.type !== "text/csv" &&
        !selectedFile.name.endsWith(".csv")
      ) {
        toast.error("Por favor, selecciona un archivo CSV válido");
        return;
      }

      setFile(selectedFile);
    }
  };

  const handleImport = async () => {
    if (!file) {
      toast.error("Por favor, selecciona un archivo CSV");
      return;
    }

    try {
      setIsUploading(true);

      // Simular progreso de carga (en una implementación real, esto vendría del backend)
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 95) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 5;
        });
      }, 200);

      const result = await importContacts.mutateAsync(file);

      clearInterval(progressInterval);
      setUploadProgress(100);
      setUploadResult(result);

      if (result.imported > 0) {
        toast.success(
          `Se importaron ${result.imported} contactos correctamente`
        );

        // Esperar un momento antes de cerrar para mostrar el resultado
        setTimeout(() => {
          onSuccess();
        }, 2000);
      } else {
        toast.error("No se pudo importar ningún contacto");
      }
    } catch (error) {
      console.error("Error al importar contactos:", error);
      toast.error("Error al importar contactos");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Importar Contactos</CardTitle>
        <CardDescription>
          Importa contactos desde un archivo CSV. El archivo debe tener las
          columnas: nombre, teléfono, email (opcional), notas (opcional).
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {!isUploading && !uploadResult ? (
          <div className="grid w-full max-w-sm items-center gap-1.5">
            <label htmlFor="csv-file" className="text-sm font-medium">
              Archivo CSV
            </label>
            <div className="flex items-center gap-2">
              <Input
                id="csv-file"
                type="file"
                accept=".csv"
                onChange={handleFileChange}
              />
            </div>
            {file && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground mt-2">
                <FileText className="h-4 w-4" />
                <span>{file.name}</span>
              </div>
            )}
          </div>
        ) : (
          <div className="space-y-4">
            {isUploading && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Subiendo archivo...</span>
                  <span>{uploadProgress}%</span>
                </div>
                <Progress value={uploadProgress} className="h-2" />
              </div>
            )}

            {uploadResult && (
              <Alert
                variant={uploadResult.errors > 0 ? "destructive" : "default"}
              >
                <CheckCircle2 className="h-4 w-4" />
                <AlertTitle>Importación completada</AlertTitle>
                <AlertDescription>
                  Se importaron {uploadResult.imported} contactos correctamente.
                  {uploadResult.errors > 0 && (
                    <div className="mt-2">
                      <AlertCircle className="h-4 w-4 inline mr-1" />
                      {uploadResult.errors} contactos no pudieron ser importados
                      debido a errores.
                    </div>
                  )}
                </AlertDescription>
              </Alert>
            )}
          </div>
        )}
      </CardContent>
      <CardFooter className="flex justify-end space-x-2">
        <Button variant="outline" onClick={onCancel} disabled={isUploading}>
          Cancelar
        </Button>
        {!uploadResult && (
          <Button onClick={handleImport} disabled={!file || isUploading}>
            {isUploading ? (
              <span className="flex items-center">Importando...</span>
            ) : (
              <span className="flex items-center">
                <Upload className="h-4 w-4 mr-2" />
                Importar
              </span>
            )}
          </Button>
        )}
      </CardFooter>
    </Card>
  );
};
