from Modulos import *
import tkinter as tk

root = Tk()


root.resizable(True, True)

frame1 = Frame(root)
frame2 = Frame(root)
label1 = Label(frame1, text= "label1")
label2 = Label(frame2, text= "label2")

frame1.grid(column=0, row=1, columnspan= 1, ipadx= 50,ipady=50, padx=10, pady=10)
frame2.grid(column=0, row=1, columnspan= 1, ipadx= 50,ipady=50, padx=10, pady=10)

root.mainloop()