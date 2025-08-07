"""trim_messages.py"""
from langchain_core.messages import trim_messages, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

def trim_messages_langchain(
    user_prompt: str,
    system_prompt: str,
    strategy: str,
    model: str = "gpt-4o"
    ) -> str:
    """Script where trim messages are used"""

    client = ChatOpenAI(model=model)

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    trim_message = trim_messages(
        messages,
        max_tokens=100,
        strategy=strategy,
        token_counter=ChatOpenAI(model=model),
        include_system=True
    )

    response = client.invoke(trim_message)

    return response.content
