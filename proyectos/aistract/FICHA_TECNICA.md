# Ficha técnica – AIstract

## 1. Propósito y alcance
Aplicación web para resumir y analizar papers académicos mediante LangChain y modelos OpenAI, orientada a investigadores que necesitan síntesis rápidas.

## 2. Arquitectura y componentes clave
- **Frontend:** Streamlit (`web/streamlit_app.py`).
- **Procesamiento:** Cargadores de PDF con PyMuPDF, segmentación y cadena de resumen map-reduce (`app/chains/summary_chain.py`).
- **LLM:** `ChatOpenAI` (gpt-3.5-turbo por defecto).
- **Persistencia:** No requiere base de datos; opera en memoria con archivos cargados.

## 3. Requisitos y despliegue
- Python ≥3.9.
- Dependencias en `requirements.txt` (Streamlit, LangChain, PyMuPDF, OpenAI, etc.).
- Variables de entorno: `OPENAI_API_KEY` en `.env`.
- Ejecución local: `streamlit run web/streamlit_app.py` tras activar el entorno virtual.

## 4. Nivel de culminación
**Alto.** El flujo extremo a extremo (carga de PDF → resumen) está implementado y probado manualmente.

## 5. Evaluación objetiva
- **Funcionamiento:** ✓ Interfaz operativa y cadena de resumen funcional.
- **Documentación:** ✓ README con instalación/uso; falta guía de despliegue productivo.
- **Pruebas:** ✗ No hay pruebas automatizadas.
- **Observabilidad:** ✗ Sin métricas ni logging estructurado.

## 6. Riesgos y brechas
1. Costos de tokens y latencia sin monitoreo.
2. Falta manejo de documentos muy extensos (riesgo de límite de tokens).
3. Ausencia de validaciones de formato y tamaño al cargar PDFs.

## 7. Recomendaciones
1. Incorporar paginación y prevalidación de archivos grandes.
2. Añadir pruebas unitarias para el pipeline de resumen y el cargador de PDFs.
3. Implementar modo batch/offline y logging de consumo de tokens.

## 8. Próximos pasos sugeridos
- Diseñar script de despliegue (Docker/Heroku) para facilitar demos.
- Evaluar modelos alternativos (gpt-4o, Llama) con métricas de calidad.
- Añadir almacenamiento opcional de resúmenes (por ejemplo, SQLite o vectores).
