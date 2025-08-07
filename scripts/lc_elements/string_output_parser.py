"""Parser the model ouput"""
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

def st_out_parser(text: str, language: str) -> str:
    """
    Function to parser the model output
    
    Args:
        text(str): The input text to be parsed.
        language(str): The language to translate the text to.
    
    Returns:
        str: The parsed text.
    """

    # Definimos la plantilla
    prompt_template = ChatPromptTemplate([
        ('system', 'Traduce lo siguiente al idioma: {language}'),
        ('human', '{text}')
    ])

    # Inicializamos el modelo
    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.2
    )

    # Configuramos el parser para el output
    parser = StrOutputParser()

    # Construimos la cadena
    chain = prompt_template | model | parser

    response = chain.invoke({
        'language': language,
        'text': text
    })

    return response
