import pandas as pd
import time
from app import exec


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
            retorno = exec(codigo, ['nome', 'marca', 'aplicacao', 'peso', 'ean', 'ncm'])
            
            nome = retorno.get('nome')
            marca = retorno.get('marca')
            aplicacao = retorno.get('aplicacao')
            peso = retorno.get('peso')
            ean = retorno.get('ean')
            ncm = retorno.get('ncm')


            lista_nome.append(nome)
            lista_marca.append(marca)
            lista_aplicacao.append(aplicacao)
            lista_peso.append(peso)
            lista_ean.append(ean)
            lista_ncm.append(ncm)

        planilha['Nome'] = lista_nome
        planilha['Marca'] = lista_marca
        planilha['Aplicação'] = lista_aplicacao
        planilha['Peso'] = lista_peso
        planilha['Código de barras (EAN)'] = lista_ean
        planilha['NCM'] = lista_ncm

        print('Salvando')
        planilha.to_excel('modelo_planilha_new.xlsx', index=False)

exel().inserir_dados_planilha('modelo_planilha.xlsx')



