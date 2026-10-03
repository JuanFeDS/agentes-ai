"""Módulo para evaluar agentes usando modelos de lenguaje."""

import json
import os
from typing import Dict, Any, Optional
import openai
from dotenv import load_dotenv

from .exceptions import LLMEvaluationError

# Cargar variables de entorno
load_dotenv()

class LLMEvaluator:
    """Evaluador de agentes usando modelos de lenguaje."""
    
    def __init__(self, model: str = "gpt-4-turbo"):
        """Inicializa el evaluador LLM.
        
        Args:
            model: Nombre del modelo a utilizar.
        """
        self.model = model
        self._setup_openai()
    
    def _setup_openai(self) -> None:
        """Configura la API de OpenAI."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no encontrada en las variables de entorno")
        openai.api_key = api_key
    
    def evaluate(
        self, 
        agent_description: str, 
        output: str, 
        criteria: str
    ) -> Dict[str, Any]:
        """Evalúa la salida de un agente usando un modelo de lenguaje.
        
        Args:
            agent_description: Descripción del agente.
            output: Salida del agente a evaluar.
            criteria: Criterios de evaluación.
            
        Returns:
            Resultado de la evaluación.
            
        Raises:
            LLMEvaluationError: Si hay un error en la evaluación.
        """
        try:
            # Preparar el prompt
            prompt = self._build_prompt(agent_description, output, criteria)
            
            # Llamar a la API de OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Procesar la respuesta
            result_text = response.choices[0].message['content'].strip()
            return self._parse_response(result_text)
            
        except Exception as e:
            raise LLMEvaluationError(f"Error en la evaluación LLM: {str(e)}")
    
    def _build_prompt(
        self, 
        agent_description: str, 
        output: str, 
        criteria: str
    ) -> str:
        """Construye el prompt para la evaluación.
        
        Args:
            agent_description: Descripción del agente.
            output: Salida del agente.
            criteria: Criterios de evaluación.
            
        Returns:
            Prompt formateado.
        """
        return f"""Evalúa la siguiente salida de un agente según los criterios proporcionados.

Descripción del agente:
{agent_description}

Salida a evaluar:
```
{output}
```

Criterios de evaluación:
{criteria}

Por favor, proporciona una evaluación en formato JSON con los siguientes campos:
- score: Puntuación del 0 al 100
- reasoning: Razonamiento detallado
- strengths: Lista de fortalezas
- weaknesses: Lista de debilidades
- suggestions: Lista de sugerencias de mejora

Respuesta en formato JSON:"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parsea la respuesta del modelo de lenguaje.
        
        Args:
            response_text: Texto de respuesta del modelo.
            
        Returns:
            Diccionario con la evaluación.
            
        Raises:
            LLMEvaluationError: Si no se puede parsear la respuesta.
        """
        try:
            # Intentar extraer el JSON de la respuesta
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No se encontró un objeto JSON en la respuesta")
                
            json_str = response_text[json_start:json_end]
            return json.loads(json_str)
            
        except json.JSONDecodeError as e:
            raise LLMEvaluationError(f"Error al parsear la respuesta JSON: {str(e)}")
        except Exception as e:
            raise LLMEvaluationError(f"Error al procesar la respuesta: {str(e)}")
