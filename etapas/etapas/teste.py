import pandas as pd

def ler_matriz(arquivo):

    excel = pd.ExcelFile(arquivo)

    return {
        "abas": excel.sheet_names,
        "quantidade_abas": len(excel.sheet_names)
    }
