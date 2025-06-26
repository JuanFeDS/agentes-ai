"""
Paquete principal de MetaAgent.

Este paquete proporciona las funcionalidades principales para la creación,
evaluación y gestión de agentes de inteligencia artificial.
"""

# Importaciones principales
from .builder import AgentBuilder, AgentSpecification
from .evaluation import AgentEvaluator, LLMEvaluator, AgentEvaluationResult

__all__ = [
    'AgentBuilder',
    'AgentSpecification',
    'AgentEvaluator',
    'LLMEvaluator',
    'AgentEvaluationResult'
]

__version__ = "0.1.0"
