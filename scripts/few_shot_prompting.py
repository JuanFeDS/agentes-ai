"""f"""
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

def few_shot_prompt(prompt: str) -> str:
    """
    Script where few shot prompting is used. In this example, 
    we are using a few examples to help the model understand 
    the task.
    
    Args:
        prompt(str): The input prompt for the model.
    
    Returns:
        str: The generated text response from the model.
    """

    # Construcción del prompt template
    examples = [
        {'input': '2 😎 3', 'output': '6'},
        {'input': '10 😎 3', 'output': '30'},
    ]

    example_prompt = ChatPromptTemplate([
        ('human', '{input}'),
        ('ai', '{output}')
    ])

    f_s_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples
    )

    main_prompt = ChatPromptTemplate.from_messages([
        ('system', 'Eres un mago de las matemáticas.'),
        f_s_prompt,
        ('human', '{input}')
    ])

    # Construcción del modelo

    model = ChatOpenAI(
        model = 'gpt-4o',
        temperature = 0.2
    )

    chain = main_prompt | model
    response = chain.invoke({
        'input': prompt
    }).content

    return response
