"""
Configuración del logger para la aplicación.
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado para el módulo especificado.

    Args:
        name: Nombre del módulo

    Returns:
        logging.Logger: Logger configurado
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger
