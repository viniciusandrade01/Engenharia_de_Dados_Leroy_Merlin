import fastavro
#import datetime
import os
#import time
import pandas as pd
import utils.logger_config as logger_config
from utils.tools import GeneralTools
from methods.transformers.transformData import TransformData
import logging
from utils.charts import GeneralCharts
generalCharts = GeneralCharts()
generalTools = GeneralTools()
transformData = TransformData()
logger_config.setup_logger(generalTools.getDate())

class FileSavers:
    def __init__(self):
        self.df = pd.DataFrame(columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Produto', 'Desmembrar', 'Desconsiderar'])
        self.resume = {
                    1: self.saveValuesSizeOne, 2: self.saveValuesSizeTwo,
                    3: self.saveValuesSizeThree, 4: self.saveValuesSizeFour,
                    5: self.saveValuesSizeFive, 6: self.saveValuesSizeSix,
                    7: self.saveValuesSizeSeven, 8: self.saveValuesSizeEight,
                    9: self.saveValuesSizeNine, 10: self.saveValuesSizeTen,
                    11: self.saveValuesSizeEleven, 12: self.saveValuesSizeTwelve,
                    13: self.saveValuesSizeThirteen,
                    14: self.saveValuesSizeFourteen, 
                    15: self.saveValuesSizeFifteen, 16: self.saveValuesSizeSixteen
        }

    def saveValuesSizeOne(self, data: list, product: str):
        pass

    def saveValuesSizeTwo(self, data: list, product: str):
        pass

    def saveValuesSizeThree(self, data: list, product: str):
        pass

    def saveValuesSizeFour(self, data: list, product: str):
        if len(data) != 4:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Preco_Original', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeFive(self, data: list, product: str):
        if len(data) != 5:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        #self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Preco_Original', 'Desmembrar', 'Produto'])], ignore_index=True) if product != 'ar-condicionado' else pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Avaliacao','Preco_Original', 'Desmembrar', 'Produto'])], ignore_index=True)
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Preco_Original', 'Desmembrar', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeSix(self, data: list, product: str):
        if len(data) != 6:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        #self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Preco_Original', 'Parcela', 'Valor_Parcela', 'Produto'])], ignore_index=True)
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Desmembrar', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeSeven(self, data: list, product: str):
        data = transformData.cleaningEmptySpace("\n".join(data).split("EXCLUSIVO SITE")[-1].split("\n"), product)
        data = transformData.cleaningDataRepeated(data)
        #self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Produto', 'Desconsiderar'])], ignore_index=True)
        if len(data) != 7:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return 
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Preco_A_Vista', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeEight(self, data: list, product: str):
        if len(data) != 8:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Preco_A_Vista', 'Desmembrar', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeNine(self, data: list, product: str):
        if len(data) != 9:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Preco_Original', 'Preco_A_Vista', 'Desconsiderar', 'Desmembrar', 'Produto'])], ignore_index=True) if '$' in data[4] else pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Desmembrar', 'Produto'])], ignore_index=True)

    def saveValuesSizeTen(self, data: list, product: str):
        if len(data) != 10:
            self.resume.get(len(data), lambda data, product: None)(data, product)
            return
        #self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Parcela', 'Desmembrar', 'Produto'])], ignore_index=True)
        self.df = pd.concat([self.df, pd.DataFrame([data], columns=['Situacao', 'Var_Desconto', 'Descricao', 'Codigo', 'Avaliacao', 'Preco_Original', 'Preco_A_Vista', 'Desconsiderar','Desmembrar', 'Produto'])], ignore_index=True)
    
    def saveValuesSizeEleven(self, data: list, product: str):
        pass

    def saveValuesSizeTwelve(self, data: list, product: str):
        pass

    def saveValuesSizeThirteen(self, data: list, product: str):
        pass

    def saveValuesSizeFourteen(self, data: list, product: str):
        pass

    def saveValuesSizeFifteen(self, data: list, product: str):
        pass

    def saveValuesSizeSixteen(self, data: list, product: str):
        pass

    def openingSheets(self, directory: str, sheet: str, rows: int, footer: int):
        return pd.read_excel(f"{directory}", sheet_name=f"{sheet}", skiprows=rows, skipfooter=footer)

    def creatingFinalDataFrame(self, data: str, sep):
        novo_df = pd.DataFrame()
        self.df = pd.read_csv("Testec.csv", sep='\t')
        self.df.fillna("", inplace=True)
        novo_df['Situacao'] = self.df['Situacao'].map(lambda x: x.title())
        novo_df = novo_df[(novo_df['Situacao'] == 'Oferta') | (novo_df['Situacao'] == '')]
        novo_df['Var_Desconto'] = self.df['Var_Desconto'].map(lambda x: generalTools.removeMinus(generalTools.percentageToEmpty(x)))
        novo_df['Descricao'] = self.df['Descricao'].map(lambda x: generalTools.removeParentheses(generalTools.plusToNull(generalTools.barToNull(generalTools.hyphenToNull(generalTools.cleaningAll(generalTools.removeEllipsis(generalTools.cleaningStr(x))))))))
        #novo_df['Codigo'] = self.df['Codigo'].apply(lambda x: pd.to_numeric(generalTools.splitByEmptySpace(x)[-1], errors='coerce')).dropna().astype(int)
        novo_df['Codigo'] = self.df['Codigo'].map(lambda x: generalTools.splitByEmptySpace(x)[-1])
        novo_df = novo_df[(novo_df['Codigo'].map(lambda x: len(x)) == 10) | (novo_df['Codigo'].map(lambda x: len(x)) == 8)]
        novo_df['Avaliacao'] = self.df['Avaliacao'].map(lambda x: generalTools.removeParentheses(x))
        # SELECIONA OS CAMPOS COM VALORES DE AVALIAÇÕES COLETADOS
        #novo_df['Avaliacao] = novo_df[(novo_df['Avaliacao'].map(lambda x: len(x)) == 1) | (novo_df['Codigo'].map(lambda x: len(x)) == 2)]

        novo_df['Preco_Original'] = self.df['Preco_Original'].map(lambda x: generalTools.replaceCommaToDot(generalTools.dotToEmpty(generalTools.extractValue(x, r'R\$ (\d{1,3}(?:\.\d{3})*(?:,\d{2})?) cada') if pd.notnull(x) else x)))
        novo_df['Preco_A_Vista'] = self.df['Preco_A_Vista'].map(lambda x: generalTools.replaceCommaToDot(generalTools.dotToEmpty(generalTools.splitByEmptySpace(x.replace("cada",""))[-1])))
        novo_df['Produto'] = self.df['Produto'].map(lambda x: generalTools.hyphenToEmptySpace(x.title()).replace("Tv", "Televisao"))

        novo_df['Desmembrar'] = self.df['Desmembrar'].map(lambda x: generalTools.extractTwoValue(x, r'(\d+)x de R\$ ([\d,]+) s/juros', r'R\$ ([\d,]+) em até (\d+)x de R\$ ([\d,]+) s/juros', self.df))
        novo_df['Preco_Original'] = novo_df.apply(generalTools.updatePrice, axis=1)
        #novo_df['Desconsiderar'] = self.df['Desconsiderar']
        novo_df['Data_Captura'] = generalTools.splitByEmptySpace(data)[0]

        return novo_df
    
    def generateFile(self, novo_df: pd.DataFrame, file_type, diretorio, sep, fileName, columnsList: list, ofertas):

        novo_df = novo_df[columnsList]

        generalTools.makeDirectory(diretorio)
        diretorio = f"{diretorio}/{fileName}"

        if ofertas != "":
            novo_df = novo_df[novo_df['Situacao'] == 'Oferta']
    
        novo_df = novo_df.reset_index()
        novo_df.drop("index", axis=1, inplace=True)

        #generalCharts.createBoxChart(novo_df, 'Preco_Original', [8, 6], 'Gráfico de Caixa - Preço Original', 'blue')

        #createBoxChart(novo_df, 'Preco_A_Vista', [8, 6], 'Gráfico de Caixa - Preço à Vista', 'orange')

        if file_type == 'csv':
            novo_df.to_csv(f"{diretorio}.csv", sep=f"{sep}", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO CSV.") 
            return
        
        elif file_type == 'excel':
            novo_df.to_excel(f"{diretorio}.xlsx", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO EXCEL.")
            return
        
        elif file_type == 'json':
            novo_df.to_json(f"{diretorio}.json", orient='records')
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO JSON.")
            return
        
        elif file_type == 'parquet':
            novo_df.to_parquet(f"{diretorio}.parquet", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO PARQUET.")
            return
        
        elif file_type == 'hdf':
            novo_df.to_hdf(f"{diretorio}.h5", key='data')
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO HDF5/H5.")
            return
        
        elif file_type == 'pickle':
            novo_df.to_pickle(f"{diretorio}.pkl")
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO PICKLE.")
            return
        
        elif file_type == 'feather':
            novo_df.to_feather(f"{diretorio}.feather")
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO FEATHER.")
            return
        
        elif file_type == 'avro':
            with open(f"{diretorio}.avro", 'wb') as out_avro:
                fastavro.writer(out_avro, novo_df.to_dict(orient='records'))
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO AVRO.")
            return
        
        elif file_type == 'html':
            novo_df.to_html(f"{diretorio}.html", index=False)
            logging.info(f"DATAFRAME SALVO COMO {fileName} EM FORMATO HTML.")
            return
        
        else:
            logging.info("TIPO DE ARQUIVO NÃO SUPORTADO. ESCOLHA UM FORMATO VÁLIDO.")

    def concatDataFrame(self, df: pd.DataFrame, dictionary: dict, index: int):
        try:
            return pd.concat([df, pd.DataFrame(dictionary, index=[index])])
        except KeyError as e:
            logging.error(f"ERRO: {e}, A CHAVE {e} NÃO FOI ENCONTRADA NO DICIONÁRIO.")
        except Exception as e:
            logging.error(f"ERRO: {e}, NÃO FOI POSSÍVEL CONCATENAR OS DATAFRAMES.")