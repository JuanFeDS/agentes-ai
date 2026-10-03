"""output parser app"""
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
    model = "gpt-3.5-turbo",
    temperature = 0.2
)

output_parser = CommaSeparatedListOutputParser()

prompt = PromptTemplate(
    template = 'Dame una lista de {n} frutas sin enumerar.',
    input_variables = ['n'],
    output_parser = output_parser
)

formatted_prompt = prompt.format_prompt(n = 20)
output = model.invoke(formatted_prompt.to_string())
parsed_output = output_parser.parse(output.content)

# response = model.invoke(prompt.format(n = 10))
# print(response.content)
print(parsed_output)
