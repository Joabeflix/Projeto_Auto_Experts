import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
from utils.utils import texto_no_console, tela_aviso
from tkinter.scrolledtext import ScrolledText
import sys
from models_excel.core import Gerar_Anuncios
from models_api.api_max import puxar_dados_produto_api
from models_api.gerar_token import TokenGerador
import threading
import time

class RedirecionarConsole:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.update_idletasks()  # Atualiza a interface imediatamente

    def flush(self):
        pass

class MinhaInterface:
    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("Interface -- XWP")
        self.root.geometry("913x950")

        """ Entrys """
        self.entrada_planilha = ttk.Entry(self.root, width=45)
        self.entrada_planilha.place(x=10, y=60)

        """ CheckButtons"""
        self.baixar_imagem = tk.BooleanVar(value=True)
        self.escolher_baixar_imagem = ttk.Checkbutton(self.root, variable=self.baixar_imagem, text='baixar imagens',  style='square-toggle')
        self.escolher_baixar_imagem.place(x=572, y=66)

        """ Labels """
        self.label_console = ttk.Label(self.root, text="Informações:", font=("Segoe UI", 17, "bold"), foreground="blue")
        self.label_console.place(x=10, y=107)



        """ Buttons """
        self.botao_selecionar_excel = ttk.Button(self.root, text='Selecionar Excel', command=self.selecionar_arquivos_excel, style='success-outline')
        self.botao_selecionar_excel.place(x=10, y=10)
        self.botao_gerar_planilha = ttk.Button(self.root, text='Gerar', style='success', command=lambda: self.gerar_anuncios_thread())
        self.botao_gerar_planilha.place(x=485, y=60)




        """ Outros """

        self.console = ScrolledText(self.root, width=85, height=30, wrap=tk.WORD)
        self.console.place(x=10, y=165)
        sys.stdout = RedirecionarConsole(self.console)


    def selecionar_arquivos_excel(self):
        arquivo = askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
        if arquivo:
            texto_no_console(f'Arquivo selecionado com sucesso: {arquivo}\n')
            self.entrada_planilha.delete(0, tk.END)
            self.entrada_planilha.insert(0, arquivo)
        else:

            texto_no_console('Nenhum arquivo selecionado.\n')

    def gerar_anuncios_thread(self):
        texto_no_console('Iniciando...')
        threading.Thread(target=self._gerar_anuncios, daemon=True).start()

    def _gerar_anuncios(self):
        token_de_acesso = TokenGerador().ler_token()
        local_planilha = self.entrada_planilha.get()
        if local_planilha:
            app = Gerar_Anuncios(acces_token=token_de_acesso, baixar_img=self.baixar_imagem.get(), planilha=local_planilha)
            app.gerar_planilha()
            return None
        tela_aviso('erro', 'Você precisa selecionar uma planilha!!!!', 'erro')

    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MinhaInterface()
    app.iniciar()
