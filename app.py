import requests
from token_gerador import gerar_arquivo_token, ler_txt_token
import json

# token_acesso = get_access_token(client_key_value, client_secret_value)
def retorno_dados(part_number):

    access_token = ler_txt_token()

    url = f'https://api.intelliauto.com.br/v1/produtos/partnumber/{part_number}'
    headers = {'accept': 'application/json', 'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
         gerar_arquivo_token()
         return retorno_dados(part_number)

    if response.status_code == 200:
        return response
    
def filtro_dados_json(part_number, filtro_json, item_filtro=None):
    data = retorno_dados(part_number).json()

    # Avaliação do caminho fornecido no filtro
    try:
        retorno = eval(f"data{filtro_json}")
    except Exception as e:
        return f"Erro ao acessar dados com o filtro: {e}"

    # Filtro adicional baseado no campo "item", se fornecido
    try:
        if item_filtro:
            filtrados = [dado for dado in retorno if dado.get("item") == item_filtro]
            retorno = filtrados[0]['descricao']
            return retorno
    except IndexError:
        return f'"{item_filtro}" indisponível.'
    return retorno

# Exemplo de uso + Caminhos no json (Lembrando que passamos o caminho bruto e
# Junto com a função enviamos o item que vamos puxar)

cod_porduto_teste = input("Digite o código que deseja pesquisar: ")
cod_porduto_teste = cod_porduto_teste.replace(' ', '').replace('  ', '')

print(f'Marca: {filtro_dados_json(cod_porduto_teste, "['data'][0]['marca']['nome']")}')
print(f'Aplicação: {filtro_dados_json(cod_porduto_teste, "['data'][0]['aplicacoes'][0]['descricaoFrota']")}')
print(f'Peso: {filtro_dados_json(cod_porduto_teste, "['data'][0]['especificacoes']", "Peso bruto")}')

