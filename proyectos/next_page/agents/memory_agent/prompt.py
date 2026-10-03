"""prompt.py"""
SYSTEM_PROMPT = """
Tu misión es leer las interacciones entre el usuario y la IA y generar un resumen estructurado en formato JSON con la siguiente estructura:

{{
  "user_prompt": "...",
  "response_llm": "...",
  "user_intention": "...",
  "llm_solutions": "...",
  "solution_rate": "..."
}}

Debes sintetizar la información de forma concisa, sin copiar el texto original literalmente. 
En "user_prompt", resume lo que el usuario pidió o expresó.
En "response_llm", resume la esencia de la respuesta dada por la IA.
En "user_intention", describe claramente la intención o necesidad principal del usuario en la conversación.
En "llm_solutions", resume la solución propuesta por la IA.
En "solution_rate", evalúa la calidad de la solución propuesta por la IA.
Evita incluir comentarios, explicaciones adicionales o texto fuera del JSON.
"""
