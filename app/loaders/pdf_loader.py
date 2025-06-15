"""app/loaders/pdf_loader.py"""

from typing import BinaryIO
import fitz  # PyMuPDF

def load_pdf_text(file: BinaryIO) -> str:
    """
    Extrae y retorna el texto completo de un archivo PDF subido por el usuario.

    Args:
        file (BinaryIO): Archivo PDF cargado por Streamlit (st.file_uploader)

    Returns:
        str: Texto extraído del PDF
    """
    pdf_doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""

    for page in pdf_doc:
        text += page.get_text()

    pdf_doc.close()
    return text.strip()
