# Modules python 
from tkinter import ttk
from tkinter import *
from json import load

# Modules projet
from Fenetre import *
from Map import * 


### APP ###

class App(Tk):
    """
    Classe pricinpale du logiciel dérivée de Tk.
    Contient toutes les fenêtres du logiciel, et permettant de les afficher / cacher
    """
    def __init__(self):
        super().__init__()

        # parametres
        self.FS = True

        # objets fils
        self.menu = Menu(self)
        self.bac = Bac(self,
                       "Bac", 
                       f"..\\data\\bac\\save.py", 
                       f"..\\data\\bac\\test.txt")
        self.wmap = WMap(self, f"..\\data\\wmap.json")
        self.map = None
        self.niv = None
        self.opt = None
        self.pgr = None
        self.console = None

        # Paramètres de la fenêtre
        self.title("Indentation Error")
        self.geometry('800x450')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.attributes('-fullscreen', True)

        # Bindings
        self.bind('<Alt-Return>', self.full_screen)

        
        # Styles
        with open("..\\opt\\style_config.json", 'r') as f:
            self.style_dict = json.load(f)

        with open("..\\opt\\style.json", 'r') as f:
            self.style = json.load(f)["selected_style"]

        self.style = self.style_dict[self.style]
        
        s = ttk.Style()

        
        s.configure("rouge.TFrame", background='red')	
        s.configure("vert.TFrame", background='green')	
        s.configure("bleu.TFrame", background='blue')



        # Style 
        s.configure("TFrame", 
                    background = self.style["app_bg"]
        )
        
        s.configure("noir.TFrame", 
                    background = self.style["app_bg"]
        )

        s.configure("border.TFrame", 
                    background = self.style["border"]
        )

        s.configure("context.TFrame", 
                    background = self.style["context_bg"]
        )

        s.configure("context_border.TFrame", 
                    background = self.style["context_border"]
        )
        
        s.configure("titre.TLabel", 
                    font = 'Courier 48 bold', 
                    anchor = "CENTER", 
                    foreground = self.style["app_fg"], 
                    background = self.style["app_bg"]
        )
        
        s.configure("fen_titre.TLabel", 
                    font = 'Courier 18 bold', 
                    anchor = "w", 
                    foreground = self.style["app_fg"], 
                    background = self.style["app_bg"]
        )

        s.configure("clickable.TLabel",
                     font = 'Courier 18 bold', 
                     anchor = "w", 
                     foreground = self.style["app_fg"], 
                     background = self.style["app_bg"]
        )

        s.configure("hovered.TLabel", 
                    font = 'Courier 18  bold underline', 
                    anchor = "w", 
                    foreground = self.style["app_fg"], 
                    background = self.style["app_bg"]
        )

        s.configure("context_clickable.TLabel",
                     font = 'Courier 18 bold', 
                     anchor = "w", 
                     foreground = self.style["context_fg"], 
                     background = self.style["context_bg"]
        )

        s.configure("context_hovered.TLabel", 
                    font = 'Courier 18  bold underline', 
                    anchor = "w", 
                    foreground = self.style["context_fg"], 
                    background = self.style["context_bg"]
        )
        

        # Lancement du menu
        self.menu.show()


    def full_screen(self, event):
        """ Active ou désactive le mode plein écran."""
        self.FS = not(self.FS)
        self.attributes('-fullscreen', self.FS)

    def show_men(self, event):
        """ Affiche le menu principal."""
        self.menu.show()

    def show_bac(self, event):
        """ Affiche le bac à sable."""
        self.bac.show()

    def show_niv(self, event):
        """ Affiche le niveau."""
        self.niv.show()

    def show_wmap(self, event):
        """ Affiche la carte du monde."""
        self.wmap.show()

    def show_cmap(self, chap, event):
        """ Affiche la carte du chapitre."""
        self.cmap.show()


    def report_callback_exception(self, exc_type, exc_value, tb):
        """ Envoie les erreurs tkinter sur la sortie standard."""
        
        if exc_type.__name__ != 'AssertionError':

            s = "\nUne erreur est survenue."
            s+= "\n    Type d'erreur : " + str(exc_type.__name__)
            s+= "\n    Indication : " + str(exc_value)
            s+= "\n"
            local_vars = {}

            s+= "\nLocalisation :"
            while tb:
                filename = tb.tb_frame.f_code.co_filename
                name = tb.tb_frame.f_code.co_name
                line_no = tb.tb_lineno
                s+= f"\n    File {filename} line {line_no}, in {name}"
                tb = tb.tb_next
            s+='\n\n>>> '
        else :
            s = "\n"+str(exc_value)+'\n>>> '
        
        if self.console is None:
            print(s)
        else:
            self.console.text.insert(END, s)
            self.console.text.see(END)



