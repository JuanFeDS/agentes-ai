"""Script to embed the documents"""
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def embedding(splits: list):
    """Function to embed the documents"""

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
    )

    retriever = vectorstore.as_retriever()

    return retriever
