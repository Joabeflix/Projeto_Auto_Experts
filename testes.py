from app import exec


x = exec('C-3473', ['nome', 'ean', 'peso'])

nome = x.get('nome')

print(nome)

