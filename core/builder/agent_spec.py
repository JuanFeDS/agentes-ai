"""Módulo que define la especificación de un agente."""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class AgentSpecification(BaseModel):
    """Especificación detallada para la creación de un agente.
    
    Attributes:
        name: Nombre único del agente (en formato PascalCase)
        description: Descripción detallada del propósito y funcionalidad
        agent_type: Tipo de agente (ej: 'analytics', 'assistant', 'automation')
        requirements: Lista de dependencias de Python requeridas
        config: Configuración específica del agente
        input_schema: Esquema de entrada esperado por el agente
        output_schema: Esquema de salida generado por el agente
        examples: Ejemplos de uso del agente
        methods: Lista de métodos principales que debe implementar el agente
    """
    
    name: str = Field(..., min_length=3, max_length=50, 
                      description="Nombre único del agente en PascalCase")
    description: str = Field(..., min_length=20, 
                           description="Descripción detallada del propósito y funcionalidad del agente")
    agent_type: str = Field(
        default="base",
        description="Tipo de agente (ej: 'analytics', 'assistant', 'automation')"
    )
    requirements: List[str] = Field(
        default_factory=lambda: ["pandas>=1.3.0", "numpy>=1.21.0"],
        description="Lista de dependencias de Python requeridas"
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuración específica del agente"
    )
    input_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Esquema de entrada esperado por el agente (opcional)"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Esquema de salida generado por el agente (opcional)"
    )
    examples: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Ejemplos de uso del agente (opcional)"
    )
    methods: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Lista de métodos principales que debe implementar el agente"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "name": "AnalizadorDatos",
                "description": "Agente para análisis de datos que limpia y procesa conjuntos de datos",
                "agent_type": "analytics",
                "requirements": ["pandas", "numpy", "matplotlib"],
                "config": {
                    "version": "1.0.0",
                    "max_rows": 10000
                },
                "methods": [
                    {
                        "name": "cargar_datos",
                        "description": "Carga datos desde una ruta de archivo",
                        "parameters": {"ruta_archivo": "str"},
                        "return_type": "pd.DataFrame"
                    },
                    {
                        "name": "limpiar_datos",
                        "description": "Limpia los datos cargados",
                        "parameters": {"df": "pd.DataFrame"},
                        "return_type": "pd.DataFrame"
                    }
                ]
            }
        }
