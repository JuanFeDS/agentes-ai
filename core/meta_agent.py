"""meta_agent.py"""
import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Carga tu clave de OpenAI desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

def generar_agente(descripcion_tarea, nombre_archivo="generated_agent.py"):
    """
    """
    prompt = f"""
        Eres un generador de agentes Python. Construye un script que cumpla esta función:
        \"\"\"{descripcion_tarea}\"\"\"

        Asegúrate de que el código incluya:
        - Conexión a la base de datos
        - Extracción de estructura (tablas, relaciones)
        - Generación de grafo usando NetworkX
        - Visualización del grafo

        El código debe ser autocontenible, limpio y bien comentado.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un experto en generación de agentes en Python."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    codigo = response.choices[0].message.content

    ruta_salida = f"agents/{nombre_archivo}"
    os.makedirs("agents", exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(codigo)

    print(f"✅ Agente guardado en: {ruta_salida}")

if __name__ == "__main__":
    descripcion = input("¿Qué tipo de agente quieres construir?\n> ")
    generar_agente(descripcion)
