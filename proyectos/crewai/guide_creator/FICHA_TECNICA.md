# Ficha técnica – guide_creator (crewAI)

## 1. Propósito y alcance
Plantilla de flujo (Flow) basada en crewAI para coordinar agentes y tareas destinadas a crear guías o reportes personalizados. Es un punto de partida para diseñar procesos multiagente más complejos.

## 2. Arquitectura y componentes clave
- **Configuraciones:** `src/guide_creator/config/agents.yaml` y `tasks.yaml` describen roles y objetivos.
- **Orquestación:** `src/guide_creator/crew.py` implementa la lógica del flujo.
- **Entrypoint:** `src/guide_creator/main.py` / comando `crewai run`.
- **Repositorio de conocimiento:** `knowledge/` (personalizable) y outputs en `report.md`.

## 3. Requisitos y despliegue
- Python 3.10–3.13.
- Gestor `uv` (recomendado) o pip; dependencias en `pyproject.toml` + `uv.lock`.
- Variables en `.env` (llaves LLM, servicios externos).
- Ejecución estándar: `crewai run` desde el directorio raíz del proyecto.

## 4. Nivel de culminación
**Bajo.** Es la plantilla default sin adaptaciones concretas; requiere configuración específica de agentes y tareas.

## 5. Evaluación objetiva
- **Funcionamiento base:** ✓ Plantilla operativa.
- **Documentación:** ✓ README genérico de crewAI; falta información contextual.
- **Pruebas:** ✗ Ninguna.
- **Observabilidad:** ✗ No implementada.

## 6. Riesgos y brechas
1. Sin herramientas personalizadas, los agentes no tienen acceso a datos externos.
2. No especifica métricas de éxito ni proceso de validación de guías.
3. Plantilla Flow requiere definición clara de dependencias entre tareas.

## 7. Recomendaciones
1. Definir el caso de guía (ej. guías de usuario, documentación técnica) y personalizar `agents.yaml`/`tasks.yaml`.
2. Añadir herramientas (APIs, bases de conocimiento) y permisos específicos.
3. Implementar proceso de QA (agente revisor, checklist) para asegurar calidad.

## 8. Próximos pasos sugeridos
- Agregar scripts `train/test/replay` similares a la plantilla crew.
- Documentar inputs esperados y ejemplo de `report.md` final.
- Configurar logging estructurado y seguimiento de iteraciones del Flow.
