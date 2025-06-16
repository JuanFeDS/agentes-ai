"""Entry point for runiing the program."""
# from scripts.basic_gen_text import basic_gen_text
# from scripts.few_shot_prompting import few_shot_prompt
# from scripts.string_output_parser import st_out_parser
from scripts.chat_history import message_history

def run():
    """"
    Entry point for running the program.
    """
    message_history()

if __name__ == '__main__':
    run()
