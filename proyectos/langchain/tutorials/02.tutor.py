"""tutor app"""

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

def tutor(text: str):
    """
    tutor function
    
    Args:
        text (str): text to tutor
    """

    model = ChatOpenAI(
        model = "gpt-3.5-turbo",
        temperature = 0.2
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            'system', 
            '''Eres un experto en {topic}. Actuaras como un tutor 
            usando el método Feynman. La idea es que expliques temas
            complejos de manera sencilla y clara, usarás ejemplos 
            didácticos e ilustrativos'''
        ),
        ('human', '¿Qué es {text}?')
    ])

    chain = prompt | model

    response = chain.invoke({
        'topic': 'Ciencia de datos',
        'text': text
    })

    print(response.content)

if __name__ == '__main__':
    user_topic = input("Introduce un tema: ")
    tutor(user_topic)
