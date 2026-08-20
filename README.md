# Apresentador 360 V2

Versão preparada para execução local e publicação no GitHub, sem dependência do Google Colab.

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
python Apresentador360_V2_GitHub.py --matriz "matriz.xlsx" --modelo "alimentador.xlsx" --ppt "modelo.pptx"
```

Se os argumentos não forem informados, o programa solicitará os caminhos dos arquivos.

## Entradas

- Excel da matriz (`.xlsx`)
- Excel Alimentador (`.xlsx`)
- PowerPoint modelo (`.pptx`)

## O que foi convertido

- Removido `google.colab.files.upload()`
- Removido `google.colab.files.download()`
- Removidos comandos `!pip`
- Adicionada leitura de arquivos por caminho local
- Mantido o fluxo e a lógica do projeto original
