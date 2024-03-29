# Modules python

from tkinter import *
from tkinter import ttk
import json
from math import sqrt
hello = open
from os import *
from io import open

from os.path import join, isdir
import shutil


# Modules projet
from Fenetre import *

class Option(Fenetre_Nav): 

    def apply_themechange(self, event):
        s = self.combo.get()
        self.combo.set(s)

        s = s.lower()

        with open("..\\opt\\style.json", 'r', encoding="utf-8") as f:
            obj = json.load(f)

        obj["selected_style"] = s

        with open("..\\opt\\style.json", 'w', encoding="utf-8") as f:
            json.dump(obj, f, indent=4)

        self.hide(event)
        self.root.set_style()
        self.show()

    def erase_save(self):
        for ch in listdir(join("..", "local")):
            if isdir(join("..", "local", ch)):
                for ex in listdir(join("..", "local", ch)):
                
          
                    f = open(f"..\\local\\{ch}\\{ex}", 'w', encoding="utf-8") 
                    f.close()
        
        f = open(join("..", "local", "bac", "save.py"), 'w', encoding="utf-8")
        f.close()

        f =  open(join("..", "local", "bac", "test.txt"), 'w', encoding="utf-8") 
        f.close()

        f =  open(join("..", "local", "prog.json"), 'r', encoding="utf-8") 
        prog = json.load(f)
        f.close()

        f =  open(join("..", "data", "wmap.json"), 'r', encoding="utf-8") 
        wmap = json.load(f)
        f.close()

        for ch in wmap:
            for ex in wmap[ch]["cmap"]:
                assert ex in prog["niv"][ch], "oups"
                prog["niv"][ch][ex]["locked"] = wmap[ch]["cmap"][ex]["locked"]
                prog["niv"][ch][ex]["done"] = False

        f =  open("..\\local\\prog.json", 'w', encoding="utf-8")
        json.dump(prog, f, indent=4)
        f.close()

            
        


    def show(self):
        super().show()
        
        # Nav
        b_men = ttk.Label(self.nav, text="> Menu", style = 'clickable.TLabel')
        b_men.bind('<Leave>', lambda e: b_men.config(style = 'clickable.TLabel'))
        b_men.bind('<Enter>', lambda e: b_men.config(style = 'hovered.TLabel'))
        b_men.bind('<1>', self.to_men)
        b_men.grid(column=1, row=1, sticky = W)

        self.root.bind('<Escape>',  self.to_men) 

        for child in self.nav.winfo_children(): 
            child.grid_configure(padx=10, pady=10)
        




        # Labels
        th = ttk.Label(self.main, text="> Thème", style = 'clickable.TLabel')
        pr = ttk.Label(self.main, text="> Réinitialiser la progression", style = 'clickable.TLabel')

        th.grid(row = 1, column = 1, sticky = W)
        pr.grid(row = 2, column = 1, sticky = W)

        self.main.rowconfigure(0, weight = 1)
        self.main.rowconfigure(10, weight = 1)
        self.main.columnconfigure(0, weight = 1)
        self.main.columnconfigure(10, weight = 1)


        # Combox
        listeThemes=["Faize", "Sombre", "Clair"]
        self.combo = ttk.Combobox(self.main, values=listeThemes, style = "combo.TCombobox")
  
        self.combo.grid(row = 1, column = 3)

        self.combo.config(font = "courier 16 bold", background = "blue")
  
        self.root.option_add('*TCombobox*Listbox.font', "courier 16 bold")
        self.root.option_add('*TCombobox*Listbox.foreground', "black")
        self.root.option_add('*TCombobox*Listbox.background', "white")
        self.root.option_add('*TCombobox*Listbox.selectForeground', "white")
        self.root.option_add('*TCombobox*Listbox.selectBackground', "black")

        index = [i for i in range(len(listeThemes)) if listeThemes[i].lower() == self.root.style_name.lower()][0]

        self.combo.current(index)
        self.combo.bind("<<ComboboxSelected>>", self.apply_themechange)
        pr.bind('<Leave>', lambda e: pr.config(style = 'clickable.TLabel'))
        pr.bind('<Enter>', lambda e: pr.config(style = 'hovered.TLabel'))
        pr.bind('<1>', lambda e : self.erase_save())

    

        for child in self.main.winfo_children(): 
            child.grid_configure(padx=10, pady=10)


