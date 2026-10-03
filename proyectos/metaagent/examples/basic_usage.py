"""
Ejemplo básico de uso del constructor de agentes.

Este script muestra cómo crear un agente simple utilizando el AgentBuilder.
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(str(Path(__file__).parent.parent))

from core.agent_builder import AgentBuilder, AgentSpecification

def main():
    # Crear una especificación de agente
    spec = AgentSpecification(
        name="MiPrimerAgente",
        description="Un agente de ejemplo que demuestra el uso del constructor.",
        agent_type="base",
        requirements=["requests>=2.25.0", "python-dotenv>=0.19.0"],
        config={
            "api_endpoint": "https://api.ejemplo.com",
            "timeout_seconds": 30
        }
    )
    
    # Crear el constructor
    builder = AgentBuilder()
    
    # Construir el agente
    agent_path = builder.build(spec)
    
    print(f"✅ Agente generado en: {agent_path}")
    print("No olvides instalar las dependencias con:")
    print(f"pip install -r {agent_path.parent / 'requirements.txt'}")

if __name__ == "__main__":
    main()
