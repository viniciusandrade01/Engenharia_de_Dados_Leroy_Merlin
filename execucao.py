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
        
        # TESTE

        driver = selenium.startSelenium()
        for produtos in range(25):
            driver.get(soup.find_all('a', class_='nav-link')[produtos].attrs['href'])
            if 'climatizacao' in driver.current_url.split("/")[-1]:
                continue
            #ok = generalTools.increase()
            #for produtodept in range(30):
            path = f'/html/body/div[9]/div[1]/div[1]/section/div/div/div[1]/div/div[{generalTools.increase()}]/div/div/a'
            driver.implicitly_wait(10)
            links = [elemento.get_attribute('href') for elemento in driver.find_elements(by='xpath', value=path)]
            #check = generalTools.checkValue(links)
            if generalTools.checkValue(links) == 'ENCERRAR':
                continue
            #auxhtml, auxsoup = webPageDataScrapers.requestGetDefault(links[0])
            #webPageDataScrapers.downloadUrl(auxhtml, f"jsonData['source']['generalLink']['params']['namehtml']{auxhtml.url.split("/")[-1].replace("-","")}", name_directory)
            driver.get(links[0])
            page = driver.find_elements(by='xpath', value='/html/body/div[8]/div[4]/div[1]/div/div[3]/div/div')[0].text
            page = page.split("EXCLUSIVO SITE\n") if produtos != 0 else page.split("s\n")

            Resume = {
                1: fileSavers.saveValuesSizeOne,
                4: fileSavers.saveValuesSizeFour,
                5: fileSavers.saveValuesSizeFive,
                6: fileSavers.saveValuesSizeSix,
                8: fileSavers.saveValuesSizeEight,
                9: fileSavers.saveValuesSizeNine,
                10: fileSavers.saveValuesSizeTen
            }
            #for changePage in range(10):
            i = 0
            for size, item in [(len(sublista), sublista) for sublista in [parte.split("\n")for parte in page]]:
                i = i + 1
                item = transformData.cleaningEmptySpace(item, links[0].split(".br/")[-1]) if len(item) != 1 else item
                #[item[i:i+3] for i in range(0, len(item), 3)]
                # Fazer um dicionáro para fazer um DE/PARA, com os links enviados
                #Resume[size](item, links[0].split(".br/")[-1])
                if i == 35:
                    print('ok')
                Resume[len(item)](item, links[0].split(".br/")[-1])
            _=1

            #webPageDataScrapers.downloadUrl(html, jsonData['source']['generalLink']['params']['namehtml'], name_directory)
            #webPageDataScrapers.extractInfoUrl()
            continue

        # ---------------------------------------------------------- CONTINUANDO LÓGICA
        #logging.info(f"SALVANDO ARQUIVO XLSX, DO ZIP, REFERENTE AOS RELATÓRIOS MENSAIS DEDÍVIDA.")
        #df = fileSavers.openingSheets(f"{name_directory}/{name_file}", '2.2', 6, 6)

        #df = transformData.deletingColumns(df, data_capt)

        #df = transformData.selectingData(df, 'Título', jsonData['source']['generalLink']['rmd22'])
            
        #fileName, file_type = fileSavers.creatingFinalDataFrame(df, dataref, f'R_Mensal_Divida_{generalTools.hyphenToNull(data_capt)}', '\t', name_directory, data_capt, generalTools.lowerCase(jsonData['source']['generalLink']['filetype']))
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