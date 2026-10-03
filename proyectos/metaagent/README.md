# MetaAgent 🛠️

MetaAgent es un sistema diseñado para la generación automática de agentes de IA. Permite definir especificaciones de agentes en términos de sus capacidades, comportamientos y requisitos, generando automáticamente el código fuente correspondiente.

## Características principales

- 🏗️ Generación de código de agentes a partir de especificaciones
- 🧩 Soporte para diferentes tipos de agentes (base, reactivos, de aprendizaje, etc.)
- 🧪 Validación de especificaciones mediante esquemas Pydantic
- 📦 Empaquetado automático con dependencias
- 📝 Documentación automática
- 🧪 Sistema de evaluación integrado

## Estructura del Proyecto

```
MetaAgent/
├── agents/                   # Agentes generados
├── core/                     # Núcleo del sistema
│   ├── agent_builder.py     # Constructor principal de agentes
│   ├── agent_evaluator.py   # Evaluador de agentes
│   └── templates/           # Plantillas de agentes
├── schemas/                 # Esquemas de validación
├── utils/                   # Utilidades varias
├── tests/                   # Pruebas unitarias
├── examples/                # Ejemplos de uso
├── .env                     # Variables de entorno
├── requirements.txt         # Dependencias
└── README.md               # Documentación principal
```

## Componentes Principales

### 1. AgentBuilder

El núcleo del sistema, ubicado en `core/agent_builder.py`, proporciona la funcionalidad para crear agentes a partir de especificaciones.

#### Clases Principales:

1. **`AgentSpecification`**
   - Modelo Pydantic para validar las especificaciones del agente
   - Campos:
     - `name`: Nombre único del agente
     - `description`: Descripción detallada
     - `agent_type`: Tipo de agente (base, reactive, learning, etc.)
     - `requirements`: Lista de dependencias
     - `config`: Configuración específica del agente

2. **`AgentBuilder`**
   - Clase principal para generar agentes
   - Métodos:
     - `__init__(output_dir="agents")`: Inicializa el constructor
     - `build(spec)`: Construye el agente a partir de una especificación
     - `_generate_agent_code(spec)`: Genera el código fuente (método interno)

### 2. AgentEvaluator

Ubicado en `core/agent_evaluator.py`, proporciona funcionalidad para evaluar los agentes generados.

## Uso Básico

### Creación de un Agente

```python
from core.agent_builder import AgentBuilder, AgentSpecification

# 1. Definir la especificación del agente
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

# 2. Crear el constructor
builder = AgentBuilder(output_dir="mis_agentes")

# 3. Construir el agente
agent_path = builder.build(spec)

print(f"✅ Agente generado en: {agent_path}")
```

### Evaluación de Agentes

```python
from core.agent_evaluator import AgentEvaluator

# 1. Crear evaluador
evaluator = AgentEvaluator(agents_dir="mis_agentes")

# 2. Evaluar todos los agentes
results = evaluator.evaluate_all_agents()

# 3. Mostrar resultados
for result in results:
    print(f"Agente: {result.agent_name}, Puntaje: {result.score}%")
```

## Plantillas de Agentes

El sistema utiliza plantillas para generar el código fuente de los agentes. Actualmente, el sistema genera un esqueleto básico del agente, pero puede extenderse para soportar diferentes tipos de agentes.

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt`

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd metaagent

# Crear y activar entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Próximos Pasos

1. **Ampliar las plantillas** para diferentes tipos de agentes
2. **Implementar validaciones** más completas en los esquemas
3. **Añadir pruebas unitarias** para garantizar la calidad del código
4. **Crear documentación detallada** de la API
5. **Implementar un sistema de plugins** para extender funcionalidades

## Contribución

Las contribuciones son bienvenidas. Por favor, sigue el estándar de código del proyecto y asegúrate de que todas las pruebas pasen antes de enviar un pull request.

## Licencia

[Incluir información sobre la licencia]
   pip install -r requirements.txt
   ```

## Uso básico

Consulta el archivo `examples/basic_usage.py` para ver un ejemplo de cómo crear un agente simple.

## Contribución

Las contribuciones son bienvenidas. Por favor, lee las pautas de contribución antes de enviar pull requests.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
