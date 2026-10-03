# Ficha técnica – crewai/new_project

## 1. Propósito y alcance
Plantilla mínima generada con `crewai new project`, pensada para iniciar rápidamente una nueva crew con configuración limpia. Incluye solo archivos esenciales (config, `crew.py`, `main.py`).

## 2. Arquitectura y componentes clave
- **`config/agents.yaml` y `config/tasks.yaml`:** definen roles y tareas iniciales (actualmente placeholders).
- **`crew.py`:** clase principal que reúne agentes y herramientas.
- **`main.py`:** punto de entrada que expone funciones `run/replay/train/test` según el scaffold estándar.

## 3. Requisitos y despliegue
- Python 3.10–3.13.
- Dependencias controladas por `pyproject.toml` en la raíz (usa `crewai`, `rich`, etc.).
- Variables de entorno en `.env` (claves LLM).
- Ejecución: `crewai run` o `python main.py` con los argumentos disponibles.

## 4. Nivel de culminación
**Bajo.** Plantilla sin personalizar; requiere definir agentes, tareas, herramientas y casos de uso.

## 5. Evaluación objetiva
- **Funcionamiento base:** ✓ Estructura válida.
- **Documentación:** ✗ No existe README específico (solo hereda instrucciones genéricas de crewAI).
- **Pruebas:** ✗ Ninguna.
- **Observabilidad:** ✗ Sin logging propio.

## 6. Riesgos y brechas
1. Archivos de configuración vacíos implican que la crew no ejecutará tareas útiles.
2. Falta de herramientas/custom code puede dejar al LLM sin contexto.
3. Sin control de versiones de `uv.lock`, difícil reproducir entornos si se borra.

## 7. Recomendaciones
1. Documentar el caso de uso que se cubrirá con esta plantilla antes de modificar archivos.
2. Añadir pruebas unitarias/integración cuando se incorporen herramientas personalizadas.
3. Configurar logging y almacenamiento de resultados para evaluar la calidad de ejecuciones futuras.

## 8. Próximos pasos sugeridos
- Definir backlog inicial: objetivos de la crew, fuentes de datos, APIs.
- Construir pipeline CI/CD mínimo que ejecute `crewai run --dry-run` o pruebas sin costo.
- Crear README y checklist de configuración (variables de entorno, permisos, dependencias extra).
