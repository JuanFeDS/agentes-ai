"""Entry point for runiing the program."""
# from scripts.basic_gen_text import basic_gen_text
# from scripts.few_shot_prompting import few_shot_prompt
from scripts.string_output_parser import st_out_parser

def run():
    """"
    Entry point for running the program.
    """
    st_out_parser()

if __name__ == '__main__':
    run()
