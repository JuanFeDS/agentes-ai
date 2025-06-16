"""A simple example of using HuggingFacePipeline to generate text."""
from langchain_huggingface.llms import HuggingFacePipeline

from src.utils.logger.logger import get_logger
logger   = get_logger(__name__)

def basic_gen_text():
    """
    Example of using HuggingFacePipeline to generate text with a pre-trained model.
    """

    logger.info('Running HuggingFace text generation example...')
    hf = HuggingFacePipeline.from_model_id(
        model_id = 'gpt2',
        task = 'text-generation',
        pipeline_kwargs = {
            'max_new_tokens': 30
        }
    )
    logger.info('HuggingFacePipeline initialized.')

    prompt = input('Enter your prompt: ')
    response = hf.invoke(prompt)

    print(response)
