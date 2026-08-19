import streamlit as st

from etapas.etapas.teste import teste

st.set_page_config(
    page_title="Estudoeprojeto360",
    layout="wide"
)

st.title("Estudoeprojeto360")

if st.button("Testar robô"):
    st.success(teste())
