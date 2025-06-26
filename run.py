"""
Script principal para crear y evaluar agentes de IA.

Este script permite crear un nuevo agente a partir de un nombre y descripción,
y luego evaluar automáticamente su calidad.
"""

import argparse
import io
import sys
import os
from pathlib import Path

# Configurar la codificación de la consola para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Asegurarse de que el directorio raíz esté en el path
sys.path.append(str(Path(__file__).parent))

from core.builder import AgentBuilder, AgentSpecification
from core.evaluation.result import AgentEvaluationResult


def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description='Crea y evalúa un nuevo agente de IA')
    parser.add_argument('--nombre', type=str, required=True, help='Nombre del agente')
    parser.add_argument('--descripcion', type=str, required=True, 
                       help='Descripción detallada del agente')
    parser.add_argument('--tipo', type=str, default='analytics', 
                       help='Tipo de agente (ej: analytics, assistant, etc.)')
    parser.add_argument('--output', type=str, default='agentes_generados',
                       help='Directorio de salida para los agentes generados')
    
    args = parser.parse_args()
    
    print(f"\n{'='*50}")
    print(f"Creando agente: {args.nombre}")
    print(f"Descripción: {args.descripcion}")
    print(f"Tipo: {args.tipo}")
    print(f"Directorio de salida: {args.output}")
    print("="*50 + "\n")
    
    try:
        # 1. Crear la especificación del agente
        spec = AgentSpecification(
            name=args.nombre,
            description=args.descripcion,
            agent_type=args.tipo,
            requirements=['pandas', 'numpy'],  # Requisitos por defecto
            config={
                'version': '1.0',
                'autor': 'Sistema Automatizado'
            }
        )
        
        # 2. Construir el agente
        print("Construyendo agente...")
        builder = AgentBuilder(args.output)
        agent_path = builder.build(spec)
        print(f"✅ Agente creado exitosamente en: {agent_path}")
        
        # 3. Evaluar el agente (usando una evaluación simplificada)
        print("\nEvaluando agente...")
        evaluation = AgentEvaluationResult(args.nombre)
        
        # Verificar que el archivo se creó correctamente
        if agent_path.exists():
            evaluation.add_success("creacion_archivo")
            
            # Verificar que el archivo no está vacío
            if agent_path.stat().st_size > 0:
                evaluation.add_success("archivo_no_vacio")
                
                # Verificación básica del contenido
                with open(agent_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'class ' in content and 'def ' in content:
                        evaluation.add_success("estructura_basica")
                    else:
                        evaluation.add_failure("estructura_basica", "El archivo no contiene una clase o métodos definidos correctamente")
            else:
                evaluation.add_failure("archivo_vacio", "El archivo del agente está vacío")
        else:
            evaluation.add_failure("creacion_archivo", f"No se pudo crear el archivo en {agent_path}")
        
        # Añadir puntuación basada en las pruebas pasadas
        total_tests = evaluation.passed_tests + evaluation.failed_tests
        evaluation.metrics['puntuacion'] = (evaluation.passed_tests / total_tests) * 10 if total_tests > 0 else 0
        
        # 4. Mostrar resultados
        print("\n" + "="*50)
        print("RESULTADOS DE LA EVALUACIÓN")
        print("="*50)
        print(f"Agente: {evaluation.agent_name}")
        
        # Calcular puntuación basada en las pruebas pasadas
        total_tests = evaluation.passed_tests + evaluation.failed_tests
        puntuacion = (evaluation.passed_tests / total_tests) * 10 if total_tests > 0 else 0
        
        print(f"Pruebas exitosas: {evaluation.passed_tests}/{total_tests}")
        print(f"Puntuación: {puntuacion:.1f}/10")
        print(f"Estado: {'[APROBADO]' if evaluation.failed_tests == 0 else '[REPROBADO]'}")
        
        # Mostrar errores si los hay
        if evaluation.errors:
            print("\nErrores encontrados:")
            for test_name, error in evaluation.errors:
                print(f"- {test_name}: {error}")
        
        if evaluation.failed_tests > 0:
            print("\n[ADVERTENCIA] El agente no pasó todas las pruebas. Se recomienda revisar y mejorar el código.")
        else:
            print("\n[ÉXITO] ¡Agente creado y evaluado exitosamente!")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Error al crear o evaluar el agente: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
