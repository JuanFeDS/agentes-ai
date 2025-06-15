"""app/chains/summary_chain.py"""
import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate


def get_summary_chain():
    """
    Crea y retorna una cadena de resumen basada en el patrón map-reduce usando un modelo OpenAI.
    """
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",  # Cambia a "gpt-4" si tienes acceso
        temperature=0.3
    )

    # Plantilla personalizada para el resumen
    map_prompt = PromptTemplate.from_template(
    """
    Resume el siguiente fragmento de un paper académico. Mantén la precisión técnica 
    y un lenguaje claro y directo.

    Texto:
    {text}

    Resumen:
    """
    )

    reduce_prompt = PromptTemplate.from_template(
    """
    Combina los siguientes resúmenes parciales en un único resumen coherente y fluido del paper. Usa un lenguaje claro, técnico y profesional.

    Resúmenes:
    {text}

    Resumen final:
    """
    )

    chain = load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=reduce_prompt,
        verbose=True
    )

    return chain
