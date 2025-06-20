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
        self.text_widget.update_idletasks()

    def flush(self):
        pass

class MinhaInterface:
    def __init__(self):
        self.root = ttk.Window(themename="vapor")
        self.root.title("Criar Anúncios AutoExperts")
        self.root.geometry("1057x493")

        """ Entrys """
        self.entrada_planilha = ttk.Entry(self.root, width=45, style='secondary')
        self.entrada_planilha.place(x=10, y=10)

        """ CheckButtons"""
        self.baixar_imagem = tk.BooleanVar(value=True)
        def printar_status_escolher_imagem():
            if self.baixar_imagem.get():
                texto_no_console('Baixar imagens (ATIVADO).')
            else:
                texto_no_console('Baixar imagens (DESATIVADO).')

        self.escolher_baixar_imagem = ttk.Checkbutton(
            self.root,
            variable=self.baixar_imagem,
            text='baixar imagens',
            style='square-toggle',
            command=printar_status_escolher_imagem
        )
        self.escolher_baixar_imagem.place(x=530, y=16)

        """ Labels """
        self.label_console = ttk.Label(self.root, text="Informações:", font=("Segoe UI", 17, "bold"), foreground="white")
        self.label_console.place(x=10, y=42)

        """ Buttons """
        self.botao_selecionar_excel = ttk.Button(
            self.root,
            text='Selecionar Excel',
            command=self.selecionar_arquivos_excel,
            style='light-outline'
        )
        self.botao_selecionar_excel.place(x=303, y=10)

        self.botao_gerar_planilha = ttk.Button(
            self.root,
            text='Criar Anúncios',
            style='success-outline',
            command=lambda: self.gerar_anuncios_thread()
        )
        self.botao_gerar_planilha.place(x=419, y=10)

        """ Medidor de Progresso (NOVO) """
        self.meter_geral = ttk.Meter(
            self.root,
            metersize=160,
            padding=5,
            amountused=0,
            metertype="semi",
            subtext="Progresso Total",
            interactive=False,
            bootstyle="success",
            stripethickness=3
        )
        self.meter_geral.place(x=850, y=109)  # posição no canto superior direito


        """ Medidor de Progresso (NOVO) """
        self.meter_anuncio = ttk.Meter(
            self.root,
            metersize=160,
            padding=5,
            amountused=0,
            metertype="semi",
            subtext="Progresso Anúncio",
            interactive=False,
            bootstyle="secondary",
            stripethickness=3
        )
        self.meter_anuncio.place(x=850, y=275)  # posição no canto superior direito

        """ Console """
        self.console = ScrolledText(self.root, width=85, height=20, wrap=tk.WORD, font=("Arial", 12))
        self.console.place(x=10, y=84)
        sys.stdout = RedirecionarConsole(self.console)

    def atualizar_progresso_geral(self, valor):
        """ Atualiza o medidor com o valor (0 a 100) """
        self.meter_geral.configure(amountused=valor)
        self.root.update_idletasks()

    def atualizar_progresso_anuncio_atual(self, valor):
        """ Atualiza o medidor com o valor (0 a 100) """
        self.meter_anuncio.configure(amountused=valor)
        self.root.update_idletasks()

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
            app = Gerar_Anuncios(
                acces_token=token_de_acesso,
                baixar_img=self.baixar_imagem.get(),
                planilha=local_planilha,
                atualizar_barra_geral=self.atualizar_progresso_geral,
                atualizar_barra_anuncio=self.atualizar_progresso_anuncio_atual
                  # Passa função para uso interno
            )
            app.gerar_planilha()
            self.atualizar_progresso_geral(100)  # Garante que termina em 100%
            self.atualizar_progresso_anuncio_atual(100)
        else:
            tela_aviso('erro', 'Você precisa selecionar uma planilha!!!!', 'erro')

    def iniciar(self):
        self.root.mainloop()
        texto_no_console('Programa iniciado com sucesso.')

if __name__ == "__main__":
    app = MinhaInterface()
    app.iniciar()
