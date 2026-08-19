import streamlit as st

st.set_page_config(
    page_title="Estudoeprojeto360",
    layout="wide"
)

st.title("Estudoeprojeto360")

st.subheader(
    "Automação de geração de apresentações corporativas"
)

arquivo = st.file_uploader(
    "Selecione a matriz Excel",
    type=["xlsx"]
)

if arquivo:
    st.success(
        "Arquivo carregado com sucesso!"
    )
