"""Script principal para rollback de la integración ElevenLabs."""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Optional, Dict

# Importar utils de rollback
from .rollback_utils import (
    take_config_snapshot,
    clear_redis_cache,
    reset_prometheus_metrics,
    close_all_elevenlabs_connections,
    restore_previous_config
)

class AsyncRollbackTransaction:
    """Manejador transaccional para operaciones de rollback."""
    
    def __init__(self):
        self.steps_executed_successfully: List[str] = []
        self.failed_steps: Dict[str, Exception] = {}
    
    async def execute(self, step_name: str, step_func, *args, **kwargs):
        """Ejecuta un paso del rollback capturando errores sin re-lanzarlos."""
        try:
            logger.info(f"Ejecutando paso: {step_name}")
            await step_func(*args, **kwargs)
            self.steps_executed_successfully.append(step_name)
            return True
        except Exception as e:
            logger.error(f"Error en paso '{step_name}': {str(e)}", exc_info=True)
            self.failed_steps[step_name] = e
            return False

    @property
    def all_steps_succeeded(self) -> bool:
        """Indica si todos los pasos se ejecutaron exitosamente."""
        return not self.failed_steps

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def rollback_elevenlabs_integration(
    dry_run: bool = False,
    take_snapshot: bool = False
) -> bool:
    """
    Ejecuta el rollback completo de la integración con ElevenLabs.

    Args:
        dry_run: Solo simula las acciones sin ejecutarlas
        take_snapshot: Toma snapshot de configuración antes del rollback

    Returns:
        bool: True si el rollback fue exitoso
    """
    logger.info(f"Iniciando rollback ElevenLabs {'(dry run)' if dry_run else ''}")
    
    async with AsyncRollbackTransaction() as transaction:
        # Paso 0: Tomar snapshot si se solicita
        if take_snapshot and not dry_run:
            await transaction.execute(
                "Snapshot de configuración",
                take_config_snapshot
            )

        # Paso 1: Cerrar conexiones activas
        await transaction.execute(
            "Cerrar conexiones activas",
            close_all_elevenlabs_connections
        )

        # Paso 2: Limpiar caché Redis
        if not dry_run:
            deleted = await clear_redis_cache("elevenlabs:*")
            logger.info(f"Eliminadas {deleted} claves")
            await transaction.execute(
                "Limpiar caché Redis",
                clear_redis_cache, 
                "elevenlabs:*"
            )

        # Paso 3: Resetear métricas
        await transaction.execute(
            "Resetear métricas Prometheus",
            reset_prometheus_metrics
        )

        # Paso 4: Restaurar configuración
        await transaction.execute(
            "Restaurar configuración",
            restore_previous_config
        )

    # Reporte final
    if transaction.all_steps_succeeded:
        logger.info(f"Rollback {'simulado' if dry_run else 'completado'} exitosamente")
    else:
        logger.error("Rollback completado con errores en algunos pasos")
    
    if transaction.steps_executed_successfully:
        logger.info(f"Pasos exitosos: {', '.join(transaction.steps_executed_successfully)}")
    if transaction.failed_steps:
        logger.error(f"Pasos fallidos: {', '.join(transaction.failed_steps.keys())}")

    return transaction.all_steps_succeeded

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Simular rollback sin cambios")
    parser.add_argument("--snapshot", action="store_true", help="Tomar snapshot antes de rollback")
    args = parser.parse_args()

    # Configurar path para imports
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    # Ejecutar rollback
    success = asyncio.run(
        rollback_elevenlabs_integration(
            dry_run=args.dry_run,
            take_snapshot=args.snapshot
        )
    )
    sys.exit(0 if success else 1)
