from tkinter import *

root = Tk()

root.geometry("500x400+100+100")
root.title("Qualquer coisa só para não ficar em branco")
root.configure(background= '#188961')
root.resizable(True,True)

frame1 = Frame(root)
frame1.pack(side=TOP, ipadx=200, ipady=100, padx=10, pady=10)
frame2 = Frame(root)
frame2.pack(side=BOTTOM, ipadx=200, ipady=200, padx=10, pady=10)
label1 = Label(frame1, text='Label1')
label1.pack()
label2 = Label(frame2, text='Label2')
label2.pack()


root.mainloop()