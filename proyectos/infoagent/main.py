"""main.py"""
from dotenv import load_dotenv
from src.ingest import ingest_arxiv

load_dotenv()

def main():
    """Función principal del agente."""

    ingest_arxiv(
        max_results=3
    )

    # print(result)

if __name__ == "__main__":
    main()
