import requests
import json
import os


class TokenGerador:
    def __init__(self):
        pass

    CLIENT_KEY=os.getenv('CLIENT_KEY')
    CLIENT_SECRET=os.getenv('CLIENT_SECRET')
 
    def get_access_token(self):

        token_url = 'https://api.intelliauto.com.br/v1/login'
        token_payload = {
            'clientKey': self.CLIENT_KEY,
            'clientSecret': self.CLIENT_SECRET
        }
        token_response = requests.post(token_url, json=token_payload)
        if token_response.status_code == 200:
            return token_response.json().get('accessToken')
        return None

    def gerar_arquivo_token(self):
        token = self.get_access_token()
        with open("token.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(token)

    def ler_txt_token(self):
        try:
            with open("token.txt", "r", encoding="utf-8") as arquivo:
                access_token = arquivo.read()
                return access_token
            
        except FileNotFoundError:
            self.gerar_arquivo_token()
            self.ler_txt_token()

class APICliente:
    BASE_URL = 'https://api.intelliauto.com.br/v1/produtos/partnumber/'
    
    def __init__(self, token_manager):
        self.token_manager = token_manager

    def obter_dados(self, part_number):

        access_token = self.token_manager.ler_txt_token()
        url = f'{self.BASE_URL}{part_number}'
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
            self.token_manager.gerar_arquivo_token()
            return self.obter_dados(part_number)

        if response.status_code == 200:
            return response

class JSONFilter:

    @staticmethod
    def filtrar_dados(data, filtro_json, item_filtro=None):
        try:
            retorno = eval(f"data{filtro_json}")
        except Exception as e:
            return f"Erro ao acessar dados com o filtro: {e}"
        
        if item_filtro:
            try:
                filtrados = [dado for dado in retorno if dado.get("item") == item_filtro]
                return filtrados[0]['descricao']
            except IndexError:
                return f'"{item_filtro}" indisponível.'
        return retorno
    


def exec():

    token_manager = TokenGerador()
    api_cliente = APICliente(token_manager)
    filtro = JSONFilter()
    cod_porduto_teste = input("Digite o código que deseja pesquisar: ").replace('  ', '')
    response = api_cliente.obter_dados(cod_porduto_teste)

    if response:
        data = response.json()
        print(f'Marca: {filtro.filtrar_dados(data, "['data'][0]['marca']['nome']")}')
        print(f'Aplicação: {filtro.filtrar_dados(data, "['data'][0]['aplicacoes'][0]['descricaoFrota']")}')
        print(f'Peso: {filtro.filtrar_dados(data, "['data'][0]['especificacoes']", "Peso bruto")}')
    return None

if __name__ == "__main__":
    exec()
