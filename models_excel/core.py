import pandas as pd
from utils.utils import texto_no_console, deixar_nome_ate_60_caracteres
from models_api.api_max import puxar_dados_api
from models_api.gerar_token import TokenGerador
import requests

class Gerar_Anuncios:
    def __init__(self, acces_token, planilha):
        self.acces_token=acces_token
        self.planilha=planilha


    def gerar_planilha(self):
        planilha = pd.read_excel(self.planilha)

        coluna_codigo = planilha['Cod Produto']
        coluna_nome_anuncio = []
        coluna_ean = []
        coluna_nome_ate_60 = []

        for cod in coluna_codigo:
            dados_puxar = ['grupo_produto', 'aplicacao', 'marca', 'part_number', 'ean', 'posicao', 'lado', 'imagem_url']
            dados_anuncio = puxar_dados_api(self.acces_token, codigo_produto=cod, dados_necessarios=dados_puxar)
            print(f'DADOS {dados_anuncio}')
            if not dados_anuncio:
                coluna_nome_anuncio.append('Não encontrado API')
                coluna_ean.append('Não encontrado API')
                coluna_nome_ate_60.append('Não encontrado API')
                continue
            nome_produto = dados_anuncio['grupo_produto']
            veiculo = dados_anuncio['aplicacao']
            posicao = dados_anuncio['posicao']
            lado = dados_anuncio['lado']
            marca = dados_anuncio['marca']
            codigo_produto = dados_anuncio['part_number']

            _nome_anuncio = f'{nome_produto} Compatível {veiculo[:veiculo.find('-')+5]} {posicao} {lado} {marca} {codigo_produto}'.title()
            nome_anuncio = " ".join(_nome_anuncio.replace('None', ' ').split()).title()

            nome_ate_60 = deixar_nome_ate_60_caracteres(nome_anuncio, codigo_produto, marca)
            coluna_nome_ate_60.append(nome_ate_60)

            coluna_nome_anuncio.append(nome_anuncio)
            coluna_ean.append(dados_anuncio['ean'])
            # self.baixar_imagem(url=dados_anuncio['imagem_url'], nome_arquivo=codigo_produto)
        
        planilha['nome anuncio completo'] = coluna_nome_anuncio
        planilha['nome anuncio < 60'] = coluna_nome_ate_60
        planilha['ean'] = coluna_ean

        salvar = planilha.to_excel('anuncios.xlsx', index=False)

    def baixar_imagem(self, url, nome_arquivo):
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                with open(f'{nome_arquivo}.jpg', 'wb') as f:
                    f.write(resposta.content)
                print(f"Imagem salva como: {nome_arquivo}")
            else:
                print(f"Erro ao baixar imagem. Código HTTP: {resposta.status_code}")
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    acces_token = TokenGerador().ler_token()
    app = Gerar_Anuncios(
        acces_token=acces_token,
        planilha='plan.xlsx')
    
    app.gerar_planilha()
    

# puxar_dados_api(access_token=acces_token, codigo_produto=codigo_produuto, dados_necessarios=dados)


