"""Módulo principal para la evaluación de agentes."""

import ast
import importlib
import inspect
import io
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type

from .result import AgentEvaluationResult
from .llm_evaluator import LLMEvaluator
from ..agents.agent_loader import load_agent_class
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AgentEvaluator:
    """Evaluador de agentes generados."""
    
    def __init__(self, agents_dir: str = "agents"):
        """Inicializa el evaluador de agentes.
        
        Args:
            agents_dir: Directorio donde se encuentran los agentes generados.
        """
        # Configurar la codificación de la consola para Windows
        if sys.platform == 'win32':
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, 
                encoding='utf-8', 
                errors='replace'
            )
            
        self.agents_dir = Path(agents_dir)
        self.agents_dir.mkdir(exist_ok=True)
        self.llm_evaluator = LLMEvaluator()
    
    def discover_agents(self) -> List[Path]:
        """Descubre todos los agentes en el directorio de agentes.
        
        Returns:
            Lista de rutas a los módulos de los agentes.
        """
        return list(self.agents_dir.glob("*.py"))
    
    def evaluate_agent(self, agent_path: Path) -> AgentEvaluationResult:
        """Evalúa un agente específico.
        
        Args:
            agent_path: Ruta al archivo del agente a evaluar.
            
        Returns:
            Resultado de la evaluación del agente.
        """
        result = AgentEvaluationResult(agent_path.stem)
        
        try:
            # Cargar el módulo del agente
            agent_class = load_agent_class(agent_path)
            
            # Realizar pruebas dinámicas
            self._run_dynamic_tests(agent_class, result)
            
        except Exception as e:
            result.add_failure("carga_agente", str(e))
        
        return result
    
    def _run_dynamic_tests(
        self, 
        agent_class: Type[Any], 
        result: AgentEvaluationResult
    ) -> None:
        """Ejecuta pruebas dinámicas en el agente cargado.
        
        Args:
            agent_class: Clase del agente a evaluar.
            result: Objeto para almacenar los resultados.
        """
        # Crear un archivo CSV de prueba temporal
        with tempfile.NamedTemporaryFile(
            mode='w+', 
            suffix='.csv', 
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            temp_file.write("""nombre,edad,ciudad,puntuacion
Juan,25,Madrid,85
Maria,30,Barcelona,92
Pedro,22,Valencia,78
Ana,35,Sevilla,88
Luis,28,Bilbao,95""")
            temp_file_path = temp_file.name
        
        try:
            # Instanciar el agente con el archivo de prueba
            agent = agent_class(temp_file_path)
            result.add_success("instanciacion")
            
            # Probar el método analyze si existe
            if hasattr(agent, 'analyze'):
                self._test_analyze_method(agent, result)
            
            # Probar el método validate si existe
            if hasattr(agent, 'validate'):
                self._test_validate_method(agent, result)
                
        except Exception as e:
            result.add_failure("ejecucion_agente", str(e))
            
        finally:
            # Limpiar archivo de prueba
            try:
                Path(temp_file_path).unlink(missing_ok=True)
            except Exception:
                pass
    
    def _test_analyze_method(self, agent: Any, result: AgentEvaluationResult) -> None:
        """Prueba el método analyze del agente.
        
        Args:
            agent: Instancia del agente.
            result: Objeto para almacenar resultados.
        """
        old_stdout = sys.stdout
        output_buffer = io.StringIO()
        
        try:
            # Redirigir la salida estándar
            sys.stdout = output_buffer
            
            # Ejecutar el método analyze
            agent.analyze()
            
            # Obtener la salida y restaurar la salida estándar
            output = output_buffer.getvalue()
            sys.stdout = old_stdout
            
            # Registrar métricas y éxito
            result.add_metric("tamano_salida_analyze", len(output))
            result.add_success("ejecucion_analyze")
            
            # Evaluar la salida con LLM
            self._evaluate_with_llm(agent, output, result)
            
        except Exception as e:
            # Restaurar la salida estándar en caso de error
            sys.stdout = old_stdout
            
            # Manejar el error de manera segura para UTF-8
            try:
                error_msg = str(e)
            except:
                error_msg = "Error al ejecutar el método analyze"
                
            result.add_failure("ejecucion_analyze", error_msg)
    
    def _test_validate_method(self, agent: Any, result: AgentEvaluationResult) -> None:
        """Prueba el método validate del agente.
        
        Args:
            agent: Instancia del agente.
            result: Objeto para almacenar resultados.
        """
        old_stdout = sys.stdout
        output_buffer = io.StringIO()
        
        try:
            # Redirigir la salida estándar
            sys.stdout = output_buffer
            
            # Ejecutar el método validate
            agent.validate()
            
            # Obtener la salida y restaurar la salida estándar
            output = output_buffer.getvalue()
            sys.stdout = old_stdout
            
            # Verificar si hay salida
            if not output:
                result.add_failure("ejecucion_validate", "El método validate no generó ninguna salida")
            else:
                result.add_success("ejecucion_validate")
                
        except Exception as e:
            # Restaurar la salida estándar en caso de error
            sys.stdout = old_stdout
            
            # Manejar el error de manera segura para UTF-8
            try:
                error_msg = str(e)
            except:
                error_msg = "Error al ejecutar el método validate"
                
            result.add_failure("ejecucion_validate", error_msg)
    
    def _evaluate_with_llm(
        self, 
        agent: Any, 
        output: str, 
        result: AgentEvaluationResult
    ) -> None:
        """Evalúa la salida del agente usando un modelo de lenguaje.
        
        Args:
            agent: Instancia del agente.
            output: Salida del agente a evaluar.
            result: Objeto para almacenar resultados.
        """
        try:
            # Obtener la descripción del agente desde su docstring
            agent_description = inspect.getdoc(agent.__class__) or "Sin descripción"
            
            # Definir criterios de evaluación
            criteria = """
            1. La salida debe ser clara y fácil de entender.
            2. Debe incluir información relevante sobre los datos analizados.
            3. Los resultados deben ser precisos y consistentes con los datos de entrada.
            4. La salida debe estar bien formateada y organizada.
            """
            
            # Evaluar con LLM
            llm_result = self.llm_evaluator.evaluate(
                agent_description=agent_description,
                output=output,
                criteria=criteria
            )
            
            # Registrar resultados
            result.add_metric("puntuacion_llm", llm_result.get("score", 0))
            result.add_metric("razonamiento_llm", llm_result.get("reasoning", ""))
            
            # Agregar sugerencias
            for suggestion in llm_result.get("suggestions", []):
                result.add_suggestion(suggestion)
                
        except Exception as e:
            result.add_failure("evaluacion_llm", str(e))
    
    def evaluate_all_agents(self) -> List[AgentEvaluationResult]:
        """Evalúa todos los agentes en el directorio de agentes.
        
        Returns:
            Lista de resultados de evaluación para cada agente.
        """
        agent_paths = self.discover_agents()
        results = []
        
        for agent_path in agent_paths:
            logger.info(f"Evaluando agente: {agent_path.name}")
            result = self.evaluate_agent(agent_path)
            results.append(result)
            
            # Imprimir resultados
            print("\n" + str(result) + "\n" + "-" * 80)
        
        return results
