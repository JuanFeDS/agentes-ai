"""Módulo para la generación de código de agentes."""
import json
from typing import Dict, Any

from openai import OpenAI

from .agent_spec import AgentSpecification


class CodeGenerator:
    """Generador de código para agentes usando OpenAI."""
    
    def __init__(self, client: OpenAI):
        """Inicializa el generador de código.
        
        Args:
            client: Cliente de OpenAI configurado
        """
        self.client = client
    
    def generate_agent_code(self, spec: AgentSpecification) -> str:
        """Genera el código fuente del agente.
        
        Args:
            spec: Especificación del agente
            
        Returns:
            str: Código fuente generado
            
        Raises:
            RuntimeError: Si hay un error al generar el código
        """
        prompt = self._build_prompt(spec)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un ingeniero de software senior especializado en arquitectura de agentes de IA.
                        Genera código Python limpio, bien documentado y listo para producción.
                        Incluye solo el código, sin explicaciones adicionales."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000,
                top_p=0.95,
                frequency_penalty=0.2,
                presence_penalty=0.2
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise RuntimeError(f"Error al generar el código del agente: {str(e)}")
    
    def _build_prompt(self, spec: AgentSpecification) -> str:
        """Construye el prompt para la generación de código.
        
        Args:
            spec: Especificación del agente
            
        Returns:
            str: Prompt detallado para el modelo
        """
        methods_str = '\n'.join([
            f"- {m['name']}: {m.get('description', 'Sin descripción')} "
            f"(params: {m.get('parameters', 'Ninguno')}, "
            f"returns: {m.get('return_type', 'None')})"
            for m in spec.methods
        ]) if spec.methods else "No se especificaron métodos"
        
        config_json = json.dumps(spec.config, indent=2, ensure_ascii=False)
        requirements_str = '\n'.join(spec.requirements) if spec.requirements else 'No se especificaron requisitos'
        
        return f"""
        # Tarea: Generación de Agente de IA
        
        ## Especificaciones del Agente
        - **Nombre**: {spec.name}
        - **Tipo**: {spec.agent_type}
        - **Descripción**: {spec.description}
        
        ## Configuración
        ```json
        {config_json}
        ```
        
        ## Métodos Requeridos
        {methods_str}
        
        ## Requisitos
        ```
        {requirements_str}
        ```
        
        ## Instrucciones de Implementación
        1. Crea una clase Python llamada `{spec.name}`
        2. Implementa los métodos especificados
        3. Incluye documentación detallada (docstrings)
        4. Agrega manejo de errores adecuado
        5. Incluye logging para seguimiento
        6. Agrega un ejemplo de uso en `if __name__ == "__main__"`
        
        ## Restricciones
        - Usa type hints
        - Sigue PEP 8
        - Incluye validación de entradas/salidas
        - Documenta los parámetros y valores de retorno
        
        ## Ejemplo de Estructura Esperada
        ```python
        class {spec.name}:
            \"\"\"{spec.description}\"\"\"
            
            def __init__(self, **config):
                \"\"\"Inicializa el agente con la configuración proporcionada.\"\"\"
                self.config = config
                self._setup()
            
            def _setup(self):
                \"\"\"Configuración inicial del agente.\"\"\"
                pass
            
            # Métodos requeridos aquí...
        ```
        """
