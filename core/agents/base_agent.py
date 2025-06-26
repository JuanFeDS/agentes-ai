"""Clase base para todos los agentes generados."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseAgent(ABC):
    """Clase base abstracta para todos los agentes generados."""
    
    def __init__(self, *args, **kwargs):
        """Inicializa el agente con los parámetros necesarios."""
        super().__init__()
    
    @abstractmethod
    def analyze(self) -> Any:
        """Realiza el análisis principal del agente.
        
        Returns:
            Resultado del análisis.
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """Valida los resultados del análisis.
        
        Returns:
            True si la validación es exitosa, False en caso contrario.
        """
        pass
    
    def __str__(self) -> str:
        """Representación en cadena del agente.
        
        Returns:
            Nombre de la clase del agente.
        """
        return self.__class__.__name__
