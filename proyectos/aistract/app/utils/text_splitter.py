"""app/utils/text_splitter.py"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[Document]:
    """
    Divide el texto en fragmentos para que puedan ser procesados por el modelo de lenguaje.

    Args:
        text (str): Texto largo a dividir (por ejemplo, el contenido de un PDF)
        chunk_size (int): Tamaño máximo de cada fragmento (en caracteres)
        chunk_overlap (int): Superposición entre fragmentos para mantener contexto

    Returns:
        list[Document]: Lista de objetos Document con metadatos mínimos
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    docs = splitter.create_documents([text])
    return docs
