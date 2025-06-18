def mapeamento_usar(chave):
    mapeamentos = {
        'nome': {
            'caminho': "['data'][0]['aplicacoes'][0]['descricao']",
            'chave_secundaria': None
        },
        'marca': {
            'caminho': "['data'][0]['marca']['nome']",
            'chave_secundaria': None
        },
        'aplicacao': {
            'caminho': "['data'][0]['aplicacoes'][0]['descricaoFrota']",
            'chave_secundaria': None
        },
        'ean': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Código de barras (EAN)"
        },
        'ncm': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "NCM"
        },
        'peso': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Peso bruto"
        },
        'imagem_url': {
            'caminho': "['data'][0]['imagens'][0]['url']",
            'chave_secundaria': None
        },
        'json_completo': {
            'caminho': "['data']",
            'chave_secundaria': None
        },
        'garantia': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Prazo de garantia"
        },
        'inclui_bucha': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Inclui bucha"
        },
        'inclui_pivo': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Inclui pivô"
        },
        'posicao': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Posição"
        },
        'lado': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Lado"
        },
        'altura_embalagem': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Altura da embalagem"
        },
        'largura_embalagem': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Largura da embalagem"
        },
        'comprimento_embalagem': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Comprimento da embalagem"
        },
        'qtd_embalagem': {
            'caminho': "['data'][0]['especificacoes']",
            'chave_secundaria': "Quantidade de peças por embalagem"
        },
        'part_number': {
            'caminho': "['data'][0]['partNumber']",
            'chave_secundaria': None
        },
        'data_cadastro': {
            'caminho': "['data'][0]['dataCadastro']",
            'chave_secundaria': None
        },
        'data_atualizacao': {
            'caminho': "['data'][0]['dataAtualizacao']",
            'chave_secundaria': None
        },
        'similares': {
            'caminho': "['data'][0]['similares']",
            'chave_secundaria': None
        },
        'grupo_produto': {
            'caminho': "['data'][0]['aplicacoes'][0]['grupoProduto']['nome']",
            'chave_secundaria': None
        },
        'mercado': {
            'caminho': "['data'][0]['aplicacoes'][0]['mercado']['nome']",
            'chave_secundaria': None
        },
        'veiculos': {
            'caminho': "['data'][0]['aplicacoes'][0]['veiculos']",
            'chave_secundaria': None
        },
        'status': {
            'caminho': "['data'][0]['status']",
            'chave_secundaria': None
        },
        'ativo_catalogo': {
            'caminho': "['data'][0]['ativoCatalogo']",
            'chave_secundaria': None
        }
    }

    if chave in mapeamentos:
        return mapeamentos[chave]
    return False


if __name__ == "__main__":
    print(mapeamento_usar('peso'))

