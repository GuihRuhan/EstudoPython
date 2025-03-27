from tkinter import *
import tkinter as tk

# Função para atualizar o texto do rótulo
def atualizar_texto():
    texto = entrada.get()  # Obtém o texto digitado na entrada
    rotulo.config(text=f"Você digitou: {texto}")

# Cria a janela principal
janela = tk()
janela.title("Exemplo de Interface com Tkinter")
janela.geometry("300x200")  # Define o tamanho da janela

# Cria um rótulo
rotulo = tk.Label(janela, text="Digite algo abaixo:", font=("Arial", 12))
rotulo.pack(pady=10)  # Adiciona o rótulo com espaçamento vertical

# Cria uma entrada de texto
entrada = tk.Entry(janela, font=("Arial", 12))
entrada.pack(pady=10)

# Cria um botão
botao = tk.Button(janela, text="Atualizar", command=atualizar_texto, font=("Arial", 12))
botao.pack(pady=10)

# Inicia o loop principal da interface
janela.mainloop()
