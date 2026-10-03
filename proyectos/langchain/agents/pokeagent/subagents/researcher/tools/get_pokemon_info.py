"""get pokemon info tool"""
import requests
from langchain_core.tools import tool

@tool
def get_pokemon_info(pokemon_name: str) -> dict:
    """Obtiene información detallada de un Pokémon.
    
    Args:
        pokemon_name: Nombre del Pokémon a buscar
        
    Returns:
        dict: Diccionario con la información del Pokémon
    """
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}'
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return f'Pokemon {pokemon_name} not found'

    data = response.json()

    data_resume = {
        'nombre': data['name'],
        'tipos': [t['type']['name'] for t in data['types']],
        'stats': {
            'hp': data['stats'][0]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'speed': data['stats'][5]['base_stat'],
            'special_attack': data['stats'][3]['base_stat'],
            'special_defense': data['stats'][4]['base_stat']
        }
    }

    return data_resume
