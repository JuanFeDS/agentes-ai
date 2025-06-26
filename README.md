# MetaAgent 🛠️

MetaAgent es un sistema para la generación automática de agentes de IA. Permite definir especificaciones de agentes en términos de sus capacidades, comportamientos y requisitos, y genera automáticamente el código fuente correspondiente.

## Características principales

- 🏗️ Generación de código de agentes a partir de especificaciones
- 🧩 Soporte para diferentes tipos de agentes (base, reactivos, de aprendizaje, etc.)
- 🧪 Validación de especificaciones
- 📦 Empaquetado automático con dependencias
- 📝 Documentación automática

## Estructura del proyecto

```
MetaAgent/
├── agents/                   # Agentes generados
├── core/                     # Núcleo del sistema
│   ├── templates/           # Plantillas de agentes
│   └── validators/          # Validadores de especificaciones
├── schemas/                  # Esquemas Pydantic
├── utils/                    # Utilidades varias
├── tests/                    # Pruebas unitarias
├── examples/                 # Ejemplos de uso
├── .env                      # Variables de entorno
├── requirements.txt          # Dependencias
└── README.md                # Este archivo
```

## Requisitos

- Python 3.8+
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/metaagent.git
   cd metaagent
   ```

2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: .\venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso básico

Consulta el archivo `examples/basic_usage.py` para ver un ejemplo de cómo crear un agente simple.

## Contribución

Las contribuciones son bienvenidas. Por favor, lee las pautas de contribución antes de enviar pull requests.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
