"""Script to demonstrate the use of JsonOutputParser with LangChain"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

def json_parser():
    """Script to demonstrate the use of JsonOutputParser with LangChain"""

    parser = JsonOutputParser()

    prompt = PromptTemplate.from_template(
        template = '''
            Responde de forma precisa: \n
            {format_instructions} \n
            {query}
        ''',
        partial_variables = {
            "format_instructions": parser.get_format_instructions()
        }
    )

    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.5
    )


    chain = prompt | model | parser

    response = chain.invoke({'query': 'Qué es el universo?'})

    print(response)
