"""pokeagent app"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()


def writer_agent():
    """
    Crea y devuelve un agente escritor que genera contenido creativo.
    """

    model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    # Plantilla para el escritor
    template = """Eres el Profesor Oak, un investigador Pokémon que combina rigor científico
    con la narrativa cautivadora de National Geographic. 

    Tarea: Transforma la siguiente información técnica de un Pokémon en un artículo breve, 
    explicando sus características, hábitat y peculiaridades. 
    El tono debe ser informativo pero entretenido, para que tanto científicos 
    como aficionados puedan disfrutarlo.
    
    Información del Pokémon:
    {input}
    
    Artículo:"""

    # Crear la cadena de procesamiento
    prompt = PromptTemplate(template=template, input_variables=["input"])

    # Crear el agente
    agent_executor = LLMChain(llm=model, prompt=prompt, verbose=True)

    return agent_executor
