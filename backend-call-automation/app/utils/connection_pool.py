import asyncio
from typing import Any, Optional
from contextlib import asynccontextmanager

class ConnectionPool:
    """Pool de conexiones para la API de ElevenLabs."""
    
    def __init__(
        self,
        max_size: int = 10,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.max_size = max_size
        self.timeout = timeout
        self.max_retries = max_retries
        self._semaphore = asyncio.Semaphore(max_size)
        self._connections = []
        
    @asynccontextmanager
    async def acquire(self):
        """Adquiere una conexión del pool."""
        async with self._semaphore:
            try:
                # In a real scenario, you might get an existing idle connection
                # or create a new one if the pool is not full.
                # For simplicity here, we just yield self, assuming the pool manages sessions implicitly.
                yield self 
            finally:
                # The release logic might be more complex, e.g., returning a connection to the pool.
                pass # Simplified release within context manager
    
    async def release(self, connection: Any):
        """Libera una conexión al pool."""
        # This method might not be needed if using the context manager approach for acquire/release.
        # If used separately, it should handle returning the connection properly.
        # For now, keep it simple or remove if acquire context manager handles everything.
        pass # Simplified or potentially unused release method
