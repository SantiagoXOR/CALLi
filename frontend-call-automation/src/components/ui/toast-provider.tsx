"use client";

import { Toaster } from "sonner";

export function ToastProvider() {
  return (
    <Toaster
      position="top-right"
      toastOptions={{
        style: {
          fontSize: "14px",
        },
        duration: 5000,
        className: "toast-custom",
        success: {
          style: {
            borderLeft: "4px solid #22c55e",
          },
        },
        error: {
          style: {
            borderLeft: "4px solid #ef4444",
          },
        },
        warning: {
          style: {
            borderLeft: "4px solid #f59e0b",
          },
        },
        info: {
          style: {
            borderLeft: "4px solid #3b82f6",
          },
        },
      }}
    />
  );
}
