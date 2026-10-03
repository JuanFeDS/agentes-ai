"""Script to create the agent"""
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.retrievers import BaseRetriever
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Cargar variables de entorno
load_dotenv()

def agent(retriever: BaseRetriever):
    """
    Crea un agente que utiliza RAG para responder preguntas basadas en documentos.
    
    Args:
        retriever: Objeto retriever para buscar documentos relevantes.
        
    Returns:
        Cadena RAG lista para invocarse con input y chat_history.
    """
    # Cargar el system prompt
    with open('./scripts/agent/prompt.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    # Inicializar el modelo de lenguaje
    llm = ChatOpenAI(
        model='gpt-4o',
        temperature=0.3,  # Reducido para respuestas más enfocadas
        max_tokens=1000,
        streaming=True
    )
    
    # Prompt para contextualizar preguntas de seguimiento
    contextualize_q_system_prompt = """
    Dada una conversación y una pregunta de seguimiento, reformula la pregunta para que sea independiente.
    Si la pregunta no está relacionada con el contexto, devuelve la pregunta original sin modificar.
    """
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    # Recuperador consciente del historial
    history_aware_retriever = create_history_aware_retriever(
        llm, 
        retriever, 
        contextualize_q_prompt
    )
    
    # Prompt para la generación de respuestas
    qa_system_prompt = f"""
    {system_prompt}
    
    Utiliza la siguiente información para responder a la pregunta del usuario.
    Si no sabes la respuesta, simplemente di que no lo sabes, no inventes nada.
    
    Contexto: {{context}}
    """
    
    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    # Cadena de respuesta final
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    
    # Combinar en un RAG chain
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain
