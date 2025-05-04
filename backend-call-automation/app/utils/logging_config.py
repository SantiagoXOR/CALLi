import json
import logging
from datetime import datetime
from typing import Any

# Configure root logger or specific loggers as needed
# This basic config sets up console logging for the elevenlabs logger
# In a real app, you'd likely use a more robust logging setup (e.g., file handlers, rotation)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class ElevenLabsLogger:
    """Provides structured logging specifically for ElevenLabs service interactions."""

    def __init__(self, logger_name: str = "elevenlabs_service") -> None:
        self.logger = logging.getLogger(logger_name)
        # Ensure logger level is set (can be configured externally too)
        if not self.logger.hasHandlers():
            # Add handler if none exists, e.g., StreamHandler
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)  # Set desired level

    def _create_log_entry(
        self, level: str, method: str, message: str, context: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Helper to create a structured log entry."""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "service": "ElevenLabsService",
            "method": method,
            "message": message,
        }
        if context:
            entry.update(context)
        return entry

    def log_api_call(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        duration: float | None = None,
        success: bool = True,
        response_info: dict[str, Any] | None = None,
    ) -> None:
        """Logs details of an API call attempt and its outcome."""
        message = f"API call {method} {'succeeded' if success else 'failed'}"
        context = {
            "params": params if params else {},
            "duration_ms": round(duration * 1000, 2) if duration is not None else None,
            "success": success,
            "response_info": response_info if response_info else {},
        }
        sanitized_context = self._sanitize_params(context)
        log_entry = self._create_log_entry(
            "INFO" if success else "WARNING", method, message, sanitized_context
        )
        # Log based on success status
        if success:
            self.logger.info(json.dumps(log_entry))
        else:
            # Log failures as warnings or errors depending on severity
            self.logger.warning(json.dumps(log_entry))

    def _sanitize_params(self, params: dict[str, Any] | None) -> dict[str, Any] | None:
        """Sanitizes sensitive parameters like API keys."""
        if not params:
            return None
        sanitized = params.copy()
        # List of keys to sanitize - expand as needed
        sensitive_keys = ["api_key", "token", "password", "Authorization"]
        for key in sensitive_keys:
            if key in sanitized:
                sanitized[key] = "***"
        # Sanitize nested structures if necessary (recursive approach might be needed)
        if "headers" in sanitized and isinstance(sanitized["headers"], dict):
            for h_key in sensitive_keys:
                if h_key in sanitized["headers"]:
                    sanitized["headers"][h_key] = "***"
        return sanitized

    def log_error(
        self, method: str, error: Exception, context: dict[str, Any] | None = None
    ) -> None:
        """Logs detailed error information."""
        message = f"Error during {method}: {error!s}"
        error_context = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context if context else {},
        }
        log_entry = self._create_log_entry("ERROR", method, message, error_context)
        # Use logger.error for errors, potentially with exc_info=True for traceback
        self.logger.error(
            json.dumps(log_entry), exc_info=False
        )  # Set exc_info=True if traceback is needed

    def log_info(self, method: str, message: str, context: dict[str, Any] | None = None) -> None:
        """Logs general informational messages."""
        log_entry = self._create_log_entry("INFO", method, message, context)
        self.logger.info(json.dumps(log_entry))

    def log_warning(self, method: str, message: str, context: dict[str, Any] | None = None) -> None:
        """Logs warning messages."""
        log_entry = self._create_log_entry("WARNING", method, message, context)
        self.logger.warning(json.dumps(log_entry))


# Global instance (optional, could be instantiated per service instance)
# elevenlabs_logger = ElevenLabsLogger()
