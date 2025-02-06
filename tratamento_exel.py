import pandas as pd
import time
from app import puxar_dados_api


class exel():
    def __init__(self):
        pass

    def gerar_planilha_padrao(self, local_salvar):
        colunas = ['Código Produto', 'Nome', 'Marca', 'Aplicação', 'Peso', 'Código de barras (EAN)', 'NCM']
        planilha = pd.DataFrame(columns=colunas)
        planilha.to_excel('modelo_planilha.xlsx', index=False)


    def inserir_dados_planilha(self, caminho):
        print('Dentro de insirir dados na planilha')
        planilha = pd.read_excel(caminho)

        lista_nome = []
        lista_marca = []
        lista_aplicacao = []
        lista_peso = []
        lista_ean = []
        lista_ncm = []

        for codigo in planilha['Código Produto']:
            retorno = puxar_dados_api(codigo, ['nome', 'marca', 'aplicacao', 'peso', 'ean', 'ncm'])
            
            lista_nome.append(retorno.get('nome'))
            lista_marca.append(retorno.get('marca'))
            lista_aplicacao.append(retorno.get('aplicacao'))
            lista_peso.append(retorno.get('peso'))
            lista_ean.append(retorno.get('ean'))
            lista_ncm.append(retorno.get('ncm'))

        planilha['Nome'] = lista_nome
        planilha['Marca'] = lista_marca
        planilha['Aplicação'] = lista_aplicacao
        planilha['Peso'] = lista_peso
        planilha['Código de barras (EAN)'] = lista_ean
        planilha['NCM'] = lista_ncm

        print('Salvando')
        planilha.to_excel('modelo_planilha_new.xlsx', index=False)

exel().inserir_dados_planilha('modelo_planilha.xlsx')






