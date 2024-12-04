from app import TokenGerador, APICliente, JSONFilter

token_manager = TokenGerador()
api_cliente = APICliente(token_manager)
filtro = JSONFilter()

cod_porduto_teste = input("Digite o código que deseja pesquisar: ").replace('  ', '')
response = api_cliente.obter_dados(cod_porduto_teste)

if response:
    data = response.json()
    marca = filtro.filtrar_dados(data, "['data'][0]['marca']['nome']")
    aplicacao = filtro.filtrar_dados(data, "['data'][0]['aplicacoes'][0]['descricaoFrota']")
    peso = filtro.filtrar_dados(data, "['data'][0]['especificacoes']", "Peso bruto")


