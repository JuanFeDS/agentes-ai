"""Main script to create a vector store"""
import json

from vector_store import VectorStore
from langchain_core.documents import Document

def main():
    """Main function to create a vector store"""

    # Crear el vector store
    vector_store = VectorStore(
        collection_name="test", persist_directory="./Data/chroma_db"
    )

    # Crear documentos
    with open('./Data/Final/naruto.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    documents = [Document(
        page_content=doc['description'],
        metadata=doc['metadata']
    ) for doc in data]

    # Agregar documentos al vector store
    vector_store.add_documents(documents)

    query = "Ninja copia"

    # Buscar documentos similares
    similar_documents = vector_store.similarity_search(query, k=3)

    for doc in similar_documents:
        print(doc.page_content)

if __name__ == "__main__":
    main()
