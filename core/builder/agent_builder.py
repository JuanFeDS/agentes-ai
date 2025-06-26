"""
Módulo principal para la construcción de agentes.

Este módulo proporciona la funcionalidad principal para generar agentes
a partir de especificaciones dadas usando la API de OpenAI.
"""

import os
import json
import openai
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel, Field

# Cargar variables de entorno
load_dotenv()

# Configurar la API de OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY no está configurada en las variables de entorno")

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=api_key)


class AgentSpecification(BaseModel):
    """Especificación para la creación de un agente."""
    
    name: str = Field(..., description="Nombre único del agente")
    description: str = Field(..., description="Descripción detallada del agente")
    agent_type: str = Field(
        default="base",
        description="Tipo de agente a crear (base, reactive, learning, etc.)"
    )
    requirements: list[str] = Field(
        default_factory=list,
        description="Lista de dependencias requeridas"
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuración específica del agente"
    )


class AgentBuilder:
    """Constructor de agentes.
    
    Esta clase se encarga de generar el código fuente de un agente
    a partir de una especificación dada.
    """
    
    def __init__(self, output_dir: str = "agents"):
        """Inicializa el constructor de agentes.
        
        Args:
            output_dir: Directorio donde se guardarán los agentes generados
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def build(self, spec: AgentSpecification) -> Path:
        """Construye un agente a partir de una especificación.
        
        Args:
            spec: Especificación del agente a construir
            
        Returns:
            Ruta al archivo principal del agente generado
        """
        # Crear directorio para el agente
        agent_dir = self.output_dir / spec.name.lower().replace(" ", "_")
        agent_dir.mkdir(exist_ok=True)
        
        # Crear archivo principal del agente
        agent_file = agent_dir / f"{spec.name.lower().replace(' ', '_')}.py"
        
        # Generar código del agente (esto se implementará más adelante)
        agent_code = self._generate_agent_code(spec)
        
        # Escribir el archivo
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(agent_code)
        
        # Crear requirements.txt si hay dependencias
        if spec.requirements:
            with open(agent_dir / 'requirements.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(spec.requirements))
        
        return agent_file
    
    def _generate_agent_code(self, spec: AgentSpecification) -> str:
        """Genera el código fuente del agente usando la API de OpenAI.
        
        Args:
            spec: Especificación del agente
            
        Returns:
            Código fuente del agente generado por la API
            
        Raises:
            RuntimeError: Si hay un error al generar el código con la API
        """
        # Crear el prompt para la API de OpenAI
        prompt = f"""
        Necesito que generes el código Python para un agente de IA con las siguientes especificaciones:
        
        Nombre: {spec.name}
        Tipo: {spec.agent_type}
        Descripción: {spec.description}
        
        Requisitos: {', '.join(spec.requirements) if spec.requirements else 'Ninguno'}
        Configuración: {json.dumps(spec.config, indent=2) if spec.config else 'Ninguna'}
        
        El código debe incluir:
        1. Una clase principal con el nombre del agente (usando notación PascalCase)
        2. Métodos relevantes según el tipo de agente
        3. Documentación adecuada
        4. Manejo de errores básico
        5. Un ejemplo de uso en el bloque if __name__ == "__main__"
        
        Por favor, devuelve SOLO el código Python sin marcas de código o explicaciones adicionales.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en programación Python que genera código de agentes de IA. Genera SOLO el código Python sin explicaciones adicionales."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extraer y limpiar el código generado
            code = response.choices[0].message.content.strip()
            
            # Eliminar marcas de código si existen
            if code.startswith('```python'):
                code = code[9:].strip()
            if code.startswith('```'):
                code = code[3:].strip()
            if code.endswith('```'):
                code = code[:-3].strip()
                
            return code
            
        except Exception as e:
            raise RuntimeError(f"Error al generar el código del agente con la API de OpenAI: {str(e)}")
