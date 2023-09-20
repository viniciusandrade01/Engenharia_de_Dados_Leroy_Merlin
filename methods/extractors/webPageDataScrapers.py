import boto3
#import datetime
import zipfile
import os
import requests as rq
import uuid
from bs4 import BeautifulSoup as bs4
#import time
import utils.logger_config as logger_config
import logging
import locale
from utils.tools import GeneralTools
from utils.aws import AboutAWS

generalTools = GeneralTools()
jsonData = generalTools.openJson()
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
logger_config.setup_logger(generalTools.getDate())

class WebPageDataScrapers:
    def __init__(self):
        #self.xlsx = []
        #self.zip = []
        self.client = AboutAWS()

    #def extractInfoUrl(self, html, data_param: dict):
        #dataref = str(html.find_all('div', class_='descricao')).split("<p>")[-1].split("</p>")[0].replace(" – "," - ").split(" - ")[-1]
        #nome_zip = f"Anexo_RMD_{datetime.datetime.strptime(dataref, '%B de %Y').strftime('%B_%y').capitalize()}.zip"
        #data_capt = generalTools.validateDate(datetime.datetime.strptime(dataref, "%B de %Y").strftime("%Y-%m-01"), data_param)
        #link_zip = html.find_all("a", {"title": f"{nome_zip}"})[0].get('href')
        #return dataref, nome_zip, link_zip, data_capt

    def extractZip(self, nome_zip: str, namedirectory: str):
        generalTools.makeDirectory(namedirectory)
        with zipfile.ZipFile(nome_zip, 'r') as zip_ref:
            zip_ref.extractall(namedirectory)
            zip_ref.close()

        # Remova o arquivo ZIP depois de extraído
        os.remove(nome_zip)

    def downloadUrl(self, response, nome_arquivo, namedirectory):
        with open(nome_arquivo, 'wb') as file:
            file.write(response.content)
            #client = self.client.createClient('s3')
            #self.client.uploadFile(client, nome_arquivo, 'engdadostest', f"{namedirectory}/{nome_arquivo}")

    def requestGetDefault(self, link: str):
        try:
            html = rq.get(link)
            html.raise_for_status()
            soup = bs4(html.text, 'html.parser')

        except rq.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP: {http_err}")
        except rq.exceptions.RequestException as req_err:
            logging.error(f"Erro de Requisição: {req_err}")
        except Exception as err:
            logging.error(f"Erro Desconhecido: {err}")
        
        #return html, soup, dataref, nome_zip, link_zip, self.xlsx[0], data_capt, name_directory
        return html, soup