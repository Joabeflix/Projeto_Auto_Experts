import pandas as pd
from utils.utils import texto_no_console, deixar_nome_ate_60_caracteres, tela_aviso, medir_tempo_execucao
from models_api.api_max import puxar_dados_produto_api, puxar_dados_veiculos_api
from models_api.gerar_token import TokenGerador
import requests
import re
from models_excel.padroes_substituir_nomes_anuncios import  PADROES

class Gerar_Anuncios:
    def __init__(self, acces_token, planilha, atualizar_barra_geral, atualizar_barra_anuncio, baixar_img=True):
        self.acces_token=acces_token
        self.planilha=planilha
        self.baixar_img=baixar_img
        self.atualizar_barra_geral=atualizar_barra_geral
        self.atualizar_barra_anuncio=atualizar_barra_anuncio
    

    def extrair_primeira_data(self, veiculo):
        match = re.search(r'\b(19|20)\d{2}-(19|20)\d{2}\b', veiculo)
        if match:
            return veiculo[:match.end()]  # Retorna até o fim da data encontrada
        return veiculo  # Se não achar, retorna o texto original

    @medir_tempo_execucao
    def gerar_planilha(self):
        self.atualizar_barra_geral(0)
        planilha = pd.read_excel(self.planilha)
        coluna_codigo = planilha['Cod Produto']
        qtd_produtos = len(coluna_codigo)
        texto_no_console(f'Total de produtos para criar anúncio: {qtd_produtos}')

        # Colunas de saída
        coluna_nome_anuncio = []
        coluna_ean = []
        coluna_nome_ate_60 = []
        coluna_descricao_completa = []
        coluna_descricao_simplificada = []
        coluna_posicao = []
        coluna_lado = []
        
        # NEWS
        coluna_ncm = []
        coluna_garantia = []
        
        coluna_peso = []
        coluna_altura_embalagem = []
        coluna_largura_embalagem = []
        coluna_comprimento_embalagem = []

        coluna_qtd_por_embalagem = []
        


        dados_puxar = [
            'nome', 'grupo_produto', 'aplicacao', 'marca',
            'part_number', 'ean', 'posicao', 'lado', 
            'imagem_url', 'veiculos', 'ncm', 'garantia',
            'peso', 'altura_embalagem', 'largura_embalagem',
            'comprimento_embalagem', 'qtd_embalagem', 'similares'
        ]

        qtd_feita = 1
        for cod in coluna_codigo:
            dados_anuncio = puxar_dados_produto_api(self.acces_token, codigo_produto=cod, dados_necessarios=dados_puxar)
            if not dados_anuncio:
                for coluna in [coluna_nome_anuncio, coluna_ean, coluna_nome_ate_60, coluna_descricao_completa, coluna_posicao, coluna_lado]:
                    coluna.append('Não encontrado API')
                qtd_feita += 1
                continue

            nome_produto_api = dados_anuncio['grupo_produto']
            nome_produto = self.verificar_e_substituir_nome_padrao(nome_produto_api)

            veiculo_titulo = dados_anuncio['aplicacao']
            posicao = dados_anuncio['posicao']
            lado = dados_anuncio['lado']
            marca = dados_anuncio['marca']
            codigo_produto = dados_anuncio['part_number']
      
            _nome_anuncio = f'{nome_produto} Compatível {self.extrair_primeira_data(veiculo_titulo)} {posicao} {lado} {marca} {codigo_produto}'.title()
            nome_anuncio = " ".join(_nome_anuncio.replace('None', ' ').split()).title()

            nome_ate_60 = deixar_nome_ate_60_caracteres(nome_anuncio, codigo_produto, marca)
            texto_no_console(f'Cód: {cod} - Nome gerado: {nome_ate_60}')

            coluna_nome_anuncio.append(nome_anuncio)
            coluna_ean.append(dados_anuncio['ean'])
            coluna_nome_ate_60.append(nome_ate_60)
            coluna_posicao.append(posicao)
            coluna_lado.append(lado)
            coluna_ncm.append(dados_anuncio['ncm'])
            coluna_garantia.append(dados_anuncio['garantia'])
            coluna_peso.append(dados_anuncio['peso'])
            coluna_altura_embalagem.append(dados_anuncio['altura_embalagem'])
            coluna_largura_embalagem.append(dados_anuncio['largura_embalagem'])
            coluna_comprimento_embalagem.append(dados_anuncio['comprimento_embalagem'])
            coluna_qtd_por_embalagem.append(dados_anuncio['qtd_embalagem'])

            def gerar_aplicacao_veiculo():
                texto_no_console(f'Gerando aplicação do código {dados_anuncio["part_number"]}')
                
                
                # Na lista de veículos crua temos a data inicial de aplicação e a data final
                # No entando não temos o veículo... temos somente o código do veículo.
                # Então para pegar o veículo exato, chamanos outra função na API e retornamos os veículos
                lista_de_veiculos_crua = dados_anuncio['veiculos']
                
                lista_veiculos_api = puxar_dados_veiculos_api(
                    access_token=self.acces_token,
                    lista_veiculos=lista_de_veiculos_crua,
                    atualizar_barra_anuncio=self.atualizar_barra_anuncio
                )
                parte_de_cima_aplicacao = f"Produto: {dados_anuncio['nome']}\nMarca: {dados_anuncio['marca']}\nCódigo Produto: {dados_anuncio['part_number']}\n\nCompatível com os veículos:\n"
                linhas_aplicacao = []
                for veiculo, ano_aplicacao in zip(lista_veiculos_api, lista_de_veiculos_crua):
                    try:
                        marca = veiculo.get('marca', '')
                        nome = veiculo.get('nome', '')
                        modelo = veiculo.get('modelo', '')
                        motorizacao = veiculo.get('motorizacao', {})
                        motor_nome = motorizacao.get('nome', '')
                        cilindrada = motorizacao.get('cilindrada', '')
                        configuracao = motorizacao.get('configuracao', '')
                        potencia = motorizacao.get('potenciaCv', '')
                        anos = f"{ano_aplicacao['anoInicial']}-{ano_aplicacao['anoFinal']}"
                        linha = f"{marca} {nome} {modelo} {anos} - Motor: {motor_nome} {cilindrada}cc {configuracao} {potencia}cv"
                        linhas_aplicacao.append(linha.strip())

                    except Exception as e:
                        texto_no_console(f"Erro ao montar aplicação para veículo: {e}")
                
                lista_similares = []
                for item in dados_anuncio['similares']:
                    try:
                        lista_similares.append(f"{item['marca']['nome']}: {item['partNumber']}")
                    except Exception as e:
                        texto_no_console(f"Erro ao montar os similares: {e}")
                        
                        
                        
                texto_no_console('Aplicação montada com sucesso!')
                
                
                linhas_similares = f"\n\nCódigos similares:\n{"\n".join(lista_similares)}" if lista_similares else ''
                return f'{parte_de_cima_aplicacao}{"\n".join(linhas_aplicacao)}{linhas_similares}'

            aplicacao_completa = gerar_aplicacao_veiculo()
            aplicacao_simplificada = f"Produto: {dados_anuncio['nome']}\nMarca: {marca}\nCódigo Produto: {codigo_produto}\n\nCompatível com os veículos:{veiculo_titulo}"
            coluna_descricao_completa.append(aplicacao_completa)
            coluna_descricao_simplificada.append(aplicacao_simplificada)

            try:
                if self.baixar_img:
                    self.baixar_imagem(url=dados_anuncio['imagem_url'], nome_arquivo=codigo_produto)
            except:
                pass

            texto_no_console(f'Feito: {qtd_feita}/{qtd_produtos}')
            texto_no_console('-')

            if self.atualizar_barra_geral:
                progresso = int((qtd_feita / qtd_produtos) * 100)
                self.atualizar_barra_geral(progresso)

            qtd_feita += 1
            

        planilha['nome anuncio completo'] = coluna_nome_anuncio
        planilha['nome anuncio < 60'] = coluna_nome_ate_60
        planilha['ean'] = coluna_ean
        planilha['aplicacao completa'] = coluna_descricao_completa
        planilha['aplicacao simplificada'] = coluna_descricao_simplificada
        planilha['posicao'] = ["" if x == 'None' else x for x in coluna_posicao]
        planilha['lado'] = ["" if x == 'None' else x for x in coluna_lado]
        planilha['ncm'] = coluna_ncm
        planilha['garantia'] = coluna_garantia
        planilha['peso'] = coluna_peso
        planilha['altura embalagem'] = coluna_altura_embalagem
        planilha['largura embalagem'] = coluna_largura_embalagem
        planilha['comprimento embalagem'] = coluna_comprimento_embalagem
        planilha['qtd por embalagem'] = coluna_qtd_por_embalagem

        planilha.to_excel('anuncios.xlsx', index=False)
        texto_no_console('Planilha de anúncios gerada com sucesso!')
        

    def baixar_imagem(self, url, nome_arquivo):
        texto_no_console(f'Baixando imagem {nome_arquivo}.')
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                with open(f'{nome_arquivo}.jpg', 'wb') as f:
                    f.write(resposta.content)
                texto_no_console(f"Imagem salva como: {nome_arquivo}")
            else:
                texto_no_console(f"Erro ao baixar imagem. Código HTTP: {resposta.status_code}")
        except Exception as e:
            texto_no_console(f"Código: {nome_arquivo} --> provavelmente não tem imagem disponível na API.")


    def verificar_e_substituir_nome_padrao(self, nome_padrao):
        nome_padrao = str(nome_padrao).lower()
        # Se o nome padão nao tiver no dicionario o .get ja retorna o nome padrao passado no input
        # Por isso passamos nome_padrao 2 vezes no argumento, por q o outro é o retorno quando não existe a chave
        return PADROES.get(nome_padrao, nome_padrao)

def teste():
    texto_no_console('teste teste ')


if __name__ == "__main__":
    acces_token = TokenGerador().ler_token()
    app = Gerar_Anuncios(
        acces_token=acces_token,
        planilha='plan.xlsx')
    
    app.gerar_planilha()
    

# puxar_dados_api(access_token=acces_token, codigo_produto=codigo_produuto, dados_necessarios=dados)


