from app import puxar_dados_api
from app import ImagemProduto
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

class interface():
    def __init__(self, root):
        self.root = root

        tk.Label(root, text='Código do produto').place(x=19, y=3)
        self.entrada_codigo = ttk.Entry(root, width=15)
        self.entrada_codigo.place(x=20, y=24)

        self.botao_pesquisar = ttk.Button(root, text="Pesquisar", width=9, command=lambda: self.inserir_dados(self.buscar_conteudo(self.ler_codigo_produto())))
        self.botao_pesquisar.place(x=134, y=23)

        # Lista para armazenar as referências dos widgets Text
        self.blocos_texto = []

        # Posição inicial
        self.y_inicial_caixas = 90
        self.y_inicial_label = 69

        # Criar os widgets Text dinamicamente
        self.nomes_labels = ['Nome', 'Marca', 'Ean', 'NCM', 'Peso']
        for x in range(5):
            tk.Label(text=self.nomes_labels[x]).place(x=18, y=self.y_inicial_label)
            self.bloco_texto = tk.Text(root, height=1, width=25)
            self.bloco_texto.place(x=20, y=self.y_inicial_caixas)
            self.blocos_texto.append(self.bloco_texto)  # Armazena a referência na lista
            self.y_inicial_caixas += 50
            self.y_inicial_label+=51

        self.bloco_texto_aplicacao = tk.Text(root, height=14, width=45)
        self.bloco_texto_aplicacao.place(x=210, y=90)

    # Função para inserir dados nos blocos
    def inserir_dados(self, lista_de_dados={}):

        indice = 0
        sequencia = ['nome', 'marca', 'ean', 'ncm', 'peso', 'aplicacao']

        # Inserindo dados nas linhas
        for i, bloco in enumerate(self.blocos_texto):
            bloco.delete("1.0", "end")  # Limpa o conteúdo existente
            bloco.insert("1.0", f"{lista_de_dados.get(sequencia[indice])}")  # Insere o novo conteúdo
            indice+=1
        # Inserindo dados na caixa de aplicação que é feita fora do looping
        self.bloco_texto_aplicacao.insert("1.0", f"{lista_de_dados.get('aplicacao')}")


    def ler_codigo_produto(self):
        
        codigo_produto = self.entrada_codigo.get()
        codigo_produto = codigo_produto.upper()
        if codigo_produto:
            return codigo_produto
        messagebox.showwarning("Erro", "Você não digitou um código.")
        return None


    def buscar_conteudo(self, codigo_produto):
        retorno = puxar_dados_api(codigo_produto, ['nome', 'marca', 'ean', 'ncm', 'peso', 'aplicacao', ])
        baixar_imagem = ImagemProduto(codigo_produto).baixar_imagem()
        print('Dentro de buscar conteúdo')
        print(f'conteúdo: {retorno}')
        print(f'type conteúdo: {type(retorno)}')
        return retorno

    def mostrar_imagem(self, codigo_produto):
        if codigo_produto:
            imagem = ImagemProduto(codigo_produto)
            imagem.mostrar_imagem(self.root)
        return None

# Inicializa a interface gráfica e executa o loop principal do Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    meu_app = interface(root)
    root.title('Catálogo AutoExperts')
    root.geometry('520x360')
    root.minsize(width=520, height=360)
    root.maxsize(width=520, height=360)
    root.mainloop()
    ImagemProduto().limpar_imagens()
    