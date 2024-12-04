import os

os.system('cls')
caminho_atual = rf'venv'
novo_caminho = rf'venv_backup'

if os.path.exists(caminho_atual):
    os.rename(caminho_atual, novo_caminho)
    print(f"Pasta renomeada para: {novo_caminho}")
else:
    pass

os.system('python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt')
os.system('python.exe -m pip install --upgrade pip')
os.system('pip list')
