import pandas as pd
import time
from app import TokenGerador, APICliente, JSONFilter


class exel():
    def __init__(self) -> None:
        pass

    def gerar_planilha_padrao(self, local_salvar):
        colunas = ['Código Produto', 'Nome', 'Marca', 'Aplicação', 'Peso', 'Código de barras (EAN)', 'NCM']
        planilha = pd.DataFrame(columns=colunas)
        planilha.to_excel('modelo_planilha.xlsx', index=False)


    def inserir_dados_planilha(self, caminho):
        planilha = pd.read_excel(caminho)

        lista_nome = []
        lista_marca = []
        lista_aplicacao = []
        lista_peso = []
        lista_codigo_de_barras = []
        lista_ncm = []

        for codigo in planilha['Código Produto']:
            token_manager = TokenGerador()
            api_cliente = APICliente(token_manager)
            filtro = JSONFilter()
            response = api_cliente.obter_dados(codigo)

            if response:
                data = response.json()
                nome = filtro.filtrar_dados(data, "['data'][0]['aplicacoes'][0]['descricao']")
                marca = filtro.filtrar_dados(data, "['data'][0]['marca']['nome']")
                aplicacao = filtro.filtrar_dados(data, "['data'][0]['aplicacoes'][0]['descricaoFrota']")
                peso = filtro.filtrar_dados(data, "['data'][0]['especificacoes']", "Peso bruto")
                codigo_de_barras = filtro.filtrar_dados(data, "['data'][0]['especificacoes']", "Código de barras (EAN)")
                ncm = filtro.filtrar_dados(data, "['data'][0]['especificacoes']", "NCM")

            lista_nome.append(nome)
            lista_marca.append(marca)
            lista_aplicacao.append(aplicacao)
            lista_peso.append(peso)
            lista_codigo_de_barras.append(codigo_de_barras)
            lista_ncm.append(ncm)

        planilha['Nome'] = lista_nome
        planilha['Marca'] = lista_marca
        planilha['Aplicação'] = lista_aplicacao
        planilha['Peso'] = lista_peso
        planilha['Código de barras (EAN)'] = lista_codigo_de_barras
        planilha['NCM'] = lista_ncm

        planilha.to_excel('modelo_planilha.xlsx', index=False)
            
exel().inserir_dados_planilha('modelo_planilha.xlsx')
