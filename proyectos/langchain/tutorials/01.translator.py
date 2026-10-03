"""translator app"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def translator(text_to_translate: str):
    """
    translator function
    
    Args:
        text_to_translate (str): text to translate
    """
    model = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7
    )

    prompt = ChatPromptTemplate.from_messages([
        ('system', 'You are a translator that can translate text from one language to another.'),
        ('human', 'Translate the following text: {text_to_translate} to english.')
    ])

    messages = prompt.invoke({
        'text_to_translate': text_to_translate
    })

    response = model.invoke(messages)
    print(response.content)

if __name__ == '__main__':
    text = input("Enter text to translate: ")
    translator(text)
