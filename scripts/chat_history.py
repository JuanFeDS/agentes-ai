"""Script where chat history is kept"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()

def message_history():
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

    while True:
        query = input('')
        chat_history.append(
            HumanMessage(
                content=query
            )
        )

        response = model.invoke(chat_history).content
        print(response)

        chat_history.append(response)
