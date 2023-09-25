import os
import pandas as pd
import requests as rq
#import time
from methods.loaders.filesSave import FileSavers
from methods.transformers.transformData import TransformData
from methods.extractors.webPageDataScrapers import WebPageDataScrapers
from utils.tools import GeneralTools
from utils.driver import DriverChrome
from utils.selenium import GeneralSelenium
import utils.logger_config as logger_config
from utils.aws import AboutAWS
import logging

def main():
    try:
        fileSavers = FileSavers()
        transformData = TransformData()
        webPageDataScrapers = WebPageDataScrapers()
        generalTools = GeneralTools()
        driverChrome = DriverChrome()
        selenium = GeneralSelenium()
        df = pd.DataFrame()
        client = AboutAWS()
        # Variável contendo informações das moedas a serem coletadas, aws e banco de dados
        jsonData = generalTools.openJson()
        logger_config.setup_logger(generalTools.getDate())

        # Pegando última versão webdriver    
        latest_chrome_version = driverChrome.getLatestChromeVersion()

        generalTools.makeDirectory('chromeDriver')
        download_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromeDriver')
        
        # Baixa o ChromeDriver com base na versão mais recente do Chrome
        driverChrome.downloadChromeDriver(latest_chrome_version, download_directory) 
        
        name_directory = f"{jsonData['source']['generalLink']['params']['directory']}{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}"

        html, soup = webPageDataScrapers.requestGetDefault(jsonData['source']['generalLink']['url'])
        webPageDataScrapers.downloadUrl(html, jsonData['source']['generalLink']['params']['namehtml'], name_directory)
        
        Resume = {
                    1: fileSavers.saveValuesSizeOne,
                    4: fileSavers.saveValuesSizeFour,
                    5: fileSavers.saveValuesSizeFive,
                    6: fileSavers.saveValuesSizeSix,
                    8: fileSavers.saveValuesSizeEight,
                    9: fileSavers.saveValuesSizeNine,
                    10: fileSavers.saveValuesSizeTen
        }

        driver = selenium.startSelenium()
        for dept in range(25):
            departamento = soup.find_all('a', class_='nav-link')[dept].attrs['href']
            driver.get(departamento)
            if 'climatizacao' in departamento.split("/")[-1] or 'cama' in departamento.split("/")[-1]:
                continue
            #ok = generalTools.increase()
            #for produtodept in range(30):
            #path = f'/html/body/div[9]/div[1]/div[1]/section/div/div/div[1]/div/div[{generalTools.increase()}]/div/div/a'
            driver.implicitly_wait(10)
            #links = [elemento.get_attribute('href') for elemento in driver.find_elements(by='xpath', value=path)]
            checagem = True
            ind = 1
            while checagem:
                driver.get(departamento)
                conteudo = driver.find_elements(by='xpath', value=f"/html/body/div[9]/div[1]/div[1]/section/div/div/div[1]/div/div[{generalTools.increase()}]/div/div/a")
                links = [elemento.get_attribute('href') for elemento in conteudo]
                
                if generalTools.checkValue(links) == 'ENCERRAR':
                    continue
                checagem2 = True
                while checagem2:
                    driver.get(links[0]) if ind == 1 else driver.get(f"{links[0]}?page={ind}")
                    if 'caixas' in driver.current_url or driver.current_url == 'https://www.leroymerlin.com.br/acessorios-para-informatica-computadores?page=2':
                        checagem2 = False
                    page = driver.find_elements(by='xpath', value='/html/body/div[8]/div[4]/div[1]/div/div[3]/div/div')[0].text
                    if generalTools.checkEmptyValue(page) == 'NEXT':
                        checagem2 = False
                        ind = 0
                    page = page.split("EXCLUSIVO SITE\n") if dept != 0 else page.split("s\n")
                    i = 0
                    for size, item in [(len(sublista), sublista) for sublista in [parte.split("\n")for parte in page]]:
                        item = transformData.cleaningEmptySpace(item, links[0].split(".br/")[-1]) if len(item) != 1 else item
                        #[item[i:i+3] for i in range(0, len(item), 3)]
                        # Fazer um dicionáro para fazer um DE/PARA, com os links enviados
                        #Resume[size](item, links[0].split(".br/")[-1])
                        print(i)
                        #if i == 24:
                        #    print('ok')
                        Resume[len(item)](item, links[0].split(".br/")[-1])
                        i = i + 1
                    if generalTools.checkValueWithComparation(item, page[-1]) == 'NEXT':
                        ind = ind + 1
                        
        # ---------------------------------------------------------- CONTINUANDO LÓGICA
        
        #logging.info(f"DOCUMENTO CRIADO COM SUCESSO!")
        #s3 = client.createClient('s3')
        #localfile = f"{name_directory}/{fileName}.{file_type}"
        #client.uploadFile(s3, localfile, 'engdadostest', localfile)
        
    except FileNotFoundError as err:
        logging.error(f"ERRO: {generalTools.upperCase(err)}, O ARQUIVO JSON (data.json) NÃO FOI ENCONTRADO.")
    except (rq.exceptions.HTTPError, rq.exceptions.RequestException) as err:
        logging.error(f"ERRO DURANTE A REQUISIÇÃO: {generalTools.upperCase(err)}")
    except Exception as err:
        logging.error(f"ERRO DESCONHECIDO: {generalTools.upperCase(err)}")

if __name__ == '__main__':
    main()