"""Script to create the agent"""
from dotenv import load_dotenv

from langchain_tavily import TavilySearch

load_dotenv()

def create_tavily_tool() -> TavilySearch:
    """Crea y retorna una instancia configurada de TavilySearch.
    
    Returns:
        TavilySearch: Instancia configurada del buscador Tavily con 5 resultados máximos.
    """
    tavily_search = TavilySearch(
        max_results=5,
        topic='general'
    )
    
    return tavily_search
