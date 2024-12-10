import tkinter as tk
from tkinter import ttk

# Configuração da janela principal
root = tk.Tk()
root.geometry("600x290")  # Tamanho da janela

# Lista para armazenar as referências dos widgets Text
blocos_texto = []

# Posição inicial
y_inicial = 30

dados = {
    'nome': 'SERVO FREIO CONTROIL - C-5682', 
    'marca': 'CONTROIL', 
    'aplicacao': 'PEUGEOT 2008 1.0 12V/1.6 16V 2015-2024',
    'ean': '7893049568296', 
    'ncm': '87083090', 
    'peso': '2,996'
    }

# Criar os widgets Text dinamicamente
for x in range(5):
    bloco_texto = tk.Text(root, height=1, width=25)
    bloco_texto.place(x=20, y=y_inicial)
    blocos_texto.append(bloco_texto)  # Armazena a referência na lista
    y_inicial += 40

bloco_texto_aplicacao = tk.Text(root, height=11, width=40)
bloco_texto_aplicacao.place(x=250, y=30)

# Função para inserir dados nos blocos
def inserir_dados(lista_de_dados={}):
    indice = 0
    sequencia = ['nome', 'marca', 'aplicacao', 'ean', 'ncm', 'peso']
    for i, bloco in enumerate(blocos_texto):
        bloco.delete("1.0", "end")  # Limpa o conteúdo existente
        bloco.insert("1.0", f"{lista_de_dados.get(sequencia[indice])}")  # Insere o novo conteúdo
        indice+=1

# Botão para inserir dados nos blocos
btn_inserir = ttk.Button(root, text="Inserir Dados", command=lambda: inserir_dados(dados))
btn_inserir.place(x=20, y=y_inicial + 10)

# Botão para exibir os dados (opcional, apenas para teste)
def obter_dados():
    for i, bloco in enumerate(blocos_texto):
        texto = bloco.get("1.0", "end").strip()
        print(f"Bloco {i}: {texto}")

btn_exibir = ttk.Button(root, text="Exibir Dados", command=obter_dados)
btn_exibir.place(x=120, y=y_inicial + 10)

root.mainloop()
