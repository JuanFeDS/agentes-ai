"""A simple example of using HuggingFacePipeline to generate text."""
from langchain_huggingface.llms import HuggingFacePipeline

def basic_gen_text(model_id: str, task: str, prompt: str, max_tokens: int) -> str:
    """
    Example of using HuggingFacePipeline to generate text with a pre-trained model.
    """

    hf = HuggingFacePipeline.from_model_id(
        model_id = model_id,
        task = task,
        pipeline_kwargs = {
            'max_new_tokens': max_tokens
        }
    )

    response = hf.invoke(prompt)

    return response
