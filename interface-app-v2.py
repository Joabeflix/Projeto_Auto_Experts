from app import puxar_dados_api
from app import ImagemProduto
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import ttkbootstrap as ttk

class interface():
    def __init__(self, root):
        self.root = root

        # Gerando a interface
        tk.Label(root, text='Código do produto').place(x=19, y=3)
        self.entrada_codigo = ttk.Entry(root, width=15)
        self.entrada_codigo.place(x=20, y=24)

        self.botao_pesquisar = ttk.Button(root, text="Pesquisar", width=9, command=lambda: self.inserir_dados(self.buscar_conteudo(self.ler_codigo_produto())))
        self.botao_pesquisar.place(x=134, y=23)

        self.botao_imagem = ttk.Button(root, text="Ver imagem", width=13, command=lambda: self.mostrar_imagem(self.ler_codigo_produto()))
        self.botao_imagem.place(x=49, y=325)
        
        tk.Label(root, text='Produto').place(x=210, y=69)
        self.entrada_nome = tk.Text(root, height=1, width=45)
        self.entrada_nome.place(x=210, y=90)

        self.botao_funcao_exel = ttk.Button(root, text="Via Exel", width=13, command=lambda: self.interface_via_exel())
        self.botao_funcao_exel.place(x=300, y=325)



        # Criar os widgets Text dinamicamente
        # Lista para armazenar as referências dos widgets Text
        self.blocos_texto = []

        # Posição inicial
        self.y_inicial_caixas = 90
        self.y_inicial_label = 69

        # Esses nomes é os que vai gerar na interface
        self.nomes_labels = ['Marca', 'Ean', 'NCM', 'Peso']

        # Fazendo um looping de 5 e gerando 5 caixas de texto
        # Após cada geração, aumentamos os pixels da variavél
        # que usamos para os indices iniciais
        # fazendo assim o looping gera a interface com os blocos
        # um abaixo do outro

        for x in range(4):

            tk.Label(text=self.nomes_labels[x]).place(x=18, y=self.y_inicial_label)

            self.bloco_texto = tk.Text(root, height=1, width=25)
            self.bloco_texto.place(x=20, y=self.y_inicial_caixas)

            # Armazena a referência na lista
            self.blocos_texto.append(self.bloco_texto)

            self.y_inicial_caixas += 50
            self.y_inicial_label+=51

        tk.Label(root, text='Aplicação').place(x=212, y=120)
        self.bloco_texto_aplicacao = tk.Text(root, height=8, width=45)
        self.bloco_texto_aplicacao.place(x=210, y=140)



    # Função para inserir dados nos blocos
    def inserir_dados(self, lista_de_dados={}):

        indice = 0
        sequencia = ['marca', 'ean', 'ncm', 'peso']

        # Inserindo dados nas linhas
        for i, bloco in enumerate(self.blocos_texto):
            bloco.delete("1.0", "end")  # Limpa o conteúdo existente
            bloco.insert("1.0", f"{lista_de_dados.get(sequencia[indice])}")  # Insere o novo conteúdo
            indice+=1

        # Inserindo dados na caixa de aplicação e nome que é feita fora do looping
        self.entrada_nome.delete("1.0", "end")
        self.bloco_texto_aplicacao.delete("1.0", "end")
        self.entrada_nome.insert("1.0", f"{lista_de_dados.get('nome')}")
        self.bloco_texto_aplicacao.insert("1.0", f"{lista_de_dados.get('aplicacao')}")

    # Função para ler o código do produto na interface
    # Ela também informa caso o usuário não escreva um código
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
        return retorno

    def mostrar_imagem(self, codigo_produto):
        if codigo_produto:
            imagem = ImagemProduto(codigo_produto)
            imagem.mostrar_imagem(self.root)
        return None

    def fechar_aba_tkinter(self):
        root.destroy()
    
    def esconder_janela(self):
        root.withdraw()

    def restaurar_janela(self):
        root.deiconify()



    def interface_via_exel(self):

        self.fechar_aba_tkinter()
            

        root_exel = tk.Tk()
        root_exel.title("Via Exel")
        root_exel.geometry('450x300')
        self.entrada_caminho_pasta = tk.Entry(root_exel, width=35)
        self.entrada_caminho_pasta.place(x=15, y=50)
        self.botao_selecionar_arquivo = tk.Button(root_exel, text="Selecionar", width=10, command=lambda: selecionar_pasta_e_inserir())
        self.botao_selecionar_arquivo.place(x=280, y=50)

        def selecionar_pasta_e_inserir():
            pasta = filedialog.askopenfile()
            print('Essa é o valor que vai atribuir para a variável "PASTA"')
            print(pasta.name)
            self.entrada_caminho_pasta.insert(0, pasta.name)

        root.mainloop()

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




