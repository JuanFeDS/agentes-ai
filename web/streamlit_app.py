# web/streamlit_app.py

import sys
sys.path.append('./')

import streamlit as st
from app.loaders.pdf_loader import load_pdf_text
from app.utils.text_splitter import split_text
from app.chains.summary_chain import get_summary_chain


st.set_page_config(page_title="AIstract - Resumen de Papers", layout="wide")
st.title("📄 AIstract — Tu lector inteligente de papers")

# Subida del archivo PDF
uploaded_file = st.file_uploader("Sube un paper en formato PDF", type="pdf")

if uploaded_file:
    st.info("📥 Cargando el archivo...")

    # 1. Extraer texto del PDF
    raw_text = load_pdf_text(uploaded_file)

    # 2. Dividir en chunks
    chunks = split_text(raw_text)

    # 3. Crear cadena de resumen
    summary_chain = get_summary_chain()
    with st.spinner("🧠 Generando el resumen..."):
        response = summary_chain({"input_documents": chunks})
        resumen = response["output_text"]

    # 4. Mostrar resultado
    st.subheader("📝 Resumen del paper:")
    st.markdown(resumen)
