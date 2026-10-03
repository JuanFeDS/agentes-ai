"""Módulo para manejar los resultados de la evaluación de agentes."""

from typing import Dict, List, Tuple, Any, Optional


class AgentEvaluationResult:
    """Resultado de la evaluación de un agente."""

    def __init__(self, agent_name: str):
        """Inicializa un nuevo resultado de evaluación.
        
        Args:
            agent_name: Nombre del agente evaluado.
        """
        self.agent_name = agent_name
        self.passed_tests = 0
        self.failed_tests = 0
        self.errors: List[Tuple[str, str]] = []
        self.metrics: Dict[str, Any] = {}
        self.suggestions: List[str] = []

    def add_success(self, test_name: str) -> None:
        """Registra una prueba exitosa.
        
        Args:
            test_name: Nombre de la prueba exitosa.
        """
        self.passed_tests += 1

    def add_failure(self, test_name: str, error: str) -> None:
        """Registra una prueba fallida.
        
        Args:
            test_name: Nombre de la prueba fallida.
            error: Mensaje de error.
        """
        self.failed_tests += 1
        self.errors.append((test_name, str(error)))

    def add_metric(self, name: str, value: Any) -> None:
        """Agrega una métrica de rendimiento.
        
        Args:
            name: Nombre de la métrica.
            value: Valor de la métrica.
        """
        self.metrics[name] = value

    def add_suggestion(self, suggestion: str) -> None:
        """Agrega una sugerencia de mejora.
        
        Args:
            suggestion: Sugerencia de mejora.
        """
        self.suggestions.append(suggestion)

    def score(self) -> float:
        """Calcula un puntaje de evaluación general (0-100).
        
        Returns:
            Puntaje de evaluación (0-100).
        """
        total_tests = self.passed_tests + self.failed_tests
        if total_tests == 0:
            return 0.0
        return (self.passed_tests / total_tests) * 100

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el resultado a un diccionario.
        
        Returns:
            Diccionario con los resultados de la evaluación.
        """
        return {
            'agent_name': self.agent_name,
            'passed_tests': self.passed_tests,
            'failed_tests': self.failed_tests,
            'score': self.score(),
            'errors': self.errors,
            'metrics': self.metrics,
            'suggestions': self.suggestions
        }

    def __str__(self) -> str:
        """Representación en cadena del resultado.
        
        Returns:
            Cadena formateada con los resultados.
        """
        lines = [
            f"Evaluación del agente: {self.agent_name}",
            "=" * 50,
            f"Puntaje: {self.score():.1f}%",
            f"Pruebas exitosas: {self.passed_tests}",
            f"Pruebas fallidas: {self.failed_tests}",
        ]

        if self.metrics:
            lines.append("\nMétricas:")
            for name, value in self.metrics.items():
                lines.append(f"  - {name}: {value}")

        if self.errors:
            lines.append("\nErrores encontrados:")
            for test_name, error in self.errors:
                lines.append(f"  - {test_name}: {error}")

        if self.suggestions:
            lines.append("\nSugerencias de mejora:")
            for i, suggestion in enumerate(self.suggestions, 1):
                lines.append(f"  {i}. {suggestion}")

        return "\n".join(lines)
