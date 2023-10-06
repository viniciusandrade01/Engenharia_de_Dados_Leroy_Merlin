import os
import pandas as pd
import requests as rq
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
        logging.info("ÚLTIMA VERSÃO DO WEBDRIVER COLETADA COM SUCESSO.")

        generalTools.makeDirectory('chromeDriver')
        download_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)),'chromeDriver')
        
        # Baixa o ChromeDriver com base na versão mais recente do Chrome
        driverChrome.downloadChromeDriver(latest_chrome_version, download_directory) 
        logging.info("BAIXANDO ÚLTIMA VERSÃO DO WEBDRIVER.")
        
        name_directory = f"{jsonData['source']['generalLink']['params']['directory']}{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}"
        
        # --- AJUSTAR, MOVER LÁ PRA BAIXO
        #df, alt_df = fileSavers.validatingStructure(generalTools.getDate(), "\t")
        
        #df = transformData.movingDataToRightColumn(df, alt_df)
        # criar função de dataframe, a partir da validação de estrutura acima

        #fileSavers.generateFile(df, jsonData['source']['generalLink']['filetype'], name_directory, "\t", f"{jsonData['source']['generalLink']['params']['nameFileGeral']}{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}", ['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Produto', 'Data_Captura'], "")

        #fileSavers.generateFile(df, jsonData['source']['generalLink']['filetype'], name_directory, "\t", f"{jsonData['source']['generalLink']['params']['nameFileOfertas']}{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}", ['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Produto', 'Data_Captura'], "Ofertas")
        # ---- ITENS ACIMA

        html, soup = webPageDataScrapers.requestGetDefault(jsonData['source']['generalLink']['url'])
        webPageDataScrapers.downloadUrl(html, jsonData['source']['generalLink']['params']['namehtml'], name_directory)
        logging.info("INFORMAÇÕES DA URL BAIXADA COM SUCESSO.")
        
        # DICIONÁRIO PARA FILTRAR A FUNÇÃO IDEAL PARA ORGANIZAÇÃO DOS DADOS
        Resume = {
                    1: fileSavers.saveValuesSizeOne, 2: fileSavers.saveValuesSizeTwo,
                    3: fileSavers.saveValuesSizeThree, 4: fileSavers.saveValuesSizeFour,
                    5: fileSavers.saveValuesSizeFive, 6: fileSavers.saveValuesSizeSix,
                    7: fileSavers.saveValuesSizeSeven, 8: fileSavers.saveValuesSizeEight,
                    9: fileSavers.saveValuesSizeNine, 10: fileSavers.saveValuesSizeTen,
                    11: fileSavers.saveValuesSizeEleven, 12: fileSavers.saveValuesSizeTwelve,
                    13: fileSavers.saveValuesSizeThirteen,
                    14: fileSavers.saveValuesSizeFourteen, 
                    15: fileSavers.saveValuesSizeFifteen, 16: fileSavers.saveValuesSizeSixteen
        }

        driver = selenium.startSelenium()
        # ITENS DEPARTAMENTOS
        for dept in range(25):
            departamento = soup.find_all('a', class_='nav-link')[dept].attrs['href']
            driver.get(departamento)
            if 'climatizacao' in departamento.split("/")[-1] or 'cama' in departamento.split("/")[-1]:
                continue
            
            driver.implicitly_wait(10)
            checagem = True
            ind = 1

            # SUBITENS DOS DEPARTAMENTOS
            aux = 0
            while checagem:
                driver.get(departamento)
                aux = aux + 1
                conteudo = driver.find_elements(by='xpath', value=f"/html/body/div[9]/div[1]/div[1]/section/div/div/div[1]/div/div[{aux}]/div/div/a")
                links = [elemento.get_attribute('href') for elemento in conteudo]

                if generalTools.checkValue(links) == 'ENCERRAR':
                    checagem = False
                    continue
                checagem2 = True
                while checagem2:
                    driver.get(links[0]) if ind == 1 else driver.get(f"{links[0]}?page={ind}")
                    if 'caixas' in driver.current_url or 'computadores' in driver.current_url or 'projetores' in driver.current_url or 'ring-light' in driver.current_url or 'drones' in driver.current_url or 'cftv' in driver.current_url or 'informatica' in driver.current_url or ('eletroportateis' in driver.current_url and ind == 2):
                        checagem2 = False
                        continue
                    page = driver.find_elements(by='xpath', value='/html/body/div[8]/div[4]/div[1]/div/div[3]/div/div')
                    
                    if generalTools.checkEmptyValue(page) == 'NEXT' or generalTools.checkValue(page) == 'ENCERRAR':
                        checagem2 = False
                        ind = 1
                        continue
                    page = page[0].text
                    if generalTools.checkEmptyValue(page) == 'NEXT':
                        checagem2 = False
                        ind = 1
                        continue
                    
                    page = page.split("cada\n") if 'eletroportateis' in driver.current_url else page.split("EXCLUSIVO SITE\n") if dept != 0 else page.split("s\n")
                    i = 0
                    for size, item in [(len(sublista), sublista) for sublista in [parte.split("\n")for parte in page]]:
                        
                        item = transformData.cleaningEmptySpace(item, links[0].split(".br/")[-1]) if len(item) != 1 else item
                        
                        print(f"Index: {i} / Url: {driver.current_url}")
                        if len(item) > 16:
                            i = i + 1
                            continue
                            #item = "\n".join(item).split("EXCLUSIVO SITE\n")
                        Resume[len(item)](item, links[0].split(".br/")[-1])
                        i = i + 1
                    if generalTools.checkValueWithComparation(item, page[-1]) == 'NEXT':
                        ind = ind + 1
        
        logging.info("DOCUMENTO CRIADO COM SUCESSO!")
        fileSavers.creatingFinalDataFrame(generalTools.getDate(), f"{jsonData['source']['generalLink']['params']['nameFile']}_{generalTools.hyphenToNull(generalTools.splitByEmptySpace(generalTools.getDate())[0])}", "\t", name_directory, jsonData['source']['generalLink']['filetype'])
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