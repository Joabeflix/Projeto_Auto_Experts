from app import TokenGerador, APICliente, JSONFilter
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

class interface():
    def __init__(self, root):
        self.root = root

        self.texto = ttk.Label(root, text="Código").place(x=3, y=3)

        self.bloco_texto1 = ttk.Text(root, height=3, width=30)
        self.bloco_texto1.place(x=10, y=30)

        self.bloco_texto2 = ttk.Text(root, height=3, width=30)
        self.bloco_texto2.place(x=10, y=90)

        self.entrada_teste = ttk.Entry(root, width=30)
        self.entrada_teste.place(x=3, y=160)

        self.botao_inserir = ttk.Button(root, text="Inserir", command=lambda: self.inserir_texto(self.buascar_conteudo(self.ler_codigo_produto())))
        self.botao_inserir.place(x=3, y=200)

        self.botao_remover = ttk.Button(root, text="Remover", command=self.remover_texto)
        self.botao_remover.place(x=70, y=200)

    def inserir_texto(self, dados):
        if dados:
            marca = dados[0]
            aplicacao = dados[1]
            self.bloco_texto1.insert(tk.END, marca)
            self.bloco_texto2.insert(tk.END, aplicacao)

    def remover_texto(self):
        self.bloco_texto1.delete(1.0, tk.END)
        self.bloco_texto2.delete(1.0, tk.END)

    def ler_codigo_produto(self):
        
        codigo_produto = self.entrada_teste.get()
        if codigo_produto:
            return codigo_produto
        messagebox.showwarning("Erro", "Você não digitou um código.")
        return None
    
    def buascar_conteudo(self, codigo_produto):
        if codigo_produto:
            token_manager = TokenGerador()
            api_cliente = APICliente(token_manager)
            filtro = JSONFilter()
            response = api_cliente.obter_dados(codigo_produto)

            if response:
                data = response.json()
                marca = filtro.filtrar_dados(data, "['data'][0]['marca']['nome']")
                aplicacao = filtro.filtrar_dados(data, "['data'][0]['aplicacoes'][0]['descricaoFrota']")
                peso = filtro.filtrar_dados(data, "['data'][0]['especificacoes']", "Peso bruto")
                return [marca, aplicacao]
        return None
   

# Inicializa a interface gráfica e executa o loop principal do Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    meu_app = interface(root)
    root.title('Dados Produtos')
    root.geometry('256x300')
    root.mainloop()
