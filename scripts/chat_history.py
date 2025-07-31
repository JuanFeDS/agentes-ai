"""Script where chat history is kept"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

# Inicializamos el modelo
model = ChatOpenAI(
    model = 'gpt-4o',
    temperature = 0.5
)

# Inicializamos la sesión
sesion = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Get the session history for the given session ID.
    
    Args:
        session_id(str): The session ID.
    
    Returns:
        BaseChatMessageHistory: The session history.
    """
    if session_id not in sesion:
        sesion[session_id] = InMemoryChatMessageHistory()
    return sesion[session_id]

def chat_history():
    """
    Script where chat history is kept
    """
    with_message_history = RunnableWithMessageHistory(
        model,
        get_session_history
    )

    config = {
        'configurable': {
            'session_id': 'session_1'
        }
    }

    while True:
        prompt_user = input('Escribe tu mensaje: ')
        response = with_message_history.invoke(prompt_user, config)
        print(response.content)
