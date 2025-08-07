from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

load_dotenv()

def runnable_lambda(prompt_user: str) -> str:
    """Script where runnables are defined"""

    clean_text = RunnableLambda(
        lambda x: x.replace('\n', ' ').replace(' ', '').capitalize()
    )

    prompt = ChatPromptTemplate.from_template(
        'Responde de forma precisa: {query}'
    )

    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.5
    )

    parser = StrOutputParser()

    a_dict = RunnableLambda(
        lambda x: {
            'Response': x
        }
    )

    chain = clean_text | prompt | model | parser | a_dict
    response = (chain.invoke(prompt_user))
    return response
