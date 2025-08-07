"""chat_prompt_template.py"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

def chat_prompt_template(prompt: str, language: str) -> str:
    """Script where chat prompts are used
    
    Args:
        prompt(str): The input prompt for the model.
        language(str): The language to translate to.

    Returns:
        str: The generated text response from the model.
    """

    # Definimos la plantilla
    template = ChatPromptTemplate([
        ('system', 'Traduce lo siguiente al idioma: {language}'),
        ('human', '{prompt}')
    ])

    # Inicializamos el modelo
    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.2
    )

    # Construimos la cadena
    chain = template | model

    response = chain.invoke({
        'language': language,
        'prompt': prompt
    })

    return response.content
