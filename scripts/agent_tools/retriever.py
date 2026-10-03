"""Módulo para crear herramientas de recuperación de documentos basadas en FAISS.

Este módulo proporciona funcionalidades para cargar documentos web, procesarlos
y crear un motor de búsqueda semántica utilizando embeddings de OpenAI.
"""
from typing import Any

from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents.agent_toolkits import create_retriever_tool

def create_web_retriever_tool(url: str) -> Any:
    """Crea una herramienta de recuperación de documentos a partir de una URL.
    
    Args:
        url: URL del documento web a procesar.
        
    Returns:
        Una herramienta de recuperación configurada para buscar en el documento.
    """
    # Cargar el documento web
    loader = WebBaseLoader(url)
    documents = loader.load()

    # Dividir el documento en fragmentos manejables
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )
    document_chunks = text_splitter.split_documents(documents)

    # Crear el índice de búsqueda vectorial
    vector_store = FAISS.from_documents(
        document_chunks,
        OpenAIEmbeddings()
    )
    retriever = vector_store.as_retriever()

    # Crear la herramienta de recuperación
    retriever_tool = create_retriever_tool(
        retriever=retriever,
        name="web_retriever",
        description="Útil para responder preguntas sobre el contenido de páginas web."
    )

    return retriever_tool
