from Modulos import *
from ValidEntry import Validadores
from frameGrad import GradientFrame
from reports import Relatorios
from funcionalidades import Funcs
#import pycep_correios
import re


class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):
        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches

        Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)

        self.listboxUp = False
    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END, w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False
    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)
    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)
    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)
    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]


autocompleteList = ['Alberto (7714)', 'Bernardo (6010)', 'Cristiano (9390)', 'Dienifer (6347)',
                    'Francisco (9781)', 'Beatriz (3094)', 'Carlos Fonseca (8427)',
                    'Igor Corner (4740)']


def matches(fieldValue, acListEntry):
    pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
    return re.match(pattern, acListEntry)


root = Tk()

class Application(Funcs, Relatorios, Validadores):
    def __init__(self):
        self.root = root
        self.images_base64()
        self.validaEntradas()####
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def cepCorreios(self):
        try:
            self.cidade_entry.delete(0, END)
            self.lograd_entry.delete(0, END)
            self.bairro_entry.delete(0, END)
            zipcode = self.cep_entry.get()
            dadosCep = pycep_correios.get_address_from_cep(zipcode)
            print(dadosCep)
            self.cidade_entry.insert(END, dadosCep['cidade'])
            self.lograd_entry.insert(END, dadosCep['logradouro'])
            self.bairro_entry.insert(END, dadosCep['bairro'])
        except:
            messagebox.showinfo("Titulo da janela", "Cep não encontrado")
    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background= '#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width= 900, height= 700)
        self.root.minsize(width=500, height= 400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee',
                             highlightbackground= '#759fe6', highlightthickness=3 )
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = GradientFrame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background= "#dfe3ee")
        self.aba2.configure(background= "lightgray")

        self.abas.add(self.aba1, text = "Aba 1")
        self.abas.add(self.aba2, text="Aba 2")

        self.abas.place(relx=0, rely=0, relwidth=0.98, relheight=0.98)

        self.canvas_bt = Canvas(self.aba1, bd=0, bg='#1e3743', highlightbackground = 'gray',
            highlightthickness=5)
        self.canvas_bt.place(relx= 0.19, rely= 0.08, relwidth= 0.22, relheight=0.19)

        ### Criação do botao limpar
        self.bt_limpar = Button(self.aba1, text= "Limpar", bd=2, bg = '#107db2',fg = 'white',
                                activebackground='#108ecb', activeforeground="white"
                                , font = ('verdana', 8, 'bold'), command= self.limpa_cliente)
        self.bt_limpar.place(relx= 0.2, rely=0.1, relwidth=0.1, relheight= 0.15)
        ### Criação do botao buscar
        self.bt_buscar = Button(self.aba1, text="Buscar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command = self.janela2)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        ### Criação do botao novo
        ## imgNovo
        self.btnovo = PhotoImage(data=base64.b64decode(self.btnovo_base64))
        self.btnovo = self.btnovo.subsample(2, 2)

        self.bt_novo = Button(self.aba1, bd =0, image = self.btnovo, command= self.add_cliente)
        self.bt_novo.place(relx=0.55, rely=0.1, width=60, height=30)

        ### Criação do botao alterar
        self.btalterar = PhotoImage(data=base64.b64decode(self.btalterar_base64))
        self.btalterar = self.btalterar.subsample(2, 2)

        self.bt_alterar = Button(self.aba1, image = self.btalterar, bd=0,
                                 command=self.altera_cliente)
        self.bt_alterar.place(relx=0.67, rely=0.1, width=60, height=30)
        ### Criação do botao apagar
        self.bt_apagar = Button(self.aba1, text="Apagar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1,
                             relwidth=0.1, relheight=0.15)

        ## Criação da label e entrada do codigo
        self.lb_codigo = Label(self.aba1, text = "Código", bg= '#dfe3ee', fg = '#107db2')
        self.lb_codigo.place(relx= 0.05, rely= 0.05)

        self.codigo_entry = Entry(self.aba1, validate="key",validatecommand=self.vcmd2)
        self.codigo_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)

        ## Criação da label e entrada do nome
        self.lb_nome = Label(self.aba1, text="Nome", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nome.place(relx=0.01, rely=0.35)

        self.nome_entry = Entry(self.aba1)
        self.nome_entry.place(relx=0.08, rely=0.35, relwidth=0.5)

        ## Criação da label e entrada do cep
        self.lb_cep = Button(self.aba1, text="CEP", bg='#dfe3ee', fg='#107db2',
                             command= self.cepCorreios)
        self.lb_cep.place(relx=0.65, rely=0.35)

        self.cep_entry = Entry(self.aba1)
        self.cep_entry.place(relx=0.75, rely=0.35, relwidth=0.2)

        ## Criação da label e entrada do telefone
        self.lb_fone = Label(self.aba1, text="Telefone", bg= '#dfe3ee', fg = '#107db2')
        self.lb_fone.place(relx=0.05, rely=0.55)

        self.fone_entry = Entry(self.aba1)
        self.fone_entry.place(relx=0.15, rely=0.55, relwidth=0.3)

        ## Criação da label e entrada da cidade
        self.lb_cidade = Label(self.aba1, text="Cidade", bg= '#dfe3ee', fg = '#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.55)

        self.cidade_entry = Entry(self.aba1)
        self.cidade_entry.place(relx=0.6, rely=0.55, relwidth=0.3)

        ## Criação da label e entrada do logradouro
        self.lb_lograd = Label(self.aba1, text="Endereço", bg='#dfe3ee', fg='#107db2')
        self.lb_lograd.place(relx=0.05, rely=0.75)

        self.lograd_entry = Entry(self.aba1)
        self.lograd_entry.place(relx=0.15, rely=0.75, relwidth=0.3)

        ## Criação da label e entrada da bairro
        self.lb_bairro = Label(self.aba1, text="Bairro", bg='#dfe3ee', fg='#107db2')
        self.lb_bairro.place(relx=0.5, rely=0.75)

        self.bairro_entry = Entry(self.aba1)
        self.bairro_entry.place(relx=0.6, rely=0.75, relwidth=0.3)

        #### drop down button
        self.Tipvar = StringVar()
        self.TipV = ("Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viuvo(a)")
        self.Tipvar.set("Solteiro(a)")
        self.popupMenu = OptionMenu(self.aba2, self.Tipvar, *self.TipV)
        self.popupMenu.place(relx= 0.1, rely=0.1, relwidth=0.2, relheight=0.2)
        self.estado_civil = self.Tipvar.get()
        print(self.estado_civil)
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3,
                                     column=("col1", "col2", "col3", "col4"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Codigo")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Cidade")
        self.listaCli.column("#0", width=1, stretch = NO)
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

        menubar.add_cascade(label= "Opções", menu=filemenu)
        menubar.add_cascade(label="Relatorios", menu=filemenu2)

        filemenu.add_command(label="Sair", command=Quit)
        filemenu.add_command(label="Limpa cliente", command= self.limpa_cliente)

        filemenu2.add_command(label="Ficha do cliente", command=self.geraRelatCliente)
    def janela2(self):
        self.root2 = Toplevel()
        self.root2.title(" Janela 2  ")
        self.root2.configure(background='gray75')
        self.root2.geometry("360x160")
        self.root2.resizable(TRUE, TRUE)
        self.root2.transient(self.root)
        self.root2.focus_force()
        self.root2.grab_set()
    def validaEntradas(self):
        ### Naming input validators

        self.vcmd2 = (self.root.register(self.validate_entry2), "%P")


Application()