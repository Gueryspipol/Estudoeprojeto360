import streamlit as st

from etapas.etapas.teste import ler_matriz

st.set_page_config(
    page_title="Estudoeprojeto360",
    layout="wide"
)

st.title("Estudoeprojeto360")

arquivo = st.file_uploader(
    "Selecione a matriz Excel",
    type=["xlsx"]
)

if arquivo:

    dados = ler_matriz(arquivo)

    st.success("Matriz carregada!")

    st.write(
        "Quantidade de abas:",
        dados["quantidade_abas"]
    )

    st.write(
        "Abas encontradas:"
    )

    for aba in dados["abas"]:

        st.write(
            "-",
            aba
        )
