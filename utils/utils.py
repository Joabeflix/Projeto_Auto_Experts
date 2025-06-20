import json
import numpy as np
import os
from tkinter import messagebox
import re
from utils.mapeamento_palavras_substituir import MAPEAMENTO_SUBSTITUICOES_NOME_ANUNCIOS
import time

def texto_no_console(obj):
    separadores = ['_', '*', '-', '#']
    if obj in separadores:
        print(obj * 120)
        return None
    if isinstance(obj, list):
        for t in obj:
            if t == '\n':
                print('\n')
                continue
            print(f'>>> {t}{'\n'}')
        return None
    print(f'>>> {obj}{'\n'}')


def alterar_valor_json(caminho_json, chave, novo_valor):
    with open(file=caminho_json, mode='r', encoding='utf8') as arquivo:
        dados = json.load(arquivo)
    dados[chave] = novo_valor
    with open(file=caminho_json, mode='w', encoding='utf8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

import json

def pegar_valor_json_arquivo(caminho_arquivo, chave, padrao=None):
    """
    Lê um arquivo JSON e retorna o valor da chave fornecida.

    Parâmetros:
        caminho_arquivo (str): Caminho para o arquivo JSON.
        chave (str): Chave a ser buscada.
        padrao: Valor padrão caso a chave não seja encontrada.

    Retorna:
        Valor correspondente à chave, ou valor padrão se não encontrado.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            texto_no_console('Lendo o arquivo json')
        texto_no_console(f'retorno === {dados.get(chave, padrao)}')
        return dados.get(chave, padrao)
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON: '{caminho_arquivo}'")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    return padrao


def tela_aviso(titulo, mensagem, tipo):

    tipos = {
        "informacao": messagebox.showinfo,
        "erro": messagebox.showerror
    }
    if tipo in tipos.keys():
        return tipos.get(tipo)(title=titulo, message=mensagem)
    texto_no_console([
        f'Tipo de tela não cadastrado na função: {tipo}', 
        f'Tipos cadastrados: {list(tipos.keys())}'])

def converter_int64_para_int(obj):
    """ Se não for int64 ele retorna o valor original."""
    if isinstance(obj, np.int64):
        return int(obj)
    return obj

def limpar_prompt():
    os.system('cls')



def deixar_nome_ate_60_caracteres(nome_produto, codigo_produto, marca):

    palavras_para_substituir = MAPEAMENTO_SUBSTITUICOES_NOME_ANUNCIOS

    def acertar_nomes(x):
        return str(x).upper().replace("  ", " ")
    
    def verificar_tamanho(nome):
        return True if len(nome) < 61 else False
    
    def retorno_final(x):
        return x.title().rstrip().replace("///", "").replace("//", "").replace("   ", " ").replace("  ", " ")
    
    nome_produto = acertar_nomes(nome_produto)
    codigo_produto = acertar_nomes(codigo_produto)
    marca = acertar_nomes(marca)
    
    nome_novo = nome_produto.replace("  ", " ")

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    
    nome_novo = nome_novo.replace(codigo_produto, "")
    nome_novo = nome_novo.replace("  ", " ")

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    
    nome_novo = nome_novo.replace(marca, "")
    nome_novo = nome_novo.replace("  ", " ")

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    
    for palavra in palavras_para_substituir:
        if palavra not in nome_novo:
            continue
        if verificar_tamanho(nome_novo):
            return retorno_final(nome_novo)
        nome_novo = nome_novo.replace(palavra, palavras_para_substituir.get(palavra))

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    

    def remover_conteudo_parenteses(texto):
        """
        Função para remover dados que temos entre parentezes dos nomes... ex: 
        "Amortecedor De Suspensão Compatível Puma 7900 (Serie 10 / X10) 1981-2005 Diant / Tras"
        vira:
        "Amortecedor De Suspensão Compatível Puma 7900 981-2005 Diant / Tras"
        """
        return re.sub(r"\([^)]*\)", "", texto)

    nome_novo = remover_conteudo_parenteses(nome_novo)

    return retorno_final(nome_novo)


def medir_tempo_execucao(funcao):
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        fim = time.perf_counter()
        texto_no_console(f"Tempo de demorado: {fim - inicio:.2f} segundos:")
        return resultado
    return wrapper

        

if __name__ == "__main__":
    @medir_tempo_execucao
    def minha_funcao():
        time.sleep(2)
        print("Função finalizada.")

    minha_funcao()
    

