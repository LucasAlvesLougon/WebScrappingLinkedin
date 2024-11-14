import os
import pandas as pd

def registrar_planilha(info_dados: list, caminho_arquivo: str):
    try:
        df = pd.DataFrame(info_dados)
        df.to_csv(caminho_arquivo, index=False, sep=';')

    except Exception as error:
        raise Exception(f'Erro ao registrar planilha | {str(error)}')