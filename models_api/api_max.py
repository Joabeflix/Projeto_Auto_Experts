import requests
import json
import os
import tkinter as tk
from PIL import Image, ImageTk
from dotenv import load_dotenv
from models_api.gerar_token import TokenGerador
from models_api.mapeamentos import mapeamento_usar

load_dotenv()



class APICliente: 
    BASE_URL = 'https://api.intelliauto.com.br/v1/produtos/partnumber/'

    def __init__(self, access_token):
        self.access_token = access_token

    def obter_dados(self, part_number):

        url = f'{self.BASE_URL}{part_number}'
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            return f'Erro 401 ({response}) === Colocar tratamento de erro quando não tiver token'

        if response.status_code == 200:
            return response

class FiltroJSON:
    @staticmethod
    def filtrar_dados(data, filtro_json, item_filtro=None):
        try:
            retorno = eval(f"data{filtro_json}")
        except Exception as e:
            print(f"Erro ao acessar dados com o filtro: {e}")
            return f""
        if item_filtro:
            try:
                filtrados = [dado for dado in retorno if dado.get("item") == item_filtro]
                return filtrados[0]['descricao']
            except IndexError:
                return f'None'
        return retorno



def puxar_dados_api(access_token, codigo_produto, dados_necessarios=[]):
    api_cliente = APICliente(access_token=access_token)
    filtro = FiltroJSON()

    response = api_cliente.obter_dados(codigo_produto)
    dados = response.json()

    if not dados.get('data'):
        response = api_cliente.obter_dados(codigo_produto)
        dados = response.json()

    if not response or not dados.get('data'):
        return {}


    retorno = {}
    for chave in dados_necessarios:
        mapeamento = mapeamento_usar(chave=chave)
        valor = filtro.filtrar_dados(dados, mapeamento['caminho'], mapeamento['chave_secundaria'])
        retorno[chave] = valor

    return retorno


if __name__ == "__main__":

    acces_token = TokenGerador().ler_token()
    codigo_produuto = 'HG 31006'
    dados = ['nome', 'grupo_produto']
    print(puxar_dados_api(access_token=acces_token, codigo_produto=codigo_produuto, dados_necessarios=dados))
