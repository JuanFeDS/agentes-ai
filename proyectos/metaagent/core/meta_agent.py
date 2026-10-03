"""Módulo principal para la generación de agentes usando IA.

Este módulo proporciona funcionalidad para generar agentes usando modelos de lenguaje
de OpenAI, integrando con el sistema de construcción de agentes.
"""

import os
import re
from typing import Optional, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

from .agent_builder import AgentBuilder, AgentSpecification
from .agent_evaluator import AgentEvaluator

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class MetaAgent(AgentBuilder):
    """Meta-agente que utiliza IA para generar agentes personalizados.
    
    Hereda de AgentBuilder y añade capacidades de generación de código
    utilizando modelos de lenguaje de OpenAI.
    """
    
    def __init__(self, output_dir: str = "agents"):
        """Inicializa el meta-agente.
        
        Args:
            output_dir: Directorio donde se guardarán los agentes generados
        """
        super().__init__(output_dir)
        self.model = "gpt-4"  # Modelo por defecto
        self.temperature = 0.2  # Temperatura para la generación
    
    def generate_agent(
        self,
        name: str,
        description: str,
        agent_type: str = "base",
        requirements: Optional[list[str]] = None,
        config: Optional[Dict[str, Any]] = None
    ) -> str:
        """Genera un agente usando IA a partir de una descripción.
        
        Args:
            name: Nombre del agente
            description: Descripción detallada de la funcionalidad del agente
            agent_type: Tipo de agente (base, reactive, learning, etc.)
            requirements: Lista de dependencias requeridas
            config: Configuración adicional para el agente
            
        Returns:
            Ruta al archivo principal del agente generado
        """
        # Crear especificación del agente
        spec = AgentSpecification(
            name=name,
            description=description,
            agent_type=agent_type,
            requirements=requirements or [],
            config=config or {}
        )
        
        # Generar el agente
        agent_path = self.build(spec)
        
        # Evaluar el agente generado
        evaluator = AgentEvaluator()
        result = evaluator.evaluate_agent(agent_path)
        
        # Mostrar resultados de la evaluación
        print("\n" + "="*50)
        print("EVALUACIÓN DEL AGENTE GENERADO")
        print("="*50)
        print(result)
        print("="*50 + "\n")
        
        return str(agent_path)
    
    def _generate_agent_code(self, spec: AgentSpecification) -> str:
        """Genera el código del agente usando OpenAI.
        
        Args:
            spec: Especificación del agente
            
        Returns:
            Código fuente del agente generado
        """
        # Crear prompt para la generación de código
        prompt = self._build_generation_prompt(spec)
        
        try:
            # Llamar a la API de OpenAI
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en generación de agentes en Python."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature
            )
            
            # Extraer y limpiar el código generado
            code = response.choices[0].message.content
            if code is None:
                raise ValueError("No se recibió código generado de la API")
                
            return self._clean_generated_code(code)
            
        except Exception as e:
            raise RuntimeError(f"Error al generar el agente: {str(e)}")
    
    def _build_generation_prompt(self, spec: AgentSpecification) -> str:
        """Construye el prompt para la generación de código.
        
        Args:
            spec: Especificación del agente
            
        Returns:
            Prompt detallado para la generación de código
        """
        return f"""
        Eres un generador experto de agentes Python. Tu tarea es crear un agente con las siguientes características:
        
        Nombre: {spec.name}
        Tipo: {spec.agent_type}
        Descripción: {spec.description}
        
        Requisitos:
        - El código debe estar bien estructurado y seguir las mejores prácticas de Python
        - Incluir manejo de errores apropiado
        - Documentar todas las funciones y clases
        - Incluir ejemplos de uso si es necesario
        
        Si el agente requiere conexión a base de datos:
        - Usar SQLAlchemy para ORM
        - Incluir configuración de conexión en una clase de configuración
        
        Si el agente procesa datos:
        - Incluir validación de datos
        - Usar pandas o numpy según sea necesario
        
        Devuelve SOLO el código Python, sin marcas de código ni explicaciones adicionales.
        """
    
    def _clean_generated_code(self, code: str) -> str:
        """Limpia el código generado por el modelo.
        
        Args:
            code: Código generado por el modelo
            
        Returns:
            Código limpio y listo para guardar
        """
        # Eliminar marcas de código markdown si existen
        code = re.sub(r'```(?:python\n)?|```', '', code).strip()
        return code


def main():
    """Función principal para uso desde línea de comandos."""
    print("🛠️  MetaAgent - Generador de Agentes con IA\n")
    
    name = input("Nombre del agente: ")
    description = input("\nDescribe la funcionalidad del agente: \n> ")
    
    agent = MetaAgent()
    try:
        agent_path = agent.generate_agent(name, description)
        print(f"\n✅ Agente generado exitosamente en: {agent_path}")
    except Exception as e:
        print(f"\n❌ Error al generar el agente: {str(e)}")


if __name__ == "__main__":
    main()
