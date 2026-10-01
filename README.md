# 🤖 Introducción a Agentes de IA con LangChain

Este repositorio contiene ejemplos y recursos para aprender sobre el desarrollo de agentes de IA utilizando LangChain. Incluye implementaciones que demuestran conceptos clave en el desarrollo de aplicaciones con modelos de lenguaje, como generación de texto, manejo de historial de conversación y streaming de respuestas en tiempo real.

## 🚀 Características

- Generación de texto con modelos de lenguaje
- Chat con historial de conversación
- Procesamiento de respuestas en formato JSON
- Chat en tiempo real con streaming de respuestas
- Integración con múltiples proveedores de modelos (OpenAI, HuggingFace, Google)

## 📋 Requisitos

- Python 3.8 o superior
- Cuenta con API key para los servicios de IA (OpenAI, Google, etc.)
- Dependencias listadas en `requirements.txt`

## 🛠️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/juanfeds/intro_agentes_ai.git
   cd intro_agentes_ai
   ```

2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crea un archivo `.env` en la raíz del proyecto con tus claves de API:
   ```
   OPENAI_API_KEY=tu_clave_aqui
   # Otras variables de entorno según sea necesario
   ```

## 🚀 Uso

El proyecto incluye varios scripts de ejemplo que puedes ejecutar. El más reciente es un chat con streaming en tiempo real:

```bash
python run.py
```

## 📂 Estructura del Proyecto

```
.
├── scripts/           # Scripts de ejemplo
│   ├── basic_gen_text.py      # Generación básica de texto
│   ├── chat_history.py        # Manejo de historial de chat
│   ├── streaming_chat.py      # Chat con streaming en tiempo real
│   └── ...
├── notebooks/         # Jupyter notebooks con ejemplos
├── data/              # Datos de ejemplo
├── src/               # Código fuente del proyecto
├── .env               # Variables de entorno
├── requirements.txt   # Dependencias
└── run.py            # Punto de entrada principal
```

## 🕸️ LangGraph

La carpeta [`langgraph/`](./langgraph/) tiene notebooks (grafos, agentes, mensajes, RAG, structured output y tools) y agentes construidos con LangGraph: conversación, extracción, reservas y soporte. Es un proyecto independiente con su propio `pyproject.toml` (uv).

## 📚 Recursos

- [Documentación de LangChain](https://python.langchain.com/)
- [Documentación de OpenAI](https://platform.openai.com/docs)
- [Documentación de HuggingFace](https://huggingface.co/docs)

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📄 Licencia

[MIT](https://choosealicense.com/licenses/mit/)