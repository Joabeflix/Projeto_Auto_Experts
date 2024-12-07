from app import exec
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk

class interface():
    def __init__(self, root):
        self.root = root

        self.texto = ttk.Label(root, text="Código do produto").place(x=193, y=4)

        self.bloco_texto = ttk.Text(root, height=25, width=65)
        self.bloco_texto.place(x=48, y=125)

        self.entrada_codigo = ttk.Entry(root, width=30)
        self.entrada_codigo.place(x=150, y=30)

        self.botao_inserir = ttk.Button(root, text="Pesquisar", width=9, command=lambda: self.inserir_texto(self.buscar_conteudo(self.ler_codigo_produto())))
        self.botao_inserir.place(x=162, y=70)

        self.botao_remover = ttk.Button(root, text="Limpar", width=9, command=self.remover_texto)
        self.botao_remover.place(x=253, y=70)

    def inserir_texto(self, dados):
        self.remover_texto('bloco_texto')
        linha = "-" * 78
        if dados:
            texto = f'Produto: {dados[0]}\n{linha}\nMarca: {dados[1]}\n{linha}\nAplicação: \n{dados[2]}\n{linha}\nPeso: {dados[3]}'
            self.bloco_texto.insert(tk.END, texto)

    def remover_texto(self, texto_remover=None):

        if texto_remover:
            self.bloco_texto.delete(1.0, tk.END)
            return None
        
        self.bloco_texto.delete(1.0, tk.END)
        self.entrada_codigo.delete(0, tk.END)

    def ler_codigo_produto(self):
        
        codigo_produto = self.entrada_codigo.get()
        if codigo_produto:
            return codigo_produto
        messagebox.showwarning("Erro", "Você não digitou um código.")
        return None
    
    def buscar_conteudo(self, codigo_produto):
        retorno = exec(codigo_produto, ['nome', 'marca', 'aplicacao', 'peso'])
        return list(retorno.values())
   

# Inicializa a interface gráfica e executa o loop principal do Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    meu_app = interface(root)
    root.title('Catálogo AutoExperts')
    root.geometry('500x555')
    root.minsize(width=500, height=555)
    root.maxsize(width=500, height=555)
    root.mainloop()
