"""
Create a vector store using Pinecone
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def pinecone():
    """Create a vector store using Pinecone"""

    index_name = os.getenv('INDEX_NAME')

    # 1. Cargar texto como Document
    loader = TextLoader('./Data/Final/text_pinecone.txt', encoding='utf-8')
    documents = loader.load()   # lista con 1 Document (todo el texto)

    # 2. Partir en varios Document (uno por chunk)
    text_splitter = CharacterTextSplitter(
        chunk_size=50,    # puedes ajustar según necesidad
        chunk_overlap=5
    )
    docs = text_splitter.split_documents(documents)  # ahora docs es una lista de muchos Document

    print(f"Original: {len(documents)} documento(s)")
    print(f"Después del split: {len(docs)} documentos")

    # 3. Crear embeddings
    embedding = OpenAIEmbeddings(model='text-embedding-3-large')

    # 4. Crear o cargar el índice de Pinecone
    vectorstore = PineconeVectorStore.from_documents(
        documents=docs,
        embedding=embedding,
        index_name=index_name,
    )

    # 5. Buscar documentos similares
    query = "¿Cuáles son los principales desafíos de la inteligencia artificial?"

    response = vectorstore.similarity_search(
        query=query,
        k=1
    )

    for doc in response:
        print("-" * 50)
        print(doc.page_content)
        print("-" * 50)

if __name__ == '__main__':
    pinecone()
