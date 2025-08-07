"""Script where chat history is kept"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

load_dotenv()

def dummie_message_history():
    """Script where chat history is kept"""

    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.5
    )

    chat_history = []

    if not chat_history:
        system_message = SystemMessage(
            content='Eres una experta en literatura'
        )
        chat_history.append(system_message)

    iterations = 5

    while iterations > 0:
        iterations -= 1
        
        query = input('')
        chat_history.append(
            HumanMessage(
                content=query
            )
        )

        response = model.invoke(chat_history).content
        print(response)
        print('-------------------')

        chat_history.append(AIMessage(content=response))
