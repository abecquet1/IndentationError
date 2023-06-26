# Modules python
from tkinter import *
from tkinter import ttk
from io import StringIO
import pygments.lexers              # need pip install 
from chlorophyll import CodeView    # need pip install 
import json
import sys
import threading
import time

# Modules projet
import Test
import Context
import Fenetre



### TextFrame ###
class TextFrame:
    """ Classe abstraite. Zone de texte avec du joli autour liée à un IDE."""
    def __init__(self, root, ideux, w, h, titre = "ENONCE / TEST CASES"):
        self.root = root
        self.ideux = ideux

        self.width = w
        self.height = h
        self.titre = titre

        self.frame = None
        self.border = None
        self.nav = None
        self.text = None
        self.h_button = None


    def grid(self, **kwargs):
        """ Positionne la zone."""
        self.frame = ttk.Frame(self.ideux.main, style = "noir.TFrame")
        self.frame.grid(**kwargs)
        
        self.nav = ttk.Frame(self.frame, style = "noir.TFrame")
        self.border = Frame(self.frame, bg = "gray")
        self.nav.grid(column = 1, row = 1, sticky = 'EW')
        self.nav.columnconfigure(1, weight = 1)
        self.nav.columnconfigure(2, weight = 1)
        self.border.grid(column = 1, row = 2)
        
        self.titre = ttk.Label(self.nav, text = self.titre, style = 'fen_titre.TLabel')
        self.titre.grid(column =1, row = 1,  sticky = "W")
        self.h_button = ttk.Label(self.nav, text = "?", anchor = "e",  style = 'fen_titre.TLabel')
        self.h_button.grid(column =2, row = 1,  sticky = "E")




### LateralFrame ###

class LateralFrame(TextFrame):
    """ Simple zone de texte avec scroll éditable ou non."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll = None

        

    def grid(self, *args, **kwargs):
        """ Positionne la zone."""
        super().grid(*args, **kwargs)
        self.text = Text(self.border, 
                         height=self.width, #56,
                         width= self.height, #74,
                         font = "Courier 12",
                         xscrollcommand = True,
                         bg = "gray10",
                         fg = "white")

        
        self.scroll = Scrollbar(self.border)

        self.text.configure(yscrollcommand = self.scroll.set, insertbackground = "white")
        self.scroll.config(command = self.text.yview)

        
        self.text.grid(column = 1, row = 2, sticky = "NS")
        self.scroll.grid(column = 2, row = 2, sticky = "NS")

        s = ""
        if isinstance(self.ideux, Fenetre.Niveau):
            s+= "### ENONCE ###\n\n"
            s+= "L'énoncé de l'exercice.\n\n"
            s+= "Suivez les instructions puis testez votre programme (F6) pour débloquer les exercices suivants."
            self.h_button.bind("<1>", lambda e: Context.contextFrame(s,self.root, 50 , 7, e))

        else:
            s+= "### TESTS UNITAIRES ###\n\n"
            s+= "Cette zone vous permet de configurer les tests (F6) à appliquer à une fonction.\n\n"
            s+= " --- Renseignez sur la première ligne le format de la fonction.\n\n"
            s+= " ex : 'carre(x:int) -> int' indique que vous voulez tester la fonction "
            s+= "'carre' prenant en argument un entier x et renvoyant un autre entier. \n\n"
            s+= " --- Renseignez sur les lignes suivantes les résultats attendus pour différents arguments.\n\n"
            s+= " ex : '2;4' indique que la fonction carre, appelée avec l'argument 2, doit renvoyer 4"
            self.h_button.bind("<1>", lambda e: Context.contextFrame(s,self.root, 50 , 17, e))
            
            
  



### ConsoleFrame ###

class ConsoleFrame(TextFrame):
    """ Fenêtre textuelle simulant une console Python."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def grid(self, *args, **kwargs):
        """ Positionne la zone."""
        super().grid(*args, **kwargs)
        self.text = CodeView(self.border,
                             width = self.width,#104
                             height = self.height,#13
                             lexer=pygments.lexers.PythonLexer,
                             color_scheme="ayu-dark",
                             font = "Courier 12",
                             tab_width = 4)


        self.text.insert(1.0, ">>> ")
        self.text.grid(column = 1, row = 2, columnspan = 2, sticky = "NSEW", padx = (2,2), pady =(2, 1))

        s = "### CONSOLE : Zone de sortie ###\n\n"
        s+= "Cette zone vous permet de visualiser l'exécution de votre programme.\n\n"
        s+= "Pas de commande spécifique ici."
        
        self.h_button.bind("<1>", lambda e: Context.contextFrame(s,self.root, 50 , 6, e))

        self.text.bind("<Return>", lambda e: self.run(e), add="")
        self.text.bind("<Key>", lambda e: self.key_block(e))
        self.text.bind("<F1>", lambda e: self.clear(e))
        

    def clear(self, event):
        """ Vide la zone de texte."""
        self.text.delete(1.0, END)
        self.text.insert(END, ">>> ")
        self.text.mark_set("insert", END)


    def key_block(self, event):
        """ Permet d'empêcher certains événements de se produire."""
        c, = self.text.count("end -1c linestart", "insert")
        if event.keysym not in ["Left", "Right", "Up", "Down", "Escape", "Control-C", "Control-A", "Control-S", "<F1>"]:
            if c < 4:
                return "break"
            if event.keysym == "BackSpace" and c == 4:
                return "break"



    def run(self, event):
        """ Éxécute la commande console."""
        try :
            # try / except pour pouvoir afficher correctement une erreur éventuelle.

            if self.text.index("insert lineend") == self.text.index("end -1c") and self.text.count("end -1c linestart", "insert")[0]>3:
                # on s'assure que le curseur est au bon endroit
                
                # Récupération de la commande
                s = self.text.get("insert linestart", "insert lineend")[4:].rstrip()

                if s != "":
                    # Gestion des Sorties
                    self.text.insert(END, "\n")
                    self.ideux.out = StringIO()
                    sys.stdout = self.ideux.out

                    # On éxécute la commande en essaynt de récupérer un éventuel résultat
                    try : 
                        exec(f"__res__ = ({s})", self.ideux.context)
                    except:
                        exec(s, self.ideux.context) # le contexte n'est pas réinitialisé 

                    # Si on a un résultat, on l'affiche
                    if "__res__" in self.ideux.context and self.ideux.context["__res__"] is not None:
                        print(self.ideux.context["__res__"])

                    sys.stdout = self.ideux.__stdout__

                    self.text.insert(END, self.ideux.out.getvalue())
                    self.text.insert(END, ">>> ")

                else:
                    self.text.insert(END, "\n>>> ")

            # Gestion des Sorties
            self.ideux.out = StringIO()
            sys.stdout = self.ideux.__stdout__
            self.text.mark_set("insert", END)
            self.text.see(END)
            return "break"
        

        except Exception as exc:
            # try / except pour pouvoir afficher correctement une erreur éventuelle.
            self.root.report_callback_exception(exc.__class__, str(exc), exc.__traceback__)
            self.text.see(END)
            self.text.mark_set("insert", END)
            return "break"




### CodeFrame ###

class CodeFrame(TextFrame):
    """ Fenêtre textuelle permettant à l'utilisateur d'éditer du code Python."""
    
    def __init__(self, root, ideux, w, h, *args, **kwargs):
        super().__init__(root, ideux, w, h, *args, **kwargs)
        self.ideux.out = StringIO()

                    
    
    def save(self, event):
        """ Sauvegarde le contenu de la fenêtre dans le fichier de savegarde de l'IDE."""
        self.ideux.console.text.insert(END, "Fichier sauvegardé.\n>>> ")
        with open(self.ideux.c_save, 'w') as file:
            file.write(self.text.get(1.0, END))
        with open(self.ideux.l_save, 'w') as file:
            file.write(self.ideux.lateral.text.get(1.0, END))


        

    def run(self, event):
        """ Exécute le code en affichant la sortie standard dans la console de l'IDE."""
        self.ideux.context = {}
        self.save(event)
        self.ideux.console.text.insert(END, "Éxécution du code (+save + context wipe):\n")

        # Gestion des sorties
        old_stdout = sys.stdout
        sys.stdout = self.ideux.out

        # Exécution
        s = self.text.get(1.0, END)
        exec(s, self.ideux.context)

        # Affichage
        if len(self.ideux.out.getvalue().split("\n"))+1 < 1000 - len(self.ideux.console.text.get(1.0, END).split("\n")):
            self.ideux.console.text.insert(END, self.ideux.out.getvalue())
            self.ideux.console.text.insert(END, ">>> ")
            self.ideux.console.text.see(END)
            self.text.mark_set("insert", END)

        else:
            # En cas de dépassement de la capacité max de la textFrame
            sys.stdout = old_stdout
            self.ideux.out = StringIO()
            raise ValueError("Console pleine (1000 lignes max)")
        
        # Gestion des sorties
        sys.stdout = old_stdout
        self.ideux.out = StringIO()



    def get_test_cases(self):
        """ Abtraite : Acquièrt les tests unitaires via l'IDE."""
        return self.ideux.get_test_cases()


    def test(self, event):
        """ Effectue les tests."""
        # Import des test cases
        self.save(event)
        self.ideux.context = {}
        test_cases = self.get_test_cases()

        info = Test.get_info(test_cases.split("\n")[0])
                


        self.ideux.console.text.insert(END, "Test de la fonction "+str(info['f_name'])+" :\n")

        # On redirige stdout et excepthook dans une SIO sui ne sera pas affichée
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        # On éxécute le code en renommant f le fonction à tester

        #f = lambda : None
        s = self.text.get(1.0, END)

        exec(s, self.ideux.context) 
        exec(f"__fonction__ = {info['f_name']}", self.ideux.context)
        

        # On redirige stdout dans une SIO sui ne sera pas affichée et on appelle test_fonction
        sys.stdout = mystdout = StringIO()
        done = Test.test_fonction(test_cases, self.ideux.context["__fonction__"])

        if done is not None:

            if self.ideux.nom != "Bac":

                # DONE
                with open("..\\data\\prog.json", 'r', encoding = 'utf-8') as file:
                    prog = json.load(file)

                with open(f"..\\data\\{self.ideux.chap}\\cmap.json", 'r', encoding = 'utf-8') as file:
                    cmap = json.load(file)
                    
                prog["niv"][self.ideux.chap][self.ideux.nom]["done"] = True
                for n in cmap[self.ideux.nom]["link"]:
                    prog["niv"][self.ideux.chap][n]["locked"] = False

                with open("..\\data\\prog.json", 'w', encoding = 'utf-8') as file:
                    json.dump(info, file, indent = 4)

                # UNLOCK LINKED
                with open("..\\data\\prog.json", 'w', encoding = 'utf-8') as file:
                    json.dump(prog, file, indent = 4)
        

        
        self.ideux.console.text.insert(END, mystdout.getvalue())
        self.ideux.console.text.insert(END, ">>> ")
        self.text.mark_set("insert", END)
        self.ideux.console.text.see(END)
        


    def grid(self, **kwargs):
        """ Positionne la zone."""
        if self.ideux.chap == "":
            self.titre = f"PROGRAMME : BAC A SABLE"
        else:
            self.titre = f"PROGRAMME : {self.ideux.chap.upper()}/{self.ideux.nom.upper()}"
        super().grid(**kwargs)

        self.text = CodeView(self.border,
                             width = self.width,
                             height = self.height,
                             lexer=pygments.lexers.PythonLexer,
                             color_scheme="ayu-dark",
                             font = "Courier 12",
                             tab_width = 4)
        
        
        self.text.grid(column = 1, row = 2, columnspan = 2, sticky = "NSEW", padx = (2,2), pady =(2, 1))

    import tkinter as tk

    def autoIndent(self):
        index = f"{self.text.index('insert')}-1l linestart"
        string = self.text.get(index, f"{index} lineend")
        tab_count = len(string)-len(string.lstrip("\t"))

        string = string.rstrip(" \n")
        

        if string!= "" and string[-1] == ':':
            tab_count+=1
            
        self.text.insert("insert linestart", "\t"*tab_count)


    def bindings(self):
        """ Bindings."""
        self.text.bind('<F5>', self.run)
        self.text.bind('<F6>', self.test)
        self.text.bind('<Control-s>', self.save)
        self.text.bind("<Return>", lambda ev:self.text.after(1, self.autoIndent))
        s = "### PROGRAMME : Zone d'édition ###\n\n"
        s+= "Cette zone vous permet d'écrire votre programme Python.\n\n"
        s+= "Commandes :\n"
        s+= "   --- F5 : exécute le programme dans la console.\n"
        s+= "   --- F6 : teste le programme\n"
        s+= "   --- Ctrl + S : sauvegarde le programme"
        self.h_button.bind("<1>", lambda e: Context.contextFrame(s,self.root, 50 , 9, e))


        

