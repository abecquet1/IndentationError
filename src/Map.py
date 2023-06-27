# Modules python
from tkinter import *
from tkinter import ttk
import json
from math import sqrt

# Modules projet
from Fenetre import *



class Noeud:
    def __init__(self, root, can, nom, x, y, r, color):
        self.root = root
        self.nom = nom
        self.can = can
        self.color = color
        self.r = r
        self.x = x
        self.y = y
        self.icone = can.create_oval(x-r, y-r, x+r, y+r, fill = color, outline = root.style["node_edge"], width = 2)
        self.etiquette = can.create_text(x-r//4, y-(3*r)//2, text = self.nom, font = "Courier 12 bold", fill = root.style["map_fg"])
        
    def creer_arc(self, n):
        ux = n.x - self.x
        uy = n.y - self.y
        N = sqrt(ux**2+uy**2)
        ux/=N
        uy/=N
        self.can.create_line(self.x+self.r*ux, self.y+self.r*uy, n.x-n.r*ux, n.y-n.r*uy, fill = self.root.style["node_edge"], width = 2)




class Map(Fenetre_Nav):
    """Carte (classe abstraite)"""
    
    def __init__(self, root, info):
        super().__init__(root)
        self.can = None
        self.info = info
        self._x = 0
        self._y = 0
        

    def move(self, event):
        """drag and drop"""
        deltax = event.x - self._x
        deltay = event.y - self._y
        self._x = event.x
        self._y = event.y
        self.can.move("all", deltax, deltay)


    def start_move(self, event):
        """drag and drop"""
        self._x = event.x
        self._y = event.y


    def zoom(self, event):
        """Zoom et dezoom sur la carte"""
        if event.delta > 0:
            self.can.scale("all", event.x, event.y, 1.1, 1.1)
        else:
            self.can.scale("all", event.x, event.y, 0.9, 0.9)


        
        
    def show(self):
        super().show()
        self.can = Canvas(self.main, width = 1910, height = 1018, background = self.root.style["map_bg"])

        # NAV ZONE
        b_men = ttk.Label(self.nav, text="> Menu", style = 'clickable.TLabel')
        b_man = ttk.Label(self.nav, text="> Manuel", style = 'clickable.TLabel')

        b_men.bind('<Leave>', lambda e: b_men.config(style = 'clickable.TLabel'))
        b_men.bind('<Enter>', lambda e: b_men.config(style = 'hovered.TLabel'))
        b_men.bind('<1>', lambda e: self.to_men(e))
        
        b_man.bind('<Leave>', lambda e: b_man.config(style = 'clickable.TLabel'))
        b_man.bind('<Enter>', lambda e: b_man.config(style = 'hovered.TLabel'))

     

        b_men.grid(column=1, row=1, sticky = W)
        b_man.grid(column=10, row=1, sticky = W)

        for child in self.nav.winfo_children(): 
            child.grid_configure(padx=10, pady=10)

        self.build_map()

        self.can.grid(row = 2, sticky = "N")

        self.can.bind("<ButtonPress-1>", self.start_move)
        self.can.bind("<B1-Motion>", self.move)    
        self.can.bind("<MouseWheel>", self.zoom)


    def hide(self, event):
        self.can.destroy()
        super().hide(event)



class WMap(Map):
    def show(self):
        super().show()
        self.frame.bind('<Escape>', lambda e : self.to_men(e), add = "")

    def to_map(self, chap, event):
        """Permet de lancer chapitre"""
        print(f"opening chapter {chap}")
        self.root.cmap = CMap(self.root, f"..\\data\\{chap}\\cmap.json",chap)
        self.hide(event)
        self.root.show_cmap(chap, event)

    def build_map(self):
        with open(self.info, "r") as f:
            dic = json.load(f)

        for ch in dic:
            c = self.root.style["node_unlocked"]

            noeud = Noeud(self.root,
                          self.can,
                          ch, 
                          int(dic[ch]["x"]),
                          int(dic[ch]["y"]),
                          int(dic[ch]["r"]),
                          c)

            dic[ch]["noeud"] = noeud
            
            self.can.tag_bind(noeud.icone,
                              sequence = '<1>',
                              func = lambda e, c = ch: self.to_map(c, e))
            
        for ch1 in dic:
            for ch2 in dic[ch1]["link"]:
                dic[ch1]["noeud"].creer_arc(dic[ch2]["noeud"])

    


class CMap(Map):
    """Carte de chapitre"""
    def __init__(self, root, info, chap):
        super().__init__(root, info)
        self.chap = chap

    def to_wmap(self, event):
        """Permet de revenir à la world map"""
        self.hide(event)
        self.root.show_wmap(event)

    def to_niv(self, ex, event):
        """Ouvre un niveau du chapitre"""
        print(f"opening level {ex}")
        self.root.niv = Niveau(self.root, 
                               ex, 
                               f"..\\data\\{self.chap}\\{ex}\\save.py", 
                               f"..\\data\\{self.chap}\\{ex}\\enonce.txt", 
                               f"..\\data\\{self.chap}\\{ex}\\test.txt",
                               self.chap)
        self.hide(event)
        self.root.show_niv(event)

    def show(self, *args):
        super().show(*args)
        
        b_wmap = ttk.Label(self.nav, text="> Wmap", style = 'clickable.TLabel')
        b_wmap.bind('<Leave>', lambda e: b_wmap.config(style = 'clickable.TLabel'))
        b_wmap.bind('<Enter>', lambda e: b_wmap.config(style = 'hovered.TLabel'))
        b_wmap.bind('<1>', self.to_wmap)
        self.frame.bind('<Escape>', lambda e : self.to_wmap(e), add = "")
        b_wmap.grid(column=2, row=1, sticky = W)


    def build_map(self):
        with open(self.info, "r") as f:
            dic = json.load(f)

        with open("..\\data\\prog.json", "r") as f:
            prog = json.load(f)

        for ex in dic:
            c = self.root.style["node_unlocked"]
            if prog["niv"][self.chap][ex]["done"]:
                c = self.root.style["node_done"]
            if prog["niv"][self.chap][ex]["locked"]:
                c = self.root.style["node_locked"]

            noeud = Noeud(self.root,
                          self.can,
                          ex, 
                          int(dic[ex]["x"]),
                          int(dic[ex]["y"]),
                          int(dic[ex]["r"]),
                          c)

            dic[ex]["noeud"] = noeud

            if not prog["niv"][self.chap][ex]["locked"]:
                self.can.tag_bind(noeud.icone,
                                  sequence = '<1>',
                                  func = lambda e, x = ex: self.to_niv(x, e))
            
        for ex1 in dic:
            for ex2 in dic[ex1]["link"]:
                dic[ex1]["noeud"].creer_arc(dic[ex2]["noeud"])




            
            
            







