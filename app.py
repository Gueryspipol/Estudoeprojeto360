import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Estudoeprojeto360", layout="wide")
st.title("Estudoeprojeto360")
st.caption("Envie a matriz, escolha até quatro cenários encontrados e gere a apresentação.")

BASE = Path(__file__).resolve().parent
MODELO_XLSX = BASE / "Mezzo_Apresentação Saúde_2026_07_v1.xlsx"
MODELO_PPTX = BASE / "Mezzo_Apresentação Saúde_2026_07_v1.pptx"
SCRIPT = BASE / "projetoestudo_streamlit.py"
COMPAT = BASE / "colab_compat.py"

for caminho in (MODELO_XLSX, MODELO_PPTX, SCRIPT, COMPAT):
    if not caminho.exists():
        st.error(f"Arquivo interno não encontrado no projeto: {caminho.name}")
        st.stop()

matriz = st.file_uploader("1. Selecione a matriz Excel", type=["xlsx"], key="matriz")

if matriz:
    assinatura = f"{matriz.name}:{matriz.size}"
    if st.session_state.get("assinatura_matriz") != assinatura:
        st.session_state["assinatura_matriz"] = assinatura
        st.session_state.pop("resultado_scan", None)
        st.session_state.pop("ppt_final", None)

    if "resultado_scan" not in st.session_state:
        with st.spinner("Lendo a matriz e identificando os cenários..."):
            with tempfile.TemporaryDirectory() as temp:
                pasta = Path(temp)
                entrada = pasta / matriz.name
                entrada.write_bytes(matriz.getvalue())
                (pasta / SCRIPT.name).write_bytes(SCRIPT.read_bytes())
                (pasta / COMPAT.name).write_bytes(COMPAT.read_bytes())

                env = os.environ.copy()
                env["SCAN_ONLY"] = "1"
                env["UPLOAD_QUEUE"] = json.dumps([str(entrada)], ensure_ascii=False)

                processo = subprocess.run(
                    [sys.executable, SCRIPT.name],
                    cwd=pasta,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=900,
                )
                resultado = pasta / "cenarios_encontrados.json"

                if processo.returncode != 0 or not resultado.exists():
                    st.error("Não foi possível identificar os cenários da matriz.")
                    with st.expander("Detalhes do processamento"):
                        st.code(processo.stderr or processo.stdout)
                    st.stop()

                st.session_state["resultado_scan"] = json.loads(
                    resultado.read_text(encoding="utf-8")
                )

    leitura = st.session_state["resultado_scan"]
    atual = leitura.get("operadora_atual") or "Não identificada"
    opcoes = leitura.get("operadoras_disponiveis", [])

    st.info(f"Operadora atual identificada: {atual}")

    escolhidos = st.multiselect(
        "2. Escolha até quatro cenários para a apresentação",
        options=opcoes,
        max_selections=4,
        placeholder="Selecione os cenários encontrados na matriz",
    )

    if not opcoes:
        st.warning("Nenhum cenário válido foi encontrado nas duas modalidades da matriz.")

    if st.button("Gerar apresentação", type="primary", use_container_width=True):
        if not escolhidos:
            st.error("Selecione pelo menos um cenário.")
            st.stop()

        numeros = [str(opcoes.index(nome) + 1) for nome in escolhidos]

        with tempfile.TemporaryDirectory() as temp:
            pasta = Path(temp)
            arquivo_matriz = pasta / matriz.name
            arquivo_matriz.write_bytes(matriz.getvalue())

            arquivo_alimentador = pasta / MODELO_XLSX.name
            arquivo_alimentador.write_bytes(MODELO_XLSX.read_bytes())

            arquivo_ppt = pasta / MODELO_PPTX.name
            arquivo_ppt.write_bytes(MODELO_PPTX.read_bytes())

            (pasta / SCRIPT.name).write_bytes(SCRIPT.read_bytes())
            (pasta / COMPAT.name).write_bytes(COMPAT.read_bytes())

            env = os.environ.copy()
            env.pop("SCAN_ONLY", None)
            env["UPLOAD_QUEUE"] = json.dumps(
                [str(arquivo_matriz), str(arquivo_alimentador), str(arquivo_ppt)],
                ensure_ascii=False,
            )
            env["CENARIOS_SELECIONADOS"] = ",".join(numeros)

            with st.spinner("Processando a matriz e gerando a apresentação..."):
                processo = subprocess.run(
                    [sys.executable, SCRIPT.name],
                    cwd=pasta,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=900,
                )

            if processo.returncode != 0:
                st.error("O robô encontrou um erro durante o processamento.")
                with st.expander("Detalhes do erro"):
                    st.code(processo.stderr or processo.stdout)
                st.stop()

            saida = pasta / "Apresentador360_V2_FINAL.pptx"
            if not saida.exists():
                st.error("O processamento terminou, mas o PowerPoint final não foi criado.")
                with st.expander("Registro do processamento"):
                    st.code(processo.stdout)
                st.stop()

            st.session_state["ppt_final"] = saida.read_bytes()

    if "ppt_final" in st.session_state:
        st.success("Apresentação gerada com sucesso!")
        st.download_button(
            "Baixar PowerPoint",
            data=st.session_state["ppt_final"],
            file_name="Apresentador360_V2_FINAL.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True,
        )
