
# from pyray import *
# init_window(800, 450, "Hello")
# while not window_should_close():
#     begin_drawing()
#     clear_background(WHITE)
#     draw_text("Hello world", 190, 200, 20, VIOLET)
#     end_drawing()
# close_window()
import tkinter as tk

# Função para exibir uma mensagem quando o botão for clicado
def exibir_mensagem():
  print("O botão foi clicado!")

# Criar uma janela
janela = tk.Tk()
janela.title("Botão Simples")

# Adicionar um botão
botao = tk.Button(janela, text="Clique Aqui", command=exibir_mensagem)
botao.pack()

# Executar o loop principal
janela.mainloop()
