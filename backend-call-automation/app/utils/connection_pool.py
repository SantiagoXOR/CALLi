import asyncio
from contextlib import asynccontextmanager
from typing import Any, Generic, TypeVar

# Definir un tipo genérico para las conexiones
T = TypeVar("T")


class ConnectionPool(Generic[T]):
    """Pool de conexiones para la API de ElevenLabs."""

    def __init__(self, max_size: int = 10, timeout: int = 30, max_retries: int = 3) -> None:
        self.max_size = max_size
        self.timeout = timeout
        self.max_retries = max_retries
        self._semaphore = asyncio.Semaphore(max_size)
        self._connections: list[T] = []

    @asynccontextmanager
    async def acquire(self) -> Any:
        """
        Adquiere una conexión del pool.

        Yields:
            Una conexión del pool (en este caso simplificado, el propio pool).
        """
        async with self._semaphore:
            try:
                # In a real scenario, you might get an existing idle connection
                # or create a new one if the pool is not full.
                # For simplicity here, we just yield self, assuming the pool manages sessions implicitly.
                yield self
            finally:
                # The release logic might be more complex, e.g., returning a connection to the pool.
                pass  # Simplified release within context manager

    async def release(self, connection: T) -> None:
        """
        Libera una conexión al pool.

        Este método devuelve una conexión al pool para que pueda ser reutilizada.
        En esta implementación simplificada, solo verifica si la conexión está en el pool.

        Args:
            connection: La conexión a liberar.
        """
        # This method might not be needed if using the context manager approach for acquire/release.
        # If used separately, it should handle returning the connection properly.
        # For now, keep it simple or remove if acquire context manager handles everything.
        # Simplified or potentially unused release method
        if connection in self._connections:
            # Lógica para marcar la conexión como disponible
            pass
