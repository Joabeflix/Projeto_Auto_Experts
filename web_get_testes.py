import requests

# URL da imagem
url = "https://www.ideia2001.com.br/catmobile/FotoMobRetArq.asp?cerq=332&n=bravkds6315"

# Nome do arquivo para salvar a imagem
nome_arquivo = "imagem_baixada.jpg"

try:
    # Fazer a solicitação GET
    resposta = requests.get(url)
    # Verificar se a requisição foi bem-sucedida
    if resposta.status_code == 200:
        # Salvar o conteúdo da imagem em um arquivo
        with open(nome_arquivo, 'wb') as arquivo:
            arquivo.write(resposta.content)
        print(f"Imagem salva como {nome_arquivo}")
    else:
        print(f"Erro ao baixar a imagem: {resposta.status_code}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

