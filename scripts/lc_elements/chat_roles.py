"""chat roles.py"""
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

def chat_roles(
    user_prompt: str,
    system_prompt: str,
    model: str = "gpt-4o"
    ) -> str:
    """Script where chat roles are used"""

    client = OpenAI()

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip()
