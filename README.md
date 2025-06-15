# AIstract

AIstract es una aplicación para resumir y analizar documentos académicos utilizando inteligencia artificial.

## Características

- Resumen automático de documentos académicos
- Respuesta a preguntas sobre el contenido de los documentos
- Interfaz web amigable con Streamlit
- Almacenamiento vectorial para búsqueda semántica

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/JuanFeDS/aistract.git
cd aistract
```

2. Crea un entorno virtual y activa:
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura las variables de entorno:
- Copia el archivo `.env.example` a `.env`
- Configura tus claves de API en `.env`

## Uso

Para ejecutar la aplicación web:
```bash
streamlit run web/streamlit_app.py
```

## Estructura del Proyecto

```
aistract/
├── app/                        # Lógica principal
│   ├── agents/                 # Agentes LangChain
│   ├── chains/                 # Cadenas de LangChain
│   ├── tools/                  # Herramientas personalizadas
│   ├── loaders/                # Cargadores de documentos
│   ├── vectorstores/          # Almacenamiento vectorial
│   ├── prompts/               # Plantillas de prompts
│   └── utils/                 # Utilidades
├── web/                       # Interfaz de usuario
├── data/                      # Documentos y datos
├── .env                       # Variables de entorno
├── requirements.txt           # Dependencias
└── README.md                  # Este archivo
```

## Licencia

MIT
