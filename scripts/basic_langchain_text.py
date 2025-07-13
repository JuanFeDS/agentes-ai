"""basic_langchain_text.py"""
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()

def basic_langchain_text(
    user_prompt: str,
    model: str = "gpt-4o"
    ) -> str:

    """Script where basic langchain text is used"""
    chat = ChatOpenAI(model=model)

    response = chat.invoke(user_prompt)

    return response.content
