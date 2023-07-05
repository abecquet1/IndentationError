from tkinter import *
from tkinter import ttk
from random import choice
from os import *
from os.path import*
import json
import shutil
from io import *

class LabeledEntry():
    def __init__(self, parent, **kwargs):
        self.frame = Frame(parent)
        self.entry = Entry(self.frame)
        self.label = Label(self.frame, text = kwargs.get('text', ""))
        
    def grid(self, *args, **kwargs): 
        self.frame.grid(*args, **kwargs)
        self.label.grid(row = 1, column = 1, sticky = E)
        self.entry.grid(row = 1, column = 2, sticky = W)


class LevelManager(Tk):


    def __init__(self):
        super().__init__()

        self.title("Level Manager")
        self.create_menu_bar()
        self.path = "."
        self.tree = ttk.Treeview(self)
        with open( join(self.path, "data", "wmap.json"), 'r', encoding = "UTF-8") as f:
            self.wmap = json.load(f)

        with open(join(self.path, "local", "prog.json"), 'r', encoding = "UTF-8") as f:
            self.prog = json.load(f)

    def create_menu_bar(self):
        menu_bar = Menu(self)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Nouveau chapitre", command=self.do_something)
        menu_file.add_command(label="Nouveau niveau", command=self.open_file)
        menu_file.add_command(label="Save", command=self.do_something)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        menu_edit = Menu(menu_bar, tearoff=0)
        menu_edit.add_command(label="Undo", command=self.do_something)
        menu_edit.add_separator()
        menu_edit.add_command(label="Copy", command=self.do_something)
        menu_edit.add_command(label="Cut", command=self.do_something)
        menu_edit.add_command(label="Paste", command=self.do_something)
        menu_bar.add_cascade(label="Edit", menu=menu_edit)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About", command=self.do_about)
        menu_bar.add_cascade(label="Help", menu=menu_help)

        self.config(menu=menu_bar)

    def open_file(self):
        file = askopenfilename(title="Choose the file to open",
                               filetypes=[("PNG image", ".png"), ("GIF image", ".gif"), ("All files", ".*")])
        print(file)

    def do_something(self):
        print("Menu clicked")

    def do_about(self):
        messagebox.showinfo("My title", "My message")

    def purger(self):
        for file in listdir(join(self.path, "data")):
            print(file)
            if file not in self.wmap and file != "wmap.json":
                print("\t->poubelle")
                if isdir(join(self.path, "data", file)): 
                    shutil.rmself.tree(join(self.path, "data", file))
                else:
                    remove(join(self.path, "data", file))
            elif isdir(join(self.path, "data", file)):
                for f in listdir(join(self.path, "data", file)):
                    print(f)
                    if f not in self.wmap[file]["cmap"]:
                        print("\t->poubelle")
                        if isdir(join(self.path, "data", file, f)): 
                            shutil.rmself.tree(join(self.path, "data", file, f))
                        else:
                            remove(join(self.path, "data", file, f))

     
    def save(self):
        with open(join(self.path, "data", "wmap.json"), 'w', encoding = "UTF-8") as f:
            json.dump(self.wmap, f, indent = 4)
        with open(join(self.path, "local", "prog.json"), 'w', encoding = "UTF-8") as f:
            json.dump(self.prog, f, indent = 4)
        self.purger()
        print("Arboréscence mise à jour !")

        



    
    def set_ch(self, ch, **kwargs):
        self.wmap[ch] = {"nom" : kwargs.get('nom', ""),
                    "description" : kwargs.get('desc', ""),
                    "locked" : kwargs.get('locked', ""),
                    "x": kwargs.get('x', 300),
                    "y": kwargs.get('y', 300),
                    "r": kwargs.get('r', 20),
                    "link": kwargs.get('link', []),
                    "cmap" : {}
                    }

        if ch not in listdir(join(self.path, "data")):
            mkdir(join(self.path, "data", ch))
        
        self.show_info()


    def set_niv(self, ch, niv, **kwargs):
        if ch not in self.wmap:
            raise KeyError(f"Chapitre {ch} inexistant")
        else :
            self.wmap[ch]["cmap"][niv] = {"nom" : kwargs.get('nom', ""),
                        "description" : kwargs.get('desc', ""),
                        "locked" : kwargs.get('locked', ""),
                        "x": kwargs.get('x', 300),
                        "y": kwargs.get('y', 300),
                        "r": kwargs.get('r', 20),
                        "link": kwargs.get('link', []),
                        }

        
            
            
    def del_niv(self, ch, niv):
        if ch in self.wmap:
            self.wmap[ch]["cmap"].pop(niv, None)


    def del_ch(self, ch):
        self.wmap.pop(ch, None)


    def show_info(self):
        self.tree['columns'] = ('nb_ex', 'type', 'lock', 'desc', 'x', 'y', 'r', 'link')

        for c in self.tree['columns']:
            self.tree.column(c, anchor='center', width = 75, stretch = False)

        self.tree.column('#0', anchor='center', width = 75, stretch = False)
        self.tree.column('nb_ex', anchor='center', width = 150, stretch = False)
        self.tree.column('desc', anchor='center', width = 200, stretch = False)


        self.tree.heading('nb_ex', text="Nombre d'exercices")

        self.tree.heading('type', text="Type")
        self.tree.heading('lock', text="Vérouillé")
        self.tree.heading('desc', text="Description")
        self.tree.heading('x', text="Abscisse")
        self.tree.heading('y', text="Ordonnée")
        self.tree.heading('r', text="Rayon")
        self.tree.heading('link', text="Liens")

        for ch in self.wmap:
            self.tree.insert('', 'end', ch, text = ch)
            self.tree.set(ch, 'nb_ex', len(self.wmap[ch]["cmap"]))
            for ex in self.wmap[ch]["cmap"]:
                T = "FAR"
                L = self.wmap[ch]["cmap"][ex]["locked"]
                D = self.wmap[ch]["cmap"][ex]["description"]
                X = self.wmap[ch]["cmap"][ex]["x"]
                Y = self.wmap[ch]["cmap"][ex]["y"]
                R = self.wmap[ch]["cmap"][ex]["r"]
                link = self.wmap[ch]["cmap"][ex]["link"]
                self.tree.insert(ch, 'end', ch+"/"+ex, text = ex, values = ("", T, L, D, X, Y, R, link))

        self.tree.grid()

        
        
        

class LevelCreator():
    def __init__(self, root):
        self.root = root
        self.top = Toplevel(root)
        # Fenetre

        # Widgets
        self.enonce = Text(self.top, width=50, height=30)
        self.test = Text(self.top, width=50, height=30)
        self.chap = LabeledEntry(self.top, text = "Chapitre :")
        self.nom = LabeledEntry(self.top, text = "Nom :")

        # Config
        self.test.insert(END, "TYPE : \nSIGN : \nCTXT : \nDATA :")

        # Ligne 1
        Label(text = "enoncé").grid(row = 1, column = 1)
        Label(text = "test").grid(row = 1, column = 2)

        # Ligne 2
        self.enonce.grid(row = 2, column=1)
        self.test.grid(row = 2, column=2)

        # Ligne 3
        
        self.chap.grid(row = 3, column = 1)
        self.nom.grid(row = 3, column = 2)

        self.top.mainloop()


 
                        



LM = LevelManager()

LM.save()

LM.show_info()

LM.mainloop()
