import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import streamlit as st

st.set_page_config(page_title='Estudoeprojeto360', layout='wide')
st.title('Estudoeprojeto360')
st.caption('Geração automatizada da apresentação a partir da matriz e dos modelos.')

matriz = st.file_uploader('1. Selecione a matriz Excel', type=['xlsx'], key='matriz')
alimentador = st.file_uploader(
    '2. Selecione o Excel Alimentador', type=['xlsx'], key='alimentador'
)
modelo_ppt = st.file_uploader(
    '3. Selecione o modelo PowerPoint', type=['pptx'], key='modelo_ppt'
)

cenarios = st.text_input(
    '4. Números dos cenários, separados por vírgula',
    value='1,2,3',
    help='Use no máximo quatro números, por exemplo: 1,2,3',
)

if st.button('Gerar apresentação', type='primary', use_container_width=True):
    if not matriz or not alimentador or not modelo_ppt:
        st.error('Envie a matriz, o Excel Alimentador e o PowerPoint modelo.')
        st.stop()

    numeros = [item.strip() for item in cenarios.split(',') if item.strip()]
    if not numeros or len(numeros) > 4 or not all(item.isdigit() for item in numeros):
        st.error('Informe de um a quatro números válidos, separados por vírgula.')
        st.stop()

    with tempfile.TemporaryDirectory() as pasta:
        pasta = Path(pasta)
        arquivo_matriz = pasta / matriz.name
        arquivo_matriz.write_bytes(matriz.getvalue())

        arquivo_alimentador = pasta / 'Mezzo_Apresentação Saúde_2026_07_v1.xlsx'
        arquivo_alimentador.write_bytes(alimentador.getvalue())

        arquivo_ppt = pasta / 'Mezzo_Apresentação Saúde_2026_07_v1.pptx'
        arquivo_ppt.write_bytes(modelo_ppt.getvalue())

        base = Path(__file__).resolve().parent
        script = base / 'projetoestudo_streamlit.py'
        compat = base / 'colab_compat.py'
        (pasta / script.name).write_bytes(script.read_bytes())
        (pasta / compat.name).write_bytes(compat.read_bytes())

        env = os.environ.copy()
        env['UPLOAD_QUEUE'] = json.dumps([
            str(arquivo_matriz),
            str(arquivo_alimentador),
            str(arquivo_ppt),
        ], ensure_ascii=False)
        env['CENARIOS_SELECIONADOS'] = ','.join(numeros)

        with st.spinner('Processando matriz e gerando apresentação...'):
            processo = subprocess.run(
                [sys.executable, script.name],
                cwd=pasta,
                env=env,
                capture_output=True,
                text=True,
                timeout=900,
            )

        if processo.returncode != 0:
            st.error('O robô encontrou um erro durante o processamento.')
            with st.expander('Detalhes do erro'):
                st.code(processo.stderr or processo.stdout)
            st.stop()

        saida = pasta / 'Apresentador360_V2_FINAL.pptx'
        if not saida.exists():
            st.error('O processamento terminou, mas o PowerPoint final não foi criado.')
            with st.expander('Registro do processamento'):
                st.code(processo.stdout)
            st.stop()

        st.success('Apresentação gerada com sucesso!')
        st.download_button(
            'Baixar PowerPoint',
            data=saida.read_bytes(),
            file_name='Apresentador360_V2_FINAL.pptx',
            mime='application/vnd.openxmlformats-officedocument.presentationml.presentation',
            use_container_width=True,
        )
        with st.expander('Registro do processamento'):
            st.code(processo.stdout)
