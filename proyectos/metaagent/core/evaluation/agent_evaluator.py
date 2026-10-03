"""Módulo para evaluar el rendimiento de los agentes generados.

Este módulo proporciona funcionalidad para evaluar automáticamente
el rendimiento de los agentes generados por el MetaAgent.
"""

import importlib
import inspect
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Type
import ast
import astunparse
import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Type
from .llm_evaluator import LLMEvaluator


class AgentEvaluationResult:
    """Resultado de la evaluación de un agente."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.passed_tests = 0
        self.failed_tests = 0
        self.errors: List[Tuple[str, Exception]] = []
        self.metrics: Dict[str, Any] = {}
        self.suggestions: List[str] = []
    
    def add_success(self, test_name: str):
        """Registra una prueba exitosa."""
        self.passed_tests += 1
    
    def add_failure(self, test_name: str, error: Exception):
        """Registra una prueba fallida."""
        self.failed_tests += 1
        self.errors.append((test_name, str(error)))
    
    def add_metric(self, name: str, value: Any):
        """Agrega una métrica de rendimiento."""
        self.metrics[name] = value
    
    def add_suggestion(self, suggestion: str):
        """Agrega una sugerencia de mejora."""
        self.suggestions.append(suggestion)
    
    @property
    def score(self) -> float:
        """Calcula un puntaje de evaluación general (0-100)."""
        total = self.passed_tests + self.failed_tests
        if total == 0:
            return 0.0
        return (self.passed_tests / total) * 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el resultado a un diccionario."""
        return {
            'agent_name': self.agent_name,
            'score': self.score,
            'passed_tests': self.passed_tests,
            'failed_tests': self.failed_tests,
            'errors': self.errors,
            'metrics': self.metrics,
            'suggestions': self.suggestions
        }
    
    def __str__(self) -> str:
        """Representación en cadena del resultado."""
        lines = [
            f"Evaluación del agente: {self.agent_name}",
            "=" * 50,
            f"Puntaje: {self.score:.1f}%",
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


class AgentEvaluator:
    """Evaluador de agentes generados.
    
    Esta clase se encarga de evaluar automáticamente los agentes generados
    por el MetaAgent, proporcionando retroalimentación sobre su rendimiento
    y sugerencias de mejora.
    """
    
    def __init__(self, agents_dir: str = "agents"):
        """Inicializa el evaluador de agentes.
        
        Args:
            agents_dir: Directorio donde se encuentran los agentes generados.
        """
        # Configurar la codificación de la consola para Windows
        import sys
        import io
        
        if sys.platform == 'win32':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            
        self.agents_dir = Path(agents_dir)
        self.agents_dir.mkdir(exist_ok=True)
    
    def discover_agents(self) -> List[Path]:
        """Descubre todos los agentes en el directorio de agentes.
        
        Returns:
            Lista de rutas a los módulos de los agentes.
        """
        agent_dirs = [d for d in self.agents_dir.iterdir() if d.is_dir()]
        agent_modules = []
        
        for agent_dir in agent_dirs:
            # Buscar archivos Python en el directorio del agente
            py_files = list(agent_dir.glob("*.py"))
            if py_files:
                # Tomar el primer archivo Python encontrado
                agent_modules.append(py_files[0])
        
        return agent_modules
    
    def evaluate_agent(self, agent_path: Path) -> AgentEvaluationResult:
        """Evalúa un agente específico.
        
        Args:
            agent_path: Ruta al archivo del agente a evaluar.
            
        Returns:
            Resultado de la evaluación del agente.
        """
        # Extraer el nombre del agente del nombre del directorio
        agent_name = agent_path.parent.name
        result = AgentEvaluationResult(agent_name)
        
        try:
            # Analizar el código fuente del agente
            with open(agent_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # Realizar análisis estático del código
            self._perform_static_analysis(source_code, result)
            
            # Cargar dinámicamente el agente
            agent_module = self._load_agent_module(agent_path)
            
            # Ejecutar pruebas dinámicas si es posible
            self._run_dynamic_tests(agent_module, result)
            
        except Exception as e:
            result.add_failure("evaluacion_general", e)
        
        return result
    
    def _perform_static_analysis(self, source_code: str, result: AgentEvaluationResult):
        """Realiza un análisis estático del código del agente."""
        try:
            # Analizar el AST del código
            tree = ast.parse(source_code)
            
            # Verificar si hay una clase principal
            has_main_class = any(
                isinstance(node, ast.ClassDef) and 
                node.name.lower() == result.agent_name.lower()
                for node in ast.walk(tree)
            )
            
            if not has_main_class:
                result.add_suggestion(
                    f"El agente no tiene una clase principal llamada '{result.agent_name}'. "
                    "Se recomienda usar el mismo nombre del agente para la clase principal."
                )
            else:
                result.add_success("estructura_clase_principal")
            
            # Verificar documentación
            has_docstring = (
                tree.body and 
                isinstance(tree.body[0], ast.Expr) and 
                isinstance(tree.body[0].value, ast.Str)
            )
            
            if not has_docstring:
                result.add_failure("documentacion", "El módulo no tiene docstring")
                result.add_suggestion("Agrega una cadena de documentación al inicio del módulo.")
            else:
                result.add_success("documentacion")
            
            # Verificar manejo de excepciones
            has_exception_handling = any(
                isinstance(node, ast.Try) 
                for node in ast.walk(tree)
            )
            
            if not has_exception_handling:
                result.add_suggestion(
                    "El código no maneja excepciones. Considera agregar bloques try/except "
                    "para manejar errores de manera adecuada."
                )
            else:
                result.add_success("manejo_excepciones")
            
        except Exception as e:
            result.add_failure("analisis_estatico", e)
    
    def _load_agent_module(self, agent_path: Path) -> Any:
        """Carga dinámicamente el módulo del agente."""
        # Agregar el directorio padre al path para importaciones relativas
        sys.path.insert(0, str(agent_path.parent.parent))
        
        try:
            # Importar el módulo dinámicamente
            module_name = agent_path.stem
            spec = importlib.util.spec_from_file_location(module_name, agent_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            raise ImportError(f"No se pudo cargar el módulo del agente: {e}")
        finally:
            # Limpiar el path
            sys.path.pop(0)
    
    def _run_dynamic_tests(self, agent_module: Any, result: AgentEvaluationResult):
        """Ejecuta pruebas dinámicas en el agente cargado."""
        try:
            # Buscar la clase principal del agente
            agent_class = None
            classes = inspect.getmembers(agent_module, inspect.isclass)
            
            # Primero intentar encontrar una clase que coincida con el nombre del módulo
            for name, obj in classes:
                if name.lower() == result.agent_name.lower():
                    agent_class = obj
                    break
            
            # Si no se encontró, tomar la primera clase que no sea una excepción ni empiece con '_'
            if agent_class is None:
                for name, obj in classes:
                    if not name.startswith('_') and not issubclass(obj, Exception):
                        agent_class = obj
                        result.add_suggestion(
                            f"El agente no tiene una clase principal llamada '{result.agent_name}'. "
                            f"Se encontró la clase '{name}' en su lugar."
                        )
                        break
            
            if agent_class is None:
                result.add_failure("clase_principal", "No se encontró ninguna clase en el módulo del agente")
                return
            
            # Verificar si la clase tiene los métodos esperados
            expected_methods = ['__init__', 'analyze']
            for method in expected_methods:
                if not hasattr(agent_class, method):
                    result.add_failure(
                        f"metodo_{method}", 
                        f"La clase no tiene el método '{method}'"
                    )
                else:
                    result.add_success(f"metodo_{method}")
            
            # Intentar instanciar la clase
            try:
                # Crear un archivo CSV de prueba temporal
                test_file = self.agents_dir / "test_data.csv"
                test_data = """nombre,edad,ciudad,puntuacion
Juan,25,Madrid,85
Maria,30,Barcelona,92
Pedro,22,Valencia,78
Ana,35,Sevilla,88
Luis,28,Bilbao,95
"""
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(test_data)
                
                # Instanciar el agente con el archivo de prueba
                agent = agent_class(str(test_file))
                result.add_success("instanciacion")
                
                # Probar el método analyze si existe
                if hasattr(agent, 'analyze'):
                    # Configurar la salida estándar para usar UTF-8
                    import io
                    import sys
                    from contextlib import redirect_stdout
                    
                    # Guardar la salida estándar original
                    old_stdout = sys.stdout
                    
                    try:
                        # Crear un buffer de salida con codificación UTF-8
                        output_buffer = io.StringIO()
                        
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
                
                # Probar el método validate si existe
                if hasattr(agent, 'validate'):
                    # Crear un buffer de salida con codificación UTF-8
                    validate_buffer = io.StringIO()
                    
                    # Guardar la salida estándar original
                    old_stdout = sys.stdout
                    
                    try:
                        # Redirigir la salida estándar
                        sys.stdout = validate_buffer
                        
                        # Ejecutar el método validate
                        agent.validate()
                        
                        # Obtener la salida y restaurar la salida estándar
                        validate_output = validate_buffer.getvalue()
                        sys.stdout = old_stdout
                        
                        # Verificar si hay salida
                        if not validate_output:
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
                
                # Limpiar archivo de prueba
                test_file.unlink(missing_ok=True)
                
            except Exception as e:
                result.add_failure("ejecucion_agente", str(e))
            
        except Exception as e:
            result.add_failure("pruebas_dinamicas", str(e))
    
    def _evaluate_with_llm(self, agent, output: str, result: AgentEvaluationResult):
        """Evalúa la salida del agente usando un modelo de lenguaje."""
        try:
            print("\n" + "="*80)
            print(f"INICIANDO EVALUACIÓN LLM PARA AGENTE: {result.agent_name}")
            print("="*80 + "\n")
            
            # Obtener la descripción del agente desde su docstring
            agent_description = ""
            if agent.__doc__:
                agent_description = agent.__doc__.strip()
            
            print(f"Descripción del agente: {agent_description[:200]}..." if len(agent_description) > 200 else f"Descripción del agente: {agent_description}")
            print(f"\nSalida a evaluar (primeros 500 caracteres):\n{output[:500]}...\n")
            
            # Criterios de evaluación específicos para el tipo de agente
            evaluation_criteria = [
                "La salida debe ser clara y fácil de entender.",
                "Debe incluir información relevante sobre los datos analizados.",
                "Los resultados deben ser precisos y consistentes con los datos de entrada.",
                "La salida debe estar bien formateada y organizada."
            ]
            
            print("Criterios de evaluación:")
            for i, criterion in enumerate(evaluation_criteria, 1):
                print(f"  {i}. {criterion}")
            print()
            
            # Crear evaluador LLM
            llm_evaluator = LLMEvaluator()
            
            # Realizar la evaluación
            print("\n" + "-"*50)
            print("SOLICITANDO EVALUACIÓN AL MODELO DE LENGUAJE")
            print("-"*50 + "\n")
            
            llm_result = llm_evaluator.evaluate_output(
                agent_name=result.agent_name,
                agent_description=agent_description,
                agent_output=output,
                evaluation_criteria=evaluation_criteria
            )
            
            print("\n" + "="*50)
            print("RESULTADO DE LA EVALUACIÓN LLM")
            print("="*50)
            
            # Procesar resultados
            if "error" in llm_result:
                error_msg = f"Error en la evaluación LLM: {llm_result['error']}"
                print(error_msg)
                result.add_failure("evaluacion_llm", error_msg)
            else:
                # Agregar métricas de la evaluación
                llm_score = llm_result.get("score", 0)
                result.add_metric("puntuacion_llm", llm_score)
                print(f"Puntuación: {llm_score}/100")
                
                # Mostrar razonamiento si existe
                if "reasoning" in llm_result:
                    print("\nRazonamiento:")
                    print(llm_result["reasoning"])
                    result.add_metric("razonamiento_llm", llm_result["reasoning"])
                
                # Mostrar fortalezas si existen
                if "strengths" in llm_result and llm_result["strengths"]:
                    print("\nFortalezas:")
                    for strength in llm_result["strengths"]:
                        print(f"- {strength}")
                
                # Mostrar debilidades si existen
                if "weaknesses" in llm_result and llm_result["weaknesses"]:
                    print("\nDebilidades:")
                    for weakness in llm_result["weaknesses"]:
                        print(f"- {weakness}")
                
                # Agregar sugerencias si existen
                if "suggestions" in llm_result and llm_result["suggestions"]:
                    print("\nSugerencias de mejora:")
                    for i, suggestion in enumerate(llm_result["suggestions"], 1):
                        print(f"{i}. {suggestion}")
                        result.add_suggestion(str(suggestion))
                
                # Considerar la puntuación en el puntaje general
                if isinstance(llm_score, (int, float)) and llm_score >= 70:
                    print("\n✅ La salida cumple con los estándares de calidad")
                    result.add_success("evaluacion_calidad_salida")
                else:
                    error_msg = f"❌ La calidad de la salida no cumple con los estándares (Puntaje: {llm_score}/100)"
                    print(f"\n{error_msg}")
                    result.add_failure("evaluacion_calidad_salida", error_msg)
            
            print("\n" + "="*80)
            print(f"FIN DE LA EVALUACIÓN LLM PARA AGENTE: {result.agent_name}")
            print("="*80 + "\n")
                    
        except Exception as e:
            error_msg = f"Error al evaluar con LLM: {str(e)}"
            print(f"\n❌ {error_msg}")
            result.add_failure("error_evaluacion_llm", error_msg)
            import traceback
            traceback.print_exc()
    
    def evaluate_all_agents(self) -> List[AgentEvaluationResult]:
        """Evalúa todos los agentes en el directorio de agentes.
        
        Returns:
            Lista de resultados de evaluación para cada agente.
        """
        agent_paths = self.discover_agents()
        results = []
        
        for agent_path in agent_paths:
            print(f"Evaluando agente: {agent_path.name}")
            result = self.evaluate_agent(agent_path)
            results.append(result)
            print(str(result))
            print("-" * 80)
        
        return results


def main():
    """Función principal para ejecutar la evaluación desde la línea de comandos."""
    evaluator = AgentEvaluator()
    print("Iniciando evaluación de agentes...\n")
    results = evaluator.evaluate_all_agents()
    
    if not results:
        print("No se encontraron agentes para evaluar.")
    else:
        avg_score = sum(r.score for r in results) / len(results)
        print(f"\nEvaluación completada. Puntaje promedio: {avg_score:.1f}%")


if __name__ == "__main__":
    main()
