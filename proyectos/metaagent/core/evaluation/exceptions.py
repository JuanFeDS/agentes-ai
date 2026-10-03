"""Excepciones personalizadas para el módulo de evaluación."""

class EvaluationError(Exception):
    """Excepción base para errores de evaluación."""
    pass

class AgentLoadError(EvaluationError):
    """Error al cargar un agente."""
    pass

class LLMEvaluationError(EvaluationError):
    """Error durante la evaluación con LLM."""
    pass

class InvalidAgentError(EvaluationError):
    """El agente no cumple con los requisitos necesarios."""
    pass
