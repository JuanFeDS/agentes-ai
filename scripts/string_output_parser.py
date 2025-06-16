"""Parser the model ouput"""
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

load_dotenv()

def st_out_parser():
    """Function to parser the model output"""

    # Definimos la plantilla
    prompt_template = ChatPromptTemplate([
        ('system', 'Traduce lo siguiente al idioma: {language}'),
        ('human', '{text}')
    ])

    # Configuramos el parser para el output
    parser = StrOutputParser()

    # Inicializamos el modelo
    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.2
    )
    # Construimos la cadena

    chain = prompt_template | model | parser

    response = chain.invoke({
        'language': 'italiano',
        'text': 'Hola, mundo!'
    })

    print(response)
