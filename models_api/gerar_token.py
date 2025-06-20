import os
from dotenv import load_dotenv
import requests
import json
from utils.utils import *


load_dotenv()

class TokenGerador:
    def __init__(self):
        pass

    CLIENT_KEY=os.getenv('CLIENT_KEY')
    CLIENT_SECRET=os.getenv('CLIENT_SECRET')
 
    def _gerar_token(self):
        token_url = 'https://api.intelliauto.com.br/v1/login'
        token_payload = {
            'clientKey': self.CLIENT_KEY,
            'clientSecret': self.CLIENT_SECRET
        }
        texto_no_console(f'Arquivo enviado: {token_payload}')
        token_response = requests.post(token_url, json=token_payload)
        if token_response.status_code == 200:
            token = token_response.json().get('accessToken')
            texto_no_console(f'Token: {token}')
            return token
        return None

    def definir_novo_token(self):
        token = self._gerar_token()
        with open(r"configs\token.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(token)

    def ler_token(self):
        """
        Essa é a única função que 
        """
        try:
            with open(r"configs\token.txt", "r", encoding="utf-8") as arquivo:
                access_token = arquivo.read()
                return access_token
            
        except FileNotFoundError:
            self.definir_novo_token()
            self.ler_token()


if __name__ == "__main__":
    app = TokenGerador()
    texto_no_console(app.ler_token())