import { toast, ToastT } from "sonner";

export type NotificationType = "success" | "error" | "warning" | "info";

export interface NotificationOptions {
  duration?: number;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  onDismiss?: () => void;
  onAutoClose?: () => void;
  closeButton?: boolean;
}

class NotificationService {
  /**
   * Show a notification toast
   */
  show(
    message: string,
    type: NotificationType = "info",
    options?: NotificationOptions
  ): ToastT {
    const {
      duration,
      description,
      action,
      onDismiss,
      onAutoClose,
      closeButton = true,
    } = options || {};

    // Create toast based on type
    switch (type) {
      case "success":
        return toast.success(message, {
          duration,
          description,
          action,
          onDismiss,
          onAutoClose,
          closeButton,
        });
      case "error":
        return toast.error(message, {
          duration,
          description,
          action,
          onDismiss,
          onAutoClose,
          closeButton,
        });
      case "warning":
        return toast.warning(message, {
          duration,
          description,
          action,
          onDismiss,
          onAutoClose,
          closeButton,
        });
      case "info":
      default:
        return toast.info(message, {
          duration,
          description,
          action,
          onDismiss,
          onAutoClose,
          closeButton,
        });
    }
  }

  /**
   * Show a success notification
   */
  success(message: string, options?: NotificationOptions): ToastT {
    return this.show(message, "success", options);
  }

  /**
   * Show an error notification
   */
  error(message: string, options?: NotificationOptions): ToastT {
    return this.show(message, "error", options);
  }

  /**
   * Show a warning notification
   */
  warning(message: string, options?: NotificationOptions): ToastT {
    return this.show(message, "warning", options);
  }

  /**
   * Show an info notification
   */
  info(message: string, options?: NotificationOptions): ToastT {
    return this.show(message, "info", options);
  }

  /**
   * Show a loading notification that can be updated
   */
  loading(
    message: string,
    promise: Promise<any>,
    options?: {
      loading?: string;
      success?: string | ((data: any) => string);
      error?: string | ((error: any) => string);
      description?: string;
      successDescription?: string | ((data: any) => string);
      errorDescription?: string | ((error: any) => string);
    }
  ): Promise<any> {
    return toast.promise(promise, {
      loading: options?.loading || message,
      success: options?.success || "Operación completada",
      error: options?.error || "Ha ocurrido un error",
      description: options?.description,
      successDescription: options?.successDescription,
      errorDescription: options?.errorDescription,
    });
  }

  /**
   * Dismiss all notifications
   */
  dismissAll(): void {
    toast.dismiss();
  }

  /**
   * Dismiss a specific notification
   */
  dismiss(toastId: string | number): void {
    toast.dismiss(toastId);
  }
}

export const notificationService = new NotificationService();
