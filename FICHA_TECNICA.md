# Ficha técnica – MetaAgent

## 1. Propósito y alcance
Framework para generar agentes de IA a partir de especificaciones declarativas (Pydantic). Automatiza creación de código, empaquetado y evaluación básica de agentes con múltiples plantillas.

## 2. Arquitectura y componentes clave
- **Core:** `core/meta_agent.py`, `core/builder/`, `core/agents/`, `core/evaluation/` contienen el motor de construcción, plantillas y evaluador.
- **Schemas:** Validaciones en `schemas/` con modelos Pydantic (`AgentSpecification`, etc.).
- **Utils:** Manejo de archivos, render de plantillas, helpers (`utils/`).
- **Examples/tests:** Carpeta `examples/` y `tests/` para casos de uso (pendiente revisar cobertura real).

## 3. Requisitos y despliegue
- Python ≥3.9.
- Dependencias listadas en `requirements.txt` (pydantic, typer, rich, etc.).
- Variables opcionales en `.env` para configuraciones runtime.
- Uso típico: definir especificación en `specs/`, ejecutar `python run.py --spec specs/demo.yaml` (según CLI descrita en README/change log).

## 4. Nivel de culminación
**Medio.** Núcleo implementado y documentado; faltan instrucciones finales (el README aún tiene placeholders) y validación práctica de output.

## 5. Evaluación objetiva
- **Funciones principales:** ✓ Builder/Evaluator presentes.
- **Documentación:** △ README completo pero con secciones por completar (licencia placeholder, URL repo). Change log detallado.
- **Pruebas:** △ Carpeta `tests/` existe; no se evidenció ejecución ni CI.
- **Observabilidad:** ✗ Sin métricas ni logging estructurado.

## 6. Riesgos y brechas
1. Falta de guía paso a paso para crear el primer agente.
2. Dependencia de plantillas internas sin validación externa.
3. No hay publicación en PyPI ni versión semántica.

## 7. Recomendaciones
1. Completar README con instrucciones de CLI, ejemplos y licencia.
2. Añadir pruebas unitarias para builder y evaluator (mockear plantillas).
3. Documentar estructura de directorios generados y compatibilidad con otros frameworks.

## 8. Próximos pasos sugeridos
- Crear especificación de ejemplo con agente funcional y compartir resultado.
- Integrar pipeline CI (lint + tests) y publicación automática.
- Explorar soporte para múltiples proveedores LLM (OpenAI, Anthropic) vía adaptadores.
