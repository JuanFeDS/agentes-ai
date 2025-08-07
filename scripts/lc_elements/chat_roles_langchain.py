"""chat roles langchain.py"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from dotenv import load_dotenv

load_dotenv()

def chat_roles_langchain(
    user_prompt: str,
    system_prompt: str,
    model: str = "gpt-4o"
    ) -> str:
    """Script where chat roles are used"""

    client = ChatOpenAI(model=model)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    response = client.invoke(messages)

    return response.content
