import os
import traceback

from pathlib import Path
from loguru import logger
from datetime import datetime

from src.linkedin import AppLinkedin
from src.enviar_email import enviar_email
from src.utils import ler_arquivo_config
from src.planilha_retorno import registrar_planilha

def main():
    try:
        data_atual = datetime.now().strftime('%Y-%m-%d')

        # ___ Pastas do assets ___
        assets = Path('assets')
        pasta_csv = os.path.join(assets, 'csv')
        pasta_yaml = os.path.join(assets, 'yaml')
        pasta_logs = os.path.join(assets, 'logs')

        # ___ Arquivos ___
        arquivo_config = os.path.join(pasta_yaml, 'config.yaml')
        arquivo_logs = os.path.join(pasta_logs, f'{data_atual}.log')

        logger.add(sink=arquivo_logs)

        # ___ Configurações ___
        CONFIG = ler_arquivo_config(arquivo_config)
        URL_LINKEDIN = CONFIG['URL_LINKEDIN']
        LOGIN = CONFIG['AUTENTICACAO']['LOGIN']
        SENHA = CONFIG['AUTENTICACAO']['SENHA']
        CAMINHO_CSV = CONFIG['CAMINHO_CSV']
        
        arquivo_csv = os.path.join(CAMINHO_CSV, 'dados_linkedin.csv')

        app_linkedin = AppLinkedin(
            url=URL_LINKEDIN,
            login=LOGIN,
            senha=SENHA
        )

        dados_pessoas = app_linkedin.buscar_pessoas()

        registrar_planilha(info_dados=dados_pessoas, caminho_arquivo=arquivo_csv)

        enviar_email(
            destinatario='lucas.mal2005@gmail.com',
            assunto='Dados Linkedin',
            corpo='Realizada busca de dados de pessoas no linkedin<br>Segue planilha...',
            arquivo=arquivo_csv
        )

    except Exception:
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    main()