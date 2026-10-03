"""
Módulo principal para la construcción de agentes.

Este módulo proporciona la funcionalidad principal para generar agentes
a partir de especificaciones dadas, utilizando servicios de generación de código.
"""

import os
from pathlib import Path
from typing import Optional
from openai import OpenAI

from .agent_spec import AgentSpecification
from .code_generator import CodeGenerator
from .code_validator import CodeValidator


class AgentBuilder:
    """Constructor de agentes.
    
    Esta clase orquesta el proceso de generación de un agente,
    coordinando la generación de código, validación y creación de archivos.
    """
    
    def __init__(self, output_dir: str = "agents"):
        """Inicializa el constructor de agentes.
        
        Args:
            output_dir: Directorio donde se guardarán los agentes generados
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Configurar cliente de OpenAI
        self._setup_openai()
        
        # Inicializar servicios
        self.code_generator = CodeGenerator(self.client)
        self.validator = CodeValidator()
    
    def _setup_openai(self) -> None:
        """Configura el cliente de OpenAI."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY no está configurada en las variables de entorno"
            )
        self.client = OpenAI(api_key=api_key)
    
    def build(self, spec: AgentSpecification) -> Path:
        """Construye un agente a partir de una especificación.
        
        Args:
            spec: Especificación del agente a construir
            
        Returns:
            Path: Ruta al archivo principal del agente generado
            
        Raises:
            ValueError: Si hay errores en la generación o validación
            RuntimeError: Si hay errores de E/S
        """
        try:
            # 1. Generar el código del agente
            agent_code = self.code_generator.generate_agent_code(spec)
            
            # 2. Validar el código generado
            self.validator.validate_syntax(agent_code)
            
            # 3. Limpiar el código
            clean_code = self.validator.clean_generated_code(agent_code)
            
            # 4. Crear directorio para el agente
            agent_dir = self._create_agent_directory(spec.name)
            
            # 5. Guardar el código del agente
            agent_file = self._save_agent_code(agent_dir, spec.name, clean_code)
            
            # 6. Guardar requirements.txt si es necesario
            self._save_requirements(agent_dir, spec.requirements)
            
            return agent_file
            
        except Exception as e:
            raise RuntimeError(f"Error al construir el agente: {str(e)}")
    
    def _create_agent_directory(self, agent_name: str) -> Path:
        """Crea el directorio para el agente.
        
        Args:
            agent_name: Nombre del agente
            
        Returns:
            Path: Ruta al directorio del agente
        """
        agent_dir = self.output_dir / agent_name.lower().replace(" ", "_")
        agent_dir.mkdir(exist_ok=True, parents=True)
        return agent_dir
    
    def _save_agent_code(self, agent_dir: Path, agent_name: str, code: str) -> Path:
        """Guarda el código del agente en un archivo.
        
        Args:
            agent_dir: Directorio del agente
            agent_name: Nombre del agente
            code: Código a guardar
            
        Returns:
            Path: Ruta al archivo guardado
        """
        agent_file = agent_dir / f"{agent_name.lower().replace(' ', '_')}.py"
        try:
            with open(agent_file, 'w', encoding='utf-8') as f:
                f.write(code)
            return agent_file
        except IOError as e:
            raise RuntimeError(f"Error al guardar el archivo del agente: {str(e)}")
    
    def _save_requirements(self, agent_dir: Path, requirements: list[str]) -> None:
        """Guarda los requisitos en un archivo requirements.txt si es necesario.
        
        Args:
            agent_dir: Directorio del agente
            requirements: Lista de dependencias
        """
        if requirements:
            try:
                with open(agent_dir / 'requirements.txt', 'w', encoding='utf-8') as f:
                    f.write('\n'.join(requirements))
            except IOError as e:
                # No es crítico si no se pueden guardar los requisitos
                print(f"Advertencia: No se pudieron guardar los requisitos: {str(e)}")
