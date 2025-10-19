"""main.py"""
import json

from agents.dummie_agent.agent import dummie_agent
from agents.memory_agent.agent import memory_agent

def main(user_prompt: str):
    """main function"""
    chain = dummie_agent(user_prompt)
    response = chain.invoke({})

    memory_chain = memory_agent(user_prompt, response.content)
    memory_response = memory_chain.invoke({})

    try:
        with open("memory.json", "r", encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(memory_response.model_dump())

    with open("memory.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(response.content)

if __name__ == "__main__":
    while True:
        user_prompt = input("User: ")
        main(user_prompt)
