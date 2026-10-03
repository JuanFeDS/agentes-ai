"""Módulo para cargar dinámicamente clases de agentes."""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Any, Optional, Type


def load_agent_module(agent_path: Path) -> Any:
    """Carga un módulo de agente desde un archivo.
    
    Args:
        agent_path: Ruta al archivo del agente.
        
    Returns:
        Módulo cargado.
        
    Raises:
        ImportError: Si no se puede cargar el módulo.
    """
    try:
        # Convertir la ruta a módulo (ej: agents/mi_agente.py -> agents.mi_agente)
        module_name = str(agent_path.with_suffix('')).replace('\\', '.').replace('/', '.')
        
        # Cargar el módulo
        spec = importlib.util.spec_from_file_location(module_name, agent_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"No se pudo cargar el módulo desde {agent_path}")
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        return module
        
    except Exception as e:
        raise ImportError(f"Error al cargar el módulo {agent_path}: {str(e)}")


def find_agent_class(module: Any, agent_name: str = None) -> Optional[Type[Any]]:
    """Encuentra la clase principal del agente en un módulo.
    
    Args:
        module: Módulo donde buscar la clase.
        agent_name: Nombre esperado del agente (opcional).
        
    Returns:
        Clase del agente si se encuentra, None en caso contrario.
    """
    # Si se proporciona un nombre de agente, buscar una clase que coincida
    if agent_name:
        # Intentar con el nombre exacto
        if hasattr(module, agent_name):
            cls = getattr(module, agent_name)
            if inspect.isclass(cls):
                return cls
        
        # Intentar con el nombre en formato de clase (primera letra mayúscula)
        class_name = agent_name[0].upper() + agent_name[1:] if agent_name else ""
        if hasattr(module, class_name):
            cls = getattr(module, class_name)
            if inspect.isclass(cls):
                return cls
    
    # Si no se encontró por nombre, buscar la primera clase que no sea una excepción
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Ignorar clases internas y excepciones
        if not name.startswith('_') and not issubclass(obj, Exception):
            return obj
    
    return None


def load_agent_class(agent_path: Path) -> Type[Any]:
    """Carga la clase principal de un agente desde un archivo.
    
    Args:
        agent_path: Ruta al archivo del agente.
        
    Returns:
        Clase del agente.
        
    Raises:
        ImportError: Si no se puede cargar el módulo o encontrar la clase.
    """
    # Cargar el módulo
    module = load_agent_module(agent_path)
    
    # Obtener el nombre base del archivo sin extensión
    agent_name = agent_path.stem
    
    # Buscar la clase del agente
    agent_class = find_agent_class(module, agent_name)
    
    if agent_class is None:
        raise ImportError(f"No se pudo encontrar una clase de agente en {agent_path}")
    
    return agent_class
