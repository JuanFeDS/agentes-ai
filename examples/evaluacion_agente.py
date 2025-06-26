"""
Ejemplo de uso del evaluador de agentes.

Este script muestra cómo utilizar el AgentEvaluator para evaluar agentes generados.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
sys.path.append(str(Path(__file__).parent.parent))

from core.agent_evaluator import AgentEvaluator

def main():
    # Crear un evaluador de agentes
    evaluator = AgentEvaluator(agents_dir="agents")
    
    # Evaluar todos los agentes en el directorio
    print("Iniciando evaluación de agentes...\n")
    results = evaluator.evaluate_all_agents()
    
    if not results:
        print("No se encontraron agentes para evaluar en el directorio 'agents/'.")
        print("Ejecuta primero el script de generación de agentes.")
    else:
        # Mostrar resumen de resultados
        print("\n" + "="*50)
        print("RESUMEN DE EVALUACIÓN")
        print("="*50)
        
        for result in results:
            print(f"\nAgente: {result.agent_name}")
            print(f"  Puntaje: {result.score:.1f}%")
            print(f"  Pruebas exitosas: {result.passed_tests}")
            print(f"  Pruebas fallidas: {result.failed_tests}")
            
            if result.suggestions:
                print("\n  Sugerencias de mejora:")
                for i, suggestion in enumerate(result.suggestions[:3], 1):
                    print(f"  {i}. {suggestion}")
                    if i >= 3 and len(result.suggestions) > 3:
                        print(f"  ... y {len(result.suggestions) - 3} sugerencias más")
                        break
        
        avg_score = sum(r.score for r in results) / len(results)
        print(f"\nPuntaje promedio: {avg_score:.1f}%")


if __name__ == "__main__":
    main()
