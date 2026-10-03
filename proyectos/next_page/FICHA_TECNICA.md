# Ficha técnica – Next_Page

## 1. Propósito y alcance
Prototipo de agentes LangChain orientado a experimentar con inferencia en cadena y almacenamiento de memorias conversacionales en disco (`memory.json`). Interfaz CLI enfocada en investigación rápida.

## 2. Arquitectura y componentes clave
- **Bucle principal:** `main.py` (recibe prompt del usuario, invoca agente principal y luego agente de memoria, persiste resultados).
- **Agente principal:** `agents/dummie_agent/agent.py` usa `ChatOpenAI` (gpt-3.5-turbo) y contexto extraído de memorias previas.
- **Agente de memoria:** `agents/memory_agent/agent.py` utiliza `ChatOpenAI` (gpt-4o-mini) con salida estructurada (Pydantic `Memory`).
- **Persistencia:** `memory.json` guarda historial de intenciones y evaluaciones.
- **Dependencias:** Declaradas en `pyproject.toml` (LangChain, LangGraph, dotenv).

## 3. Requisitos y despliegue
- Python ≥3.12.
- Instalar dependencias: `uv pip install -r requirements` (o `pip install -e .` si se usa `pyproject`).
- Variables de entorno: `OPENAI_API_KEY` (cargado con `dotenv`).
- Ejecución: `python main.py` y seguir prompts en consola.

## 4. Nivel de culminación
**Bajo-Medio.** El flujo CLI funciona pero carece de documentación, pruebas y manejo de errores robusto.

## 5. Evaluación objetiva
- **Funcionamiento:** ✓ Ejecutable en CLI; memoria persistente básica.
- **Documentación:** ✗ README vacío; no hay instrucciones ni ejemplos.
- **Pruebas:** ✗ No existen tests.
- **Observabilidad:** ✗ Sin logging ni métricas.

## 6. Riesgos y brechas
1. `memory.json` crece indefinidamente y puede corromperse si la sesión se interrumpe.
2. Falta validación de entradas (cadena vacía, interrupciones).
3. Dependencia directa de modelos OpenAI sin manejo de errores HTTP.

## 7. Recomendaciones
1. Documentar flujo, rutas de ejecución y propósito del experimento.
2. Agregar rotación o límite de tamaño para `memory.json` y fallback en caso de fallo de lectura.
3. Incorporar pruebas unitarias para serialización de memoria y prompts.
4. Considerar migración a interfaz web ligera (por ejemplo, FastAPI + frontend simple) para mejorar UX.

## 8. Próximos pasos sugeridos
- Añadir soporte para perfiles de usuario y segmentación de memorias.
- Integrar LangGraph para visualización del flujo de agentes.
- Implementar configuración YAML para seleccionar modelos y temperaturas sin editar código.
