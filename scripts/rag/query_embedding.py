"""
Script para demostrar el uso de embeddings en consultas de lenguaje natural.
Este script muestra cómo convertir consultas a vectores numéricos (embeddings)
y cómo estos pueden usarse para encontrar información relevante.
"""
import numpy as np
from numpy.linalg import norm
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Cargar variables de entorno
load_dotenv()

def query_embeddings():
    """
    Demuestra el uso de embeddings para procesar consultas en lenguaje natural.
    """
    # Inicializar el modelo de embeddings
    modelo_embeddings = OpenAIEmbeddings()

    # Lista de oraciones de ejemplo
    oraciones = [
        "Hola!",
        "Hola ¿Cómo estás?",
        "Cuál es tu nombre?",
        "Mi nombre es John Doe",
        "¿Cuál es tu edad?",
        "Tengo 30 años",
        "¿Cuál es tu profesión?",
        "Soy programador",
    ]

    # Crear embeddings para las oraciones
    print("Creando embeddings para las oraciones de ejemplo...")
    embeddings = modelo_embeddings.embed_documents(oraciones)
    print(f"Se crearon {len(embeddings)} embeddings de dimensión {len(embeddings[0])}")

    # Consulta para buscar información específica
    consulta = "Cuál es el nombre mencionado en la conversación?"
    print(f"\nConsulta: '{consulta}'")

    # Convertir la consulta a embedding
    embedding_consulta = modelo_embeddings.embed_query(consulta)
    print("\nLa consulta se ha convertido a un vector numérico (embedding).")
    print(f"Dimensión del embedding: {len(embedding_consulta)}")

    # Calcular similitudes entre la consulta y todas las oraciones
    print("\nCalculando similitudes...")
    similitudes = [
        np.dot(embedding_consulta, emb) / (norm(embedding_consulta) * norm(emb))
        for emb in embeddings
    ]

    # Encontrar el índice del más similar
    indice = np.argmax(similitudes)
    texto_mas_cercano = oraciones[indice]
    similitud = similitudes[indice]

    # Mostrar resultados
    print("\n" + "=" * 60)
    print("📌 Resultado de la búsqueda por similitud de embedding")
    print("=" * 60)
    print("\n🔍 Texto original generador del embedding:")
    print(f"   '{consulta}'\n")

    print("📝 Texto más cercano encontrado en la base de conocimiento:")
    print(f"   '{texto_mas_cercano}'\n")

    print(f"📊 Nivel de similitud: {similitud:.2%}")

    # Interpretación de la similitud
    if similitud > 0.9:
        print(
            """\n✅ Coincidencia excelente: 
            El texto encontrado es prácticamente equivalente en significado."""
        )
    elif similitud > 0.7:
        print(
            """\n👍 Buena coincidencia: 
            El texto encontrado es muy similar en significado."""
        )
    elif similitud > 0.5:
        print(
            """\n🤔 Coincidencia moderada: 
            El texto encontrado tiene cierta relación semántica."""
        )
    else:
        print(
            """\n⚠️ Baja coincidencia: 
            El texto encontrado no es muy similar. 
            Considera ampliar tu base de conocimiento."""
        )

if __name__ == "__main__":
    query_embeddings()
