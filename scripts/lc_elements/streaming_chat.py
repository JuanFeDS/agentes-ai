# Script to demonstrate streaming chat
import time

from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

async def streaming_chat(prompt_user: str):
    """Demonstrates streaming chat"""

    # Initialize the model
    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.5
    )

    # Create a human message
    prompt = HumanMessage(
        content = prompt_user
    )

    # Stream the response
    chunks = []

    async for chunk in model.astream([prompt]):
        chunks.append(chunk)
        print(chunk.content, end='', flush=True)
        time.sleep(0.1)
