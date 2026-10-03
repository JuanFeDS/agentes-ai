"""Script para ejecutar el agente con RAG"""
from dotenv import load_dotenv
from typing import Dict, Any

from doc_splitter import doc_splitter
from embedding import embedding
from agent import agent

load_dotenv()

def run():
    """Función principal para ejecutar el agente con RAG"""
    try:
        # Cargar y dividir los documentos
        print("Cargando y procesando documentos...")
        splits = doc_splitter('./Data/Final/agents')
        
        # Crear el vectorizador y el recuperador
        print("Creando embeddings...")
        retriever = embedding(splits)
        
        # Inicializar el agente con RAG
        print("Inicializando agente RAG...")
        rag_chain = agent(retriever)
        
        # Bucle de interacción con el usuario
        print("\n¡Agente listo! Escribe 'salir' para terminar.")
        chat_history = []
        
        while True:
            user_input = input("\nTú: ")
            
            if user_input.lower() == 'salir':
                print("¡Hasta luego!")
                break
                
            # Ejecutar la cadena RAG
            response = rag_chain.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            # Mostrar la respuesta
            print(f"\nAsistente: {response['answer']}")
            
            # Actualizar el historial de chat
            chat_history.extend([
                ("human", user_input),
                ("ai", response['answer'])
            ])
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    run()



if __name__ == '__main__':
    run()
