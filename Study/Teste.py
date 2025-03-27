from tkinter import *
import tkinter as tk
import sqlite3
from tkinter import ttk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image 

import webbrowser
from PIL import ImageTk, Image


root = tk.Tk()

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    
    def geraRelatCliente(self):
        self.c = canvas.Canvas('cliente.pdf')
        self.codigoRel = self.codigo_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.foneRel = self.fone_entry.get()
        self.cidadeRel = self.cidade_entry.get()
        
        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')
        
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, ' Código: ')
        self.c.drawString(50, 670, ' Nome: ')
        self.c.drawString(50, 630, ' Telefone: ')
        self.c.drawString(50, 600, ' Cidade: ')
        
        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(150, 700, self.codigoRel)
        self.c.drawString(150, 670, self.nomeRel)
        self.c.drawString(150, 630, self.foneRel)
        self.c.drawString(150, 600, self.cidadeRel)
        
        self.c.rect(20,550,550, 3, fill=True, stroke=False)
        
        self.c.showPage()
        self.c.save()
        self.printCliente()
        
    
class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.fone_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        
    def conecta_bd(self):  # Conecta banco de dados
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor()
        print("Conectando ao banco de dados")
        
    def desconecta_bd(self):  # Desconecta banco de dados
        self.conn.close()
        print("Desconectando ao banco de dados")   
    
    def montaTabelas(self):  # Criar banco de dados
        self.conecta_bd()
        print("Conectando ao banco de dados")
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS clientes (
                                cod INTEGER PRIMARY KEY,
                                nome_cliente CHAR(40) NOT NULL,
                                telefone INTEGER(20),
                                cidade CHAR(40)       
                                )
                            ''')
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()
        
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.fone = self.fone_entry.get()
        self.cidade = self.cidade_entry.get()   
    
    def add_cliente(self):  # Adiciona clientes 
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(''' 
                            INSERT INTO clientes(nome_cliente, telefone, cidade)
                            VALUES(?, ?, ?)
                            ''', (self.nome, self.fone, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente() 
    
    def select_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute('''
                SELECT cod, nome_cliente, telefone, cidade FROM clientes
                ORDER BY nome_cliente ASC; 
                ''')
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(''' SELECT cod, nome_cliente, telefone, cidade FROM clientes
                            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC
                            ''' % nome
        )
        buscanomeCli = self.cursor.fetchall()
        for i in buscanomeCli:
            self.listaCli.insert("", END, values = i)
        
        self.limpa_cliente()
        self.desconecta_bd()
    
    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()
        
        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.fone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(''' DELETE FROM clientes WHERE cod = ? ''', (self.codigo,))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()  
    
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(''' 
            UPDATE clientes 
            SET nome_cliente = ?, telefone = ?, cidade = ? 
            WHERE cod = ? 
            ''', (self.nome, self.fone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
        
class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background='#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        self.canvas_bt = Canvas(self.frame_1,bd=0, bg = '#1e3743', highlightbackground = 'gray', highlightthickness=4)
        self.canvas_bt.place(relx=0.19, rely= 0.08, relwidth= 0.219, relheight=0.19)
        
        # Criação do botão limpar
        self.bt_limpar = Button(self.frame_1, text="Limpar", bd=2, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command=self.limpa_cliente)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação do botão buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg='#107db2', fg='white',
            activebackground= '#108ecb', activeforeground='white',font=('verdana', 8, 'bold'), command= self.busca_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação do botão novo
        self.imgNovo = PhotoImage(file = "BotaoNew.png")
        self.imgNovo = self.imgNovo.subsample(6,6)
        
        self.style = ttk.Style()
        self.style.configure("BW.TButton", relwidth=1, relheight=1, foreground = "gray",
                            borderwidth=0, bordercolor = "gray", background = '#dfe3ee',
                            image= self.imgNovo)
        
        self.bt_novo = ttk.Button(self.frame_1, style = "BW.TButton", command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        self.bt_novo.config(image = self.imgNovo)

        # Criação do botão alterar
        self.imgEdit = PhotoImage(file= "BotaoEdit.png")
        self.imgEdit = self.imgEdit.subsample(8,8)
        
        self.style = ttk.Style()
        self.style.configure("BE.TButton", relwidth=1, relheight=1, foreground = "gray",
                            borderwidth=0, bordercolor = "gray", background = '#dfe3ee',
                            image= self.imgEdit)
        
        self.bt_alterar = ttk.Button(self.frame_1, style = "BE.TButton", command=self.altera_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação do botão apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação da label e entrada do código
        self.lb_codigo = Label(self.frame_1, text="Código", bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.08)

        # Criação da label e entrada do nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)

        # Criação da label e entrada do telefone
        self.lb_telefone = Label(self.frame_1, text="Telefone", bg='#dfe3ee', fg='#107db2')
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.fone_entry = Entry(self.frame_1)
        self.fone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        # Criação da label e entrada da cidade
        self.lb_cidade = Label(self.frame_1, text="Cidade", bg='#dfe3ee', fg='#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)

    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")
        self.listaCli.column("#0", width=1, stretch=NO)
        self.listaCli.column("#1", width=50)
        self.listaCli.column("#2", width=200)
        self.listaCli.column("#3", width=125)
        self.listaCli.column("#4", width=125)
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)
        
        def Quit(): self.root.destroy()
        
        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relarórios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa Cliente", command=self.limpa_cliente)
        
        filemenu2.add_command(label="Ficha do Cliente", command=self.geraRelatCliente)



Application()
