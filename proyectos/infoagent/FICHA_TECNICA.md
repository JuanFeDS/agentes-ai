# Ficha técnica – infoagent

## 1. Propósito y alcance
Automatizar la ingesta periódica de papers desde el API de arXiv para construir un repositorio local de documentos (JSON) que luego puede usarse para análisis y generación de conocimiento.

## 2. Arquitectura y componentes clave
- **`main.py`:** Punto de entrada que carga variables de entorno y ejecuta `ingest_arxiv` con parámetros predefinidos.
- **`src/ingest.py`:** Función principal que consulta arXiv vía `feedparser`, normaliza los metadatos y guarda resultados en `data/raw`.
- **Datos:** Archivos JSON con timestamp y query en su nombre (`arxiv_<query>_<fecha>.json`).
- **Dockerfile:** Plantilla inicial para contenerizar el proceso (pendiente personalización).

## 3. Requisitos y despliegue
- Python ≥3.9.
- Dependencias en `requirements.txt` (feedparser, python-dotenv, etc.).
- Variables de entorno opcionales (p. ej. parámetros de consultas) definidas en `.env`.
- Ejecución: `python main.py` o importación del módulo `ingest_arxiv` para integrarlo en pipelines externos.

## 4. Nivel de culminación
**Medio.** La ingesta funciona; carece de pipeline de análisis posterior, pruebas y documentación en README.

## 5. Evaluación objetiva
- **Funcionamiento:** ✓ Descarga y persistencia operativa.
- **Documentación:** ✗ README vacío; se requiere guía de uso.
- **Pruebas:** ✗ No hay cobertura automatizada.
- **Escalabilidad:** △ Adecuado para lotes pequeños; no hay paralelización ni paginación.

## 6. Riesgos y brechas
1. Falta manejo de errores HTTP/timeout en llamadas a arXiv.
2. Almacena archivos sin control de tamaño ni limpieza histórica.
3. Sin verificación de duplicados ni pipeline analítico que consuma los datos.

## 7. Recomendaciones
1. Documentar CLI y parámetros (query, `max_results`, directorios).
2. Implementar reintentos y validaciones de respuesta antes de escribir en disco.
3. Añadir pruebas unitarias para el formateo de documentos y generar fixtures.
4. Diseñar módulo de análisis (p. ej. vector store + consultas) para completar el flujo.

## 8. Próximos pasos sugeridos
- Integrar con un orquestador (Airflow, Prefect o cron) para ejecuciones programadas.
- Generar reporte sintético después de cada ingesta (conteos, campos principales).
- Explorar almacenamiento en base de datos documental (MongoDB) o lago de datos.
