"""dummie_agent.py"""
import json
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def dummie_agent(user_prompt: str):
    """Builds the agent"""

    try:
        with open("memory.json", "r", encoding='utf-8') as f:
            content = f.read().strip()
            history = json.loads(content) if content else []
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    intention = ''
    if isinstance(history, list):
        for item in history:
            if isinstance(item, dict) and 'user_intention' in item:
                intention += item['user_intention'] + '\n'

    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    system_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        ("human", user_prompt + '\n' + intention)
    ])
    chain = system_prompt | model
    return chain
