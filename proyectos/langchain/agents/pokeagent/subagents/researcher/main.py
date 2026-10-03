"""pokeagent app"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import ChatPromptTemplate
from .tools.get_pokemon_info import get_pokemon_info

load_dotenv()

def researcher_agent():
    """
    Crea y devuelve un agente investigador que consulta datos de Pokémon.
    """

    model = ChatOpenAI(
        model = "gpt-3.5-turbo",
        temperature = 0
    )

    # Inicializar el agente con configuración simplificada
    agent_executor = initialize_agent(
        tools=[get_pokemon_info],
        llm=model,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            'system_message': (
                "Eres un investigador Pokémon experto. "
                "Usa la herramienta proporcionada para obtener información precisa. "
                "Responde siempre con los datos exactos de la API, sin inventar información."
            )
        }
    )

    return agent_executor
