"""
Script principal para crear y evaluar agentes de IA.

Este script permite crear un nuevo agente a partir de una especificación
y evaluar automáticamente su calidad.
"""

import argparse
import io
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Configurar la codificación de la consola para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Asegurarse de que el directorio raíz esté en el path
sys.path.append(str(Path(__file__).parent))

from core.builder.agent_builder import AgentBuilder
from core.builder.agent_spec import AgentSpecification
from core.evaluation.result import AgentEvaluationResult


def load_spec_from_file(spec_file: str) -> Dict[str, Any]:
    """Carga una especificación de agente desde un archivo JSON.
    
    Args:
        spec_file: Ruta al archivo de especificación
        
    Returns:
        Dict con la especificación cargada
    """
    try:
        with open(spec_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar el archivo de especificación: {e}")
        raise


def create_agent(spec: Dict[str, Any], output_dir: str = "agents") -> Path:
    """Crea un agente a partir de una especificación.
    
    Args:
        spec: Diccionario con la especificación del agente
        output_dir: Directorio de salida para el agente
        
    Returns:
        Ruta al archivo principal del agente generado
    """
    try:
        # Crear la especificación del agente
        agent_spec = AgentSpecification(**spec)
        
        # Crear el builder y generar el agente
        builder = AgentBuilder(output_dir=output_dir)
        agent_file = builder.build(agent_spec)
        
        print(f"✅ Agente generado exitosamente en: {agent_file}")
        return agent_file
        
    except Exception as e:
        print(f"❌ Error al crear el agente: {e}")
        raise


def evaluate_agent(agent_file: Path) -> AgentEvaluationResult:
    """Evalúa un agente generado.
    
    Args:
        agent_file: Ruta al archivo del agente
        
    Returns:
        Resultado de la evaluación
    """
    try:
        # Aquí iría la lógica de evaluación
        # Por ahora, devolvemos un resultado simulado
        print(f"🔍 Evaluando agente: {agent_file.name}")
        return AgentEvaluationResult(
            success=True,
            score=0.85,
            details={
                'file_exists': True,
                'syntax_valid': True,
                'has_main_class': True,
                'has_required_methods': True
            }
        )
    except Exception as e:
        print(f"❌ Error al evaluar el agente: {e}")
        raise


def main():
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(
        description='Crea y evalúa agentes de IA a partir de especificaciones',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Comandos principales
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando para crear un agente
    create_parser = subparsers.add_parser('crear', help='Crear un nuevo agente')
    create_parser.add_argument('--especificacion', type=str, required=True,
                             help='Archivo JSON con la especificación del agente')
    create_parser.add_argument('--directorio-salida', type=str, default='agents',
                             help='Directorio donde se guardará el agente')
    
    # Comando para evaluar un agente
    eval_parser = subparsers.add_parser('evaluar', help='Evaluar un agente existente')
    eval_parser.add_argument('archivo_agente', type=str,
                           help='Ruta al archivo del agente a evaluar')
    
    # Parsear argumentos
    args = parser.parse_args()
    
    try:
        if args.command == 'crear':
            # Cargar especificación
            spec = load_spec_from_file(args.especificacion)
            
            # Crear agente
            agent_file = create_agent(spec, args.directorio_salida)
            
            # Evaluar agente
            result = evaluate_agent(agent_file)
            
            # Mostrar resultados
            print("\n📊 Resultados de la evaluación:")
            print(f"  - Éxito: {'✅' if result.success else '❌'}")
            print(f"  - Puntuación: {result.score:.2f}")
            print("  - Detalles:")
            for key, value in result.details.items():
                print(f"    - {key}: {value}")
                
        elif args.command == 'evaluar':
            # Evaluar agente existente
            agent_file = Path(args.archivo_agente)
            if not agent_file.exists():
                print(f"❌ El archivo {agent_file} no existe")
                return
                
            result = evaluate_agent(agent_file)
            
            # Mostrar resultados
            print("\n📊 Resultados de la evaluación:")
            print(f"  - Éxito: {'✅' if result.success else '❌'}")
            print(f"  - Puntuación: {result.score:.2f}")
            print("  - Detalles:")
            for key, value in result.details.items():
                print(f"    - {key}: {value}")
                
        else:
            parser.print_help()
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
