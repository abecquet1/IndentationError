# Modules python
from tkinter import *
from tkinter import ttk
from io import StringIO
from tkinter import simpledialog 

# Modules projet 
from TextFrame import *




### FENETRE ###

class Fenetre:
    """ Classe abstraite. Fenêtre du logiciel pouvant être affichée ou cachée."""
    def __init__(self, root):
        """ Constructeur de Fenêtre.
         --- root : App : l'app dans laquelle est lancée la fenêtre."""
        self.root = root
        self.shown = False

        self.frame = None
        self.nav = None
        self.main = None


    def show(self):
        """ Affiche la fenêtre."""
        if self.shown:
            return None
    
        # Mise à jour du booléen 
        self.shown = True

        # La frame
        self.frame = ttk.Frame(self.root, padding="3 3 3 3", style = "noir.TFrame")
        self.frame.grid(column=0, row=0, sticky="NSEW")

        # Focus
        self.frame.focus_set()

    def hide(self, event):
        """ Cache le fenêtre."""
        self.shown = False
        self.frame.destroy()
        self.root.focus_set()
        self.root.unbind('<Escape>')




### FENETRE_NAV ###

class Fenetre_Nav(Fenetre):
    """ Classe Abstraite. Comme fenêtre mais avec un bandeau de navigation en haut."""
    def __init__(self, root):
        super().__init__(root)
        self.nav = None
        self.main = None
        
        
    def show(self):
        """ Affiche la fenêtre."""
        super().show()
    
        self.frame.rowconfigure(2, weight=1)
        
        self.nav = ttk.Frame(self.frame, style = 'noir.TFrame', width = 100, height = 300)
        self.nav.grid(column=1, row=1, sticky = "NSEW")

        self.main = ttk.Frame(self.frame, style = 'noir.TFrame', width = 100, height = 300)
        self.main.grid(column=1, row=2, sticky = "NSEW")
        self.frame.columnconfigure(1, weight = 1)


    def to_men(self, event):
        """ Retourne au menu pricipal."""
        self.hide(event)
        self.root.show_men(event)

    
    
################## MENU ################## 
class Menu(Fenetre):
    """ Menu principal de l'app."""
 
    def show(self):
        
        super().show()

        # Frame 
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=4)
        self.frame.rowconfigure(1, weight=1)


        # Nav
        self.nav = ttk.Frame(self.frame, style = 'noir.TFrame', width = 100, height = 300)
        self.nav.grid(column=1, row=1, sticky = "NSEW")

        self.nav.rowconfigure(1, weight = 6)
        self.nav.rowconfigure(7, weight = 1)

        # Bouttons
        b_map = ttk.Label(self.nav, text="> Continuer", style = 'clickable.TLabel')
        b_bac = ttk.Label(self.nav, text="> Bac à sable", style = 'clickable.TLabel')
        #b_man = ttk.Label(self.nav, text="> Manuel", style = 'clickable.TLabel')
        #b_pgr = ttk.Label(self.nav, text="> Progression", style = 'clickable.TLabel')
        b_opt = ttk.Label(self.nav, text="> Options", style = 'clickable.TLabel')
        
        b_map.grid(column=1, row=2, sticky = W)
        b_bac.grid(column=1, row=3, sticky = W)
        #b_man.grid(column=1, row=4, sticky = W)
        #b_pgr.grid(column=1, row=5, sticky = W)
        b_opt.grid(column=1, row=6, sticky = W)
        
        for child in self.nav.winfo_children(): 
            child.grid_configure(padx=10, pady=10)


        # Main frame
        self.main = ttk.Frame(self.frame, style = 'noir.TFrame', width = 400, height = 300)
        self.main.grid(column=2, row=1, sticky = "NSEW")

        self.main.rowconfigure(1, weight = 1)
        self.main.columnconfigure(1, weight = 1)

        # Titre
        ttk.Label(self.main, text="INDENTATION\nERROR [1.0]", style = "titre.TLabel").grid(column = 1, row = 1)


        # Bindings 
        b_map.bind('<Leave>', lambda e: b_map.config(style = 'clickable.TLabel'))
        b_map.bind('<Enter>', lambda e: b_map.config(style = 'hovered.TLabel'))
        b_map.bind('<1>', self.to_wmap)
        
        b_bac.bind('<Leave>', lambda e: b_bac.config(style = 'clickable.TLabel'))
        b_bac.bind('<Enter>', lambda e: b_bac.config(style = 'hovered.TLabel'))
        b_bac.bind('<1>', self.to_bac)
        
        #b_man.bind('<Leave>', lambda e: b_man.config(style = 'clickable.TLabel'))
        #b_man.bind('<Enter>', lambda e: b_man.config(style = 'hovered.TLabel'))

        #b_pgr.bind('<Leave>', lambda e: b_pgr.config(style = 'clickable.TLabel'))
        #b_pgr.bind('<Enter>', lambda e: b_pgr.config(style = 'hovered.TLabel'))

        b_opt.bind('<Leave>', lambda e: b_opt.config(style = 'clickable.TLabel'))
        b_opt.bind('<Enter>', lambda e: b_opt.config(style = 'hovered.TLabel'))
        b_opt.bind('<1>', self.to_opt)

        self.root.bind('<Escape>', lambda e: Context.confirmation("Êtes-vous sûr de vouloir quitter ?", self.root, self.root.destroy) , add= "+") 
            


    def to_bac(self, event):
        """ Affiche le bac à sable."""
        self.hide(event)
        self.root.show_bac(event)

    def to_niv(self, event):
        """ Affiche le niveau."""
        self.hide(event)
        self.root.show_niv(event)

    def to_wmap(self, event):
        """ Affiche la carte du monde."""
        self.hide(event)
        self.root.show_wmap(event)

    def to_opt(self, event):
        """ Affiche la carte du monde."""
        self.hide(event)
        self.root.show_opt(event)

    

        




################## IDEUX ################## 
class Ideux(Fenetre_Nav):
    """ Fenêtre reproduisant un mini IDE.
    --- nav : bandeau de navigation
    --- main : frame principale 
    ------ code -> pour taper son code 
    ------ console -> pour exécuter le code / des commandes / pour les inputs
    ------ lateral -> énoncé d'un exercice ou tests unitaires 
    """

    

    def __init__(self, root, nom, c_save, l_save):
        
        """ Constructeur de l'IDE.
        --- nom : str -> le nom de la fenêtre (bac ou niv)
        --- c_save : str -> chemin du fichier de sauvegarde du code
        --- l_save : str -> chemin du fichier de sauvegarde du panneau latéral
        """
        super().__init__(root)
        self.nom = nom
        self.chap = ""

        self.code = None
        self.console = None
        self.lateral = None
        self.__context__ =  {"input" : self.input}
        self.context =  {"input" : self.input}
        self.out = StringIO()
        self.inp = StringIO()
        self.__stdout__ = sys.stdout
        self.__stdin__ = sys.stdin
        self.c_save = c_save
        self.l_save = l_save
        self.saved = True 


    def input(self, *args): 
        prompt = ""
        if len(args) != 0 :
            prompt = args[0]
        return simpledialog.askstring("input", prompt)



    def show(self):
        """ Affiche la fenêtre ideuse"""
        super().show()
        self.saved = True 
        
        # Nav
        b_men = ttk.Label(self.nav, text="> Menu", style = 'clickable.TLabel')
        b_man = ttk.Label(self.nav, text="> Manuel", style = 'clickable.TLabel')

        b_men.bind('<Leave>', lambda e: b_men.config(style = 'clickable.TLabel'))
        b_men.bind('<Enter>', lambda e: b_men.config(style = 'hovered.TLabel'))
        b_men.bind('<1>', self.to_men)
        
        b_man.bind('<Leave>', lambda e: b_man.config(style = 'clickable.TLabel'))
        b_man.bind('<Enter>', lambda e: b_man.config(style = 'hovered.TLabel'))

        b_men.grid(column=1, row=1, sticky = W)
        b_man.grid(column=7, row=1, sticky = W)

        for child in self.nav.winfo_children(): 
            child.grid_configure(padx=10, pady=10)

        # Main
        self.main.columnconfigure(1, weight=5)
        self.main.columnconfigure(2, weight=1)

        # Code
        self.code = CodeFrame(self.root, self, 80, 24)
        self.code.grid(row = 1, column =  1)
        self.code.bindings()
        with open(self.c_save, 'r', encoding = 'utf-8') as f: 
            self.code.text.insert(END, f.read().rstrip())


        # Console
        self.console = ConsoleFrame(self.root, self, 80, 8, titre = "Console")
        self.console.grid(row =2, column = 1)
        
        # Latéral
        self.lateral = LateralFrame(self.root, self,  36, 46)
        self.lateral.grid(row = 1, column =2, rowspan = 2, padx = (10,10), pady = (0,12))
        with open(self.l_save, 'r', encoding = 'utf-8') as f:
            self.lateral.text.insert(END, f.read().rstrip())

        # Lien entre les objets
        self.code.console = self.console
        self.root.console = self.console
        self.code.lateral = self.lateral

        








### BAC ###
class Bac(Ideux):
    """ Fenêtre du bac à sable."""
    def show(self):
        """ Affiche le niveau."""
        super().show()

        self.root.bind('<Escape>',  self.to_men) 

    def get_test_cases(self):
        """ Acquiert les tests unitaire à partir du panneau latéral. """
        return self.lateral.text.get(1.0, END).split("\n")
    
    def hide(self, event):
        self.code.save(event)
        super().hide(event)


################## NIVEAU ################## 
class Niveau(Ideux):
    """ Fenêtre d'un niveau."""

    def __init__(self, root, nom, f_save, f_enonce, f_test, chap):
        """
        Constructeur de niveau. 
        f_save : str -> chemin du fichier de sauvegarde du code
        f_enonce : str -> chemin du fichier de sauvegarde d'e l'enoncé (affiché dans le panneau latéral)
        f_test : str -> chemin du fichier de sauvegarde des tests unitaires (non affichés)
        chap : str -> nom du chapitre
        """
        super().__init__(root, nom, f_save, f_enonce)
        self.f_enonce = f_enonce
        self.f_test = f_test
        self.chap = chap


    def show(self):
        """ Affiche le niveau."""
        super().show()

        b_map = ttk.Label(self.nav, text="> Map", style = 'clickable.TLabel')

        b_map.bind('<Leave>', lambda e: b_map.config(style = 'clickable.TLabel'))
        b_map.bind('<Enter>', lambda e: b_map.config(style = 'hovered.TLabel'))
        b_map.bind('<1>', self.to_map)
        self.root.bind('<Escape>', self.to_map, add= "")

        b_map.grid(column=3, row=1, sticky = W)

        for child in self.nav.winfo_children(): 
            child.grid_configure(padx=10, pady=10)

        self.lateral.text.configure(state = "disabled")

        
    def get_test_cases(self):
        """ Acquiert les tests unitaire à partir du fichier de sauvegarde. """
        with open(self.f_test, 'r', encoding='utf-8') as file:
            data = file.readlines()
        return data


    def to_map(self, event):
        """ Affiche la carte du chapitre."""
        self.hide(event)
        self.root.show_cmap(self.chap, event)

    def hide(self, event):
        self.code.save(event)
        super().hide(event)