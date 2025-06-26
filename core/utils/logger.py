"""Utilidades de registro para el framework MetaAgent."""

import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Obtiene un logger configurado.
    
    Args:
        name: Nombre del logger.
        level: Nivel de registro (opcional).
        
    Returns:
        Logger configurado.
    """
    logger = logging.getLogger(name)
    
    # Configurar el nivel de registro
    if level is not None:
        logger.setLevel(level)
    
    # Evitar agregar manejadores múltiples
    if not logger.handlers:
        # Crear un manejador para la salida estándar
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level or logging.INFO)
        
        # Definir el formato del log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Agregar el manejador al logger
        logger.addHandler(handler)
    
    return logger
