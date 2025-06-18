import tkinter as tk
from models_excel.core import teste



root = tk.Tk()
root.geometry('500x500')

botao = tk.Button(text='TESTE', command=lambda: teste())
botao.place(x=10, y=10)

label = tk.Label(text='OIIIIII').place(x=50, y=50)


root.mainloop()





