import tkinter as tk
from PIL import Image, ImageTk

# Criação da janela principal
root = tk.Tk()
root.title("Renderizar Imagem com Tkinter")

# Carregar a imagem com Pillow
image_path = "imagem.jpg"  # Substitua pelo caminho da sua imagem
img = Image.open(image_path)

# Redimensionar a imagem (opcional)
# img = img.resize((300, 300))  # Ajuste a largura e altura conforme necessário

# Converter a imagem para um formato compatível com o Tkinter
tk_image = ImageTk.PhotoImage(img)

# Criar um widget Label para exibir a imagem
label = tk.Label(root, image=tk_image)
label.pack()

# Iniciar o loop principal do Tkinter
root.mainloop()
