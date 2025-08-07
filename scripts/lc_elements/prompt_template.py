"""prompt_template.py"""
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

def prompt_template(prompt: str, language: str) -> str:
    """Script where template prompts are used
    
    Args:
        prompt (str): The input prompt for the model.
        language (str): The language to translate to.
    
    Returns:
        str: The generated text response from the model.
    """

    # Definimos la plantilla
    template = PromptTemplate(
        input_variables=['language', 'prompt'],
        template = "Traduce {prompt} al idioma: {language}"
    )

    # Aplicamos el template
    response = template.invoke({
        'language': language,
        'prompt': prompt
    })

    # Inicializamos el modelo
    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.2
    )

    # Construimos la cadena
    chain = template | model

    # Invocamos la cadena
    response = chain.invoke({
        'language': language,
        'prompt': prompt
    })

    return response.content
