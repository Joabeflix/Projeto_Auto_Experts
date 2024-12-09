import tkinter as tk
from PIL import Image, ImageTk



class MostrarImagem():
    def __init__(self):
        pass
    
    def get_url(self):
        
    

    def baixar_imagem(self, codigo_produto):
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



    

    def mostrar_imagem(self, nome_aba):
        # Criação da janela principal
        root = tk.Tk()
        root.title(nome_aba)

        # Carregar a imagem com Pillow
        image_path = "imagem.jpg"  # Substitua pelo caminho da sua imagem
        img = Image.open(image_path)

        # Redimensionar a imagem (opcional)
        # img = img.resize((300, 300))  # Ajuste a largura e altura conforme necessário

        # Converter a imagem para um formato compatível com o Tkinter
        tk_image = ImageTk.PhotoImage(img)

        # Criar um widget Label para exibir a imagem
        label = tk.Label(root, image=tk_image)
        label.pack()

        # Iniciar o loop principal do Tkinter
        root.mainloop()

