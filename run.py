"""Entry point for runing the program."""

import asyncio
# from scripts.basic_gen_text import basic_gen_text
# from scripts.few_shot_prompting import few_shot_prompt
# from scripts.string_output_parser import st_out_parser
# from scripts.chat_history import message_history
# from scripts.runnable_lambda import runnable_lambda
# from scripts.json_output_parser import json_parser
from scripts.streaming_chat import streaming_chat

def run():
    """"
    Entry point for running the program.
    """
    # basic_gen_text() # Generación de texto básico
    # message_history() # Almacena el historial de conversación
    # runnable_lambda() # Agregar una función personalizada como runnable
    # json_parser() # Devuelve la respuesta en formato JSON
    asyncio.run(streaming_chat('Hola, mundo!'))

if __name__ == '__main__':
    run()
