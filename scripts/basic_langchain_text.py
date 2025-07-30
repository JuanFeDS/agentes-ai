"""basic_langchain_text.py"""
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

def basic_langchain_text(
    user_prompt: str,
    model: str = "gpt-4o"
    ) -> str:

    """Script where basic langchain text is used
    
    Args:
        user_prompt(str): The input prompt for the model.
        model(str): The model to use for text generation.
    
    Returns:
        str: The generated text response from the model.
    """
    
    # Inicializamos el modelo   
    chat = ChatOpenAI(model=model)

    # Generamos la respuesta
    response = chat.invoke(user_prompt)

    return response.content
