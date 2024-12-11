import tkinter as tk
from tkinter import ttk
from app import puxar_dados_api

# Configuração da janela principal
root = tk.Tk()
root.geometry("600x290")  # Tamanho da janela

# Lista para armazenar as referências dos widgets Text
blocos_texto = []



dados_api = puxar_dados_api('AC 30726', dados_necessarios=['nome', 'marca', 'aplicacao', 'ean', 'ncm', 'peso'])

# Posição inicial
y_inicial_caixas = 30
y_inicial_label = 9

# Criar os widgets Text dinamicamente
nomes_labels = ['Nome', 'Marca', 'Ean', 'NCM', 'Peso']
for x in range(5):
    tk.Label(text=nomes_labels[x]).place(x=18, y=y_inicial_label)
    bloco_texto = tk.Text(root, height=1, width=25)
    bloco_texto.place(x=20, y=y_inicial_caixas)
    blocos_texto.append(bloco_texto)  # Armazena a referência na lista
    y_inicial_caixas += 40
    y_inicial_label+=41

bloco_texto_aplicacao = tk.Text(root, height=11, width=40)
bloco_texto_aplicacao.place(x=250, y=30)

# Função para inserir dados nos blocos
def inserir_dados(lista_de_dados={}):
    indice = 0
    sequencia = ['nome', 'marca', 'ean', 'ncm', 'peso']

    # Inserindo dados nas linhas
    for i, bloco in enumerate(blocos_texto):
        bloco.delete("1.0", "end")  # Limpa o conteúdo existente
        bloco.insert("1.0", f"{lista_de_dados.get(sequencia[indice])}")  # Insere o novo conteúdo
        indice+=1
    
    # Inserindo dados na caixa de aplicação que é feita fora do looping
    bloco_texto_aplicacao.insert("1.0", f"{lista_de_dados.get('aplicacao')}")

# Botão para inserir dados nos blocos
btn_inserir = ttk.Button(root, text="Inserir Dados", command=lambda: inserir_dados(dados_api))
btn_inserir.place(x=20, y=y_inicial_caixas + 10)

# Botão para exibir os dados (opcional, apenas para teste)
def obter_dados():
    for i, bloco in enumerate(blocos_texto):
        texto = bloco.get("1.0", "end").strip()
        print(f"Bloco {i}: {texto}")

btn_exibir = ttk.Button(root, text="Exibir Dados", command=obter_dados)
btn_exibir.place(x=120, y=y_inicial_caixas + 10)

root.mainloop()
