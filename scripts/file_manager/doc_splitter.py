"""Script to split documents"""
from langchain.text_splitter import RecursiveCharacterTextSplitter

def doc_splitter(file_path: str):
    """Script to split documents
    
    Args:
        file_path (str): Path to the file to split
    """

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20,
        length_function = len,
        is_separator_regex = False,
    )

    text = text_splitter.create_documents([content])

    print(text[1])

if __name__ == '__main__':
    doc_splitter('./Data/Final/01.un_camino_solitario.txt')
