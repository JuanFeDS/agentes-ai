"""memory_agent.py"""
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agents.memory_agent.prompt import SYSTEM_PROMPT

load_dotenv()

class Memory(BaseModel):
    """Memory class"""
    user_prompt: str = Field(description="User prompt")
    response_llm: str = Field(description="Response from LLM")
    user_intention: str = Field(description="User intention")
    llm_solutions: str = Field(description="LLM solutions")
    solution_rate: int = Field(description="Solution rate")

def memory_agent(user_prompt: str, response_llm: str):
    """Builds the agent"""
    model = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    model = model.with_structured_output(schema=Memory)

    system_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"""
            Este es el mensaje del usuario: {user_prompt}.
            Este es el mensaje de la IA: {response_llm}
        """)
    ])

    chain = system_prompt | model
    return chain
