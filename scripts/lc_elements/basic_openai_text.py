from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def basic_openai(model: str, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> str:
    """
    Generate text using OpenAI's API.
    
    Args:
        model (str): The model to use for text generation.
        prompt (str): The input prompt for the model.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Sampling temperature for randomness in output.
    
    Returns:
        str: The generated text response from the model.
    """
    client = OpenAI()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )

    return response.choices[0].message.content.strip()
