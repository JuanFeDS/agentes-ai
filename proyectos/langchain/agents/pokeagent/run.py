"""pokeagent app"""
from subagents.researcher.main import researcher_agent
from subagents.writer.main import writer_agent

def run():
    """
    Función principal que orquesta el flujo entre el investigador y el escritor
    """
    # Inicializar los agentes
    researcher = researcher_agent()
    writer = writer_agent()

    # 1. Primera fase: Investigación
    query = "¿Cuál es la información del pokemon venusaur?"
    print("\n=== Fase 1: Investigación ===")
    print(f"Consultando: {query}")

    # Ejecutar el investigador
    research_result = researcher.invoke({"input": query})
    research_output = research_result.get('output', '')
    print("\nResultado de la investigación:")
    print(research_output)

    # 2. Segunda fase: Escritura
    print("\n=== Fase 2: Escritura ===")

    # Ejecutar el escritor con los datos del investigador
    writing_result = writer.run({"input": research_output})
    final_output = writing_result if isinstance(writing_result, str) else ''

    print("\n=== Artículo Final ===")
    print(final_output)

if __name__ == "__main__":
    run()
