import os

from loguru import logger
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AppLinkedin():

    def __init__(
            self,
            url: str,
            login: str,
            senha: str
        ):
        
        self.url = url
        options = self.__options()
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 30)

        self.__login_site(login, senha)

    def __options(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")

        return options

    def __login_site(self, login: str, senha: str):

        try:
            logger.info('Iniciando site Linkedin...')
            self.driver.get(self.url)
        
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Entrar com e-mail')]"))).click()

            logger.info('Fazendo login...')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys(login)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(senha)

            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Entrar')]"))).click()

            logger.success('Login feito com sucesso!')

        except Exception as error:
            raise Exception(f'Erro ao fazer login | {str(error)}')
        
    def buscar_pessoas(self) -> list[dict]:

        try:
            logger.info('Pesquisando pessoas programadoras')

            pesquisa = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Pesquisar']")))
            pesquisa.click()
            pesquisa.clear()
            pesquisa.send_keys('Programador')
            pesquisa.send_keys(Keys.ENTER)

            filtros_pesquisa = self.wait.until(EC.visibility_of_all_elements_located(
                (By.XPATH, "//nav[@aria-label='Filtros de pesquisa']//ul/li")))
            
            for filtro in filtros_pesquisa:
                if 'PESSOAS' in filtro.text.upper():
                    filtro.click()
                    break
            
            logger.info('Filtro de pessoas aplicado')

            # ___ Percorre 5 páginas ___
            dados_pessoas = []
            for pagina in range(1, 10):

                lista_pessoas = self.wait.until(EC.visibility_of_all_elements_located(
                    (By.XPATH, "//div[@class='search-results-container']//div[2]//ul[@role='list']/li")))
                
                for pessoa in lista_pessoas:

                    if 'enviar mensagem' in pessoa.text.lower():
                        continue
                    
                    dados = pessoa.text.split('\n')
                    if 'Status' in dados[0]:
                        dados = dados[1:]

                    dados_pessoa = {
                        'nome': dados[0],
                        'localidade': dados[5],
                        'habilidades': dados[4],
                    }
                    
                    dados_pessoas.append(dados_pessoa)

                logger.info('Mudando para próxima página')

                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//button[@aria-label='Avançar']"))).click()
                
            return dados_pessoas

        except Exception as error:
            raise Exception(f'Erro ao buscar pessoas | {str(error)}')


