"""Class to create a vector store"""
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

class VectorStore():
    """Class to create a vector store"""
    def __init__(self, collection_name: str, persist_directory: str):
        """Initialize the vector store with the given collection name and directory.
        
        Args:
            collection_name: Name of the collection in the vector store
            persist_directory: Directory where the vector store will be persisted
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
        self.vector_store = self._initialize_vector_store()

    def _initialize_vector_store(self):
        """Initialize and return a Chroma vector store.
        
        Returns:
            Chroma: Initialized Chroma vector store instance
        """
        return Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of Document objects to add to the vector store
            
        Raises:
            ValueError: If no documents are provided
        """
        if not documents:
            raise ValueError("No documents provided to add to vector store")

        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4) -> list[Document]:
        """Search for similar documents in the vector store.
        
        Args:
            query: The query string to search for
            k: Number of similar documents to return (default: 4)
            
        Returns:
            list[Document]: List of documents most similar to the query
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        return self.vector_store.similarity_search(query, k=k)
