import yaml

def ler_arquivo_config(caminho_arquivo: str) -> None:

    with open(caminho_arquivo, 'r') as file:
        dados = yaml.safe_load(file)
        return dados