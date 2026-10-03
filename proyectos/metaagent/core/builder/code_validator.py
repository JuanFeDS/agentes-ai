"""Módulo para validar código Python generado."""
import ast
from typing import Optional


class CodeValidator:
    """Validador de código Python."""
    
    @staticmethod
    def validate_syntax(code: str) -> None:
        """Valida que el código tenga sintaxis Python válida.
        
        Args:
            code: Código fuente a validar
            
        Raises:
            ValueError: Si el código tiene errores de sintaxis
        """
        try:
            ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Error de sintaxis en el código generado: {str(e)}")
    
    @staticmethod
    def clean_generated_code(code: str) -> str:
        """Limpia el código generado eliminando marcas de código y texto explicativo.
        
        Args:
            code: Código generado por el modelo
            
        Returns:
            str: Código limpio y listo para guardar
        """
        # Eliminar bloques de código markdown
        if '```python' in code:
            code = code.split('```python', 1)[1]
        if '```' in code:
            code = code.split('```', 1)[0]
        
        # Eliminar líneas que no son código (comentarios al inicio)
        lines = []
        code_started = False
        for line in code.splitlines():
            if not code_started and (line.strip().startswith('import ') or 
                                    line.strip().startswith('class ') or 
                                    line.strip().startswith('def ')):
                code_started = True
            if code_started:
                lines.append(line)
        
        return '\n'.join(lines).strip()
