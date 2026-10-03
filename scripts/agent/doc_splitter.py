"""Script to split documents"""
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def doc_splitter(directory_path: str):
    """Split documents into chunks"""

    loader = DirectoryLoader(
        directory_path,
        glob='*.pdf',
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    # Extraer solo el contenido de texto de los documentos
    texts = [doc.page_content for doc in documents]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap = 20,
        length_function = len,
        is_separator_regex = False,
    )

    splits = text_splitter.create_documents(texts)

    return splits
