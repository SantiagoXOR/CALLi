"use client";

import { useState } from "react";
import { format } from "date-fns";
import { es } from "date-fns/locale";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Download, Robot, User } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

interface CallTranscriptProps {
  transcript: Message[] | string;
}

export function CallTranscript({ transcript }: CallTranscriptProps) {
  const [showTimestamps, setShowTimestamps] = useState(false);

  // Parse transcript if it's a string
  const messages: Message[] = typeof transcript === "string"
    ? JSON.parse(transcript)
    : transcript;

  // Download transcript as text file
  const downloadTranscript = () => {
    const text = messages
      .map((msg) => {
        const speaker = msg.role === "assistant" ? "AI" : "Usuario";
        const time = msg.timestamp
          ? format(new Date(msg.timestamp), "HH:mm:ss", { locale: es })
          : "";
        return `[${time}] ${speaker}: ${msg.content}`;
      })
      .join("\n\n");

    const blob = new Blob([text], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `transcript-${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (!messages || messages.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <p>No hay transcripción disponible.</p>
      </div>
    );
  }

  return (
    <div className="border rounded-md">
      <div className="flex justify-between items-center p-3 border-b">
        <h3 className="text-sm font-medium">Transcripción de la conversación</h3>
        <div className="flex space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowTimestamps(!showTimestamps)}
          >
            {showTimestamps ? "Ocultar horas" : "Mostrar horas"}
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={downloadTranscript}
          >
            <Download className="h-4 w-4 mr-2" />
            Descargar
          </Button>
        </div>
      </div>

      <ScrollArea className="h-[400px] p-4">
        <div className="space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${
                message.role === "assistant" ? "justify-start" : "justify-end"
              }`}
            >
              <div
                className={`flex max-w-[80%] ${
                  message.role === "assistant"
                    ? "flex-row"
                    : "flex-row-reverse"
                }`}
              >
                <div
                  className={`flex items-center justify-center h-8 w-8 rounded-full mr-2 ${
                    message.role === "assistant"
                      ? "bg-primary/10 text-primary"
                      : "bg-secondary text-secondary-foreground"
                  }`}
                >
                  {message.role === "assistant" ? (
                    <Robot className="h-4 w-4" />
                  ) : (
                    <User className="h-4 w-4" />
                  )}
                </div>
                <div>
                  <div
                    className={`rounded-lg px-3 py-2 ${
                      message.role === "assistant"
                        ? "bg-primary/10 text-foreground"
                        : "bg-secondary text-secondary-foreground"
                    }`}
                  >
                    {message.content}
                  </div>
                  {showTimestamps && message.timestamp && (
                    <div className="text-xs text-muted-foreground mt-1">
                      {format(new Date(message.timestamp), "HH:mm:ss", {
                        locale: es,
                      })}
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
