import json
import os
import datetime
import logging

class GeneralTools:
    def __init__(self):
        self.contador = 0

    def validateDate(self, data: str, data_param: dict):
        try:
            data_param = f"{data_param['year']}-{data_param['month']}"
            return data if data_param > data[:-3] else f"{data_param}-01"
        except ValueError:
            logging.info ("A ESTRUTURA DA DATA_PARAM NÃO É VÁLIDA. DEVE SER NO FORMATO '%Y-%m', EX.: Year = 2023, Month = 06")
    
    def makeDirectory(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def getDate(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def openJson(self):
        with open('utils\data.json') as json_file:
            return json.load(json_file)
    
    def hyphenToNull(self, dado: str):
        return dado.replace("-","")
    
    def hyphenToEmptySpace(self, dado: str):
        return dado.replace("-"," ")
    
    def splitByEmptySpace(self, dado: str):
        return dado.split(" ")
    
    def brlToEmpty(self, dado: str):
        return dado.replace("R$","")
    
    def commaToEmpty(self, dado: str):
        return dado.replace(",","")
    
    def dotToEmpty(self, dado: str):
        return dado.replace(".","")
    
    def emptyValueToEmpty(self, dado: str):
        return dado.replace (" ","")
    
    def percentageToEmpty(self, dado: str):
        return dado.replace("%","")

    def zeroToEmpty(self, dado: str):
        return dado.replace("0","")
    
    def nanToEmpty(self, dado: str):
        return dado.replace("nan", "")
    
    def removeParentheses(self, dado: str):
        return dado.replace("(","").replace(")","")
    
    def upperCase(self, dado: str):
        return dado.upper()
    
    def lowerCase(self, dado: str):
        return dado.lower()

    def increase(self):
        self.contador += 1
        return self.contador
    
    def checkValue(self, data):
        return 'CONTINUAR' if len(data) != 0 else 'ENCERRAR'

    def checkValueWithComparation(self, data, page):
        return 'NEXT' if page.split("\n")[0] == data[0] else 'CONTINUAR'
    
    def checkEmptyValue(self, page):
        return 'NEXT' if page == '' else 'CONTINUAR'