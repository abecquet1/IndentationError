from tkinter import *
from tkinter import ttk
from random import choice
from os import *
from os.path import*
import json
import shutil
from io import *
import tkinter.messagebox





class LevelManager(Tk):


    def __init__(self):
        super().__init__()

        self.title("Level Manager")
        
        self.path = "."
        self.tree = None
        self.openned = []

        with open( join(self.path, "data", "wmap.json"), 'r', encoding = "UTF-8") as f:
            self.wmap = json.load(f)

        with open(join(self.path, "local", "prog.json"), 'r', encoding = "UTF-8") as f:
            self.prog = json.load(f)

        self.create_menu_bar()


    def create_menu_bar(self):
        menu_bar = Menu(self)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Nouveau chapitre", command=self.nouveau_chapitre)
        menu_file.add_command(label="Nouveau niveau", command=self.nouveau_niveau)
        menu_file.add_command(label="Modifier selection", command=self.set_selection)
        menu_file.add_separator()
        menu_file.add_command(label="Sauvegarder", command=self.save)
        menu_file.add_separator()
        menu_file.add_command(label="Quitter", command=self.quit)

        menu_arb = Menu(menu_bar, tearoff=0)
        menu_arb.add_command(label = "Sauvegarder", command = self.save)
        menu_arb.add_command(label = "Purger", command = self.purger)
        menu_arb.add_command(label = "Ajouter", command = self.add_files)

        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="About", command=self.do_something)

        menu_bar.add_cascade(label="Fichiers", menu=menu_file)
        menu_bar.add_cascade(label = "Arborescence", menu = menu_arb)
        menu_bar.add_cascade(label="Help", menu=menu_help)

        self.config(menu=menu_bar)



        


    def do_something(self):
        print("Menu clicked")



    def set_selection(self):
        for s in self.tree.selection():
            if s not in self.openned:
                if "/" in s :
                    chap, ex = s.split("/")
                    LC = LevelCreator(self, chap, ex)

    def nouveau_chapitre(self):
        LC = ChapterCreator(self, "")

    def nouveau_niveau(self):
        if len(self.tree.selection()) == 0:
            tkinter.messagebox.showerror("Erreur création niveau", "Veuillez sélectionner un chapitre.")
        else:
            for s in self.tree.selection():
                if '/' in s: 
                    chap, _ = s.split('/')
                    break
                else:
                    chap = s
            LC = LevelCreator(self, chap, "")



    def purger(self):
        """ Supprime les dossiers et fichiers obsolètes de l'arborscence."""

        for file in listdir(join(self.path, "data")):

            if file not in self.wmap and file != "wmap.json":

                if isdir(join(self.path, "data", file)): 
                    print(f'Suppression du dossier "data/{file}".')
                    shutil.rmtree(join(self.path, "data", file))
                    
                else:
                    print(f'Suppression du fichier "data/{file}".')
                    remove(join(self.path, "data", file))

            elif isdir(join(self.path, "data", file)):

                for f in listdir(join(self.path, "data", file)):
                    if f not in self.wmap[file]["cmap"]:
                        
                        if isdir(join(self.path, "data", file, f)):
                            print(f'Suppression du dossier "data/{file}/{f}".') 
                            shutil.rmtree(join(self.path, "data", file, f))
                        else:
                            print(f'Suppression du fichier "data/{file}/{f}".')
                            remove(join(self.path, "data", file, f))

                    else: 

                        for ff in listdir(join(self.path, "data", file, f)):
                            if ff not in ["enonce.txt", "test.txt"]:

                                if isdir(join(self.path, "data", file, f, ff)):
                                    print(f'Suppression du dossier "data/{file}/{f}/{ff}".') 
                                    shutil.rmtree(join(self.path, "data", file, f, ff))

                                else:
                                    print(f'Suppression du fichier "data/{file}/{f}/{ff}".')
                                    remove(join(self.path, "data", file, f, ff))
        self.reload_tree()



    def add_files(self):
        """Ajoute les dossiers et fichiers maquants à l'arborescence."""

        for chap in self.wmap :

            # Dossier data 
            if chap not in listdir(join(self.path, "data")):

                print(f'Ajout du dossier "data/{chap}".') 
                mkdir(join(self.path, "data", chap))

            for ex in self.wmap[chap]["cmap"]:

                if ex not in listdir(join(self.path, "data", chap)):
                    print(f'Ajout du dossier "data/{chap}/{ex}".') 
                    mkdir(join(self.path, "data", chap, ex))

                if "enonce.txt" not in listdir(join(self.path, "data", chap, ex)):
                    print(f'Ajout du fichier "data/{chap}/{ex}/enonce.txt".') 
                    f = open(join(self.path, "data", chap, ex, "enonce.txt"), 'w', encoding="UTF-8")
                    f.close()

                if "test.txt" not in listdir(join(self.path, "data", chap, ex)):
                    print(f'Ajout du fichier "data/{chap}/{ex}/test.txt".') 
                    f = open(join(self.path, "data", chap, ex, "test.txt"), 'w', encoding="UTF-8")
                    f.close()

            # Dossier local
            if chap not in listdir(join(self.path, "local")):

                print(f'Ajout du dossier "local/{chap}".') 
                mkdir(join(self.path, "local", chap))

            for ex in self.wmap[chap]["cmap"]:

                if ex+".py" not in listdir(join(self.path, "local", chap)):
                    print(f'Ajout du fichier "local/{chap}/{ex}.py".') 
                    f = open(join(self.path, "local", chap, ex+".py"), 'w', encoding="UTF-8")
                    f.close()




                


    def save(self):
        with open(join(self.path, "data", "wmap.json"), 'w', encoding = "UTF-8") as f:
            json.dump(self.wmap, f, indent = 4)
        with open(join(self.path, "local", "prog.json"), 'w', encoding = "UTF-8") as f:
            json.dump(self.prog, f, indent = 4)
        self.add_files()
        self.purger()
        self.reload_tree()
        print("Arboréscence mise à jour !")
            

    def remove_selection(self):

        for s in self.tree.selection():
            if '/' in s:
                chap, niv = s.split("/")

                if niv in self.wmap[chap]["cmap"]:
                    del(self.wmap[chap]["cmap"][niv])
                if niv in self.prog["niv"][chap]:
                    del(self.prog["niv"][chap][niv])

                for ex in self.wmap[chap]["cmap"]:
                    if niv in self.wmap[chap]["cmap"][ex]["link"] : 
                        self.wmap[chap]["cmap"][ex]["link"].remove(niv)
                    


        for s in self.tree.selection():
            if '/' not in s:
                chap = s
                if chap in self.wmap:
                    del(self.wmap[chap])
                for ch in self.wmap:
                    if chap in self.wmap[ch]["link"]:
                        self.wmap[ch]["link"].remove(chap)
                    if chap in self.prog["niv"]:
                        del(self.prog["niv"][chap])

        self.save()
        
        



    def reload_tree(self):
        self.tree.destroy()
        self.show_info()


    def show_info(self):
        self.tree = ttk.Treeview(self)
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


        self.tree.bind('<Double-Button-1>', lambda e: self.set_selection())
        self.tree.bind('<Delete>', lambda e: self.remove_selection())

        self.tree.grid()

        
        
        




class TToplevel(Toplevel):
    def __init__(self, master, name, **kwargs) -> None:
        assert name not in master.openned
        master.openned.append(name)
        super().__init__(master, **kwargs)
        self.name = name
        

    def destroy(self) -> None:
        if self.name in self.master.openned:
            self.master.openned.remove(self.name)
        return super().destroy()



class LevelCreator():

    def __init__(self, root, chap, ex = ""):
        """ Classe servant à créer un niveau.
        --- root : le tk parent.
        --- chap : le chapitre du niveau. 
        --- ex : le nom du niveau ("" pour nouveau).
        """

        # Nouveau niveau ou édition d'un niveau existant
        set = (ex!="") 

        # Vérifications
        assert chap in root.wmap
        if set:
            assert ex in root.wmap[chap]["cmap"]

        # Attributs simples
        self.ex = ex
        self.chap = chap

        # Fenêtres 
        self.root = root
        self.top = TToplevel(root, chap+'/'+ex)

        # Widgets
        self.enonce = Text(self.top, width=50, height=30, wrap="word")
        self.test = Text(self.top, width=50, height=30)

        self.nom = Entry(self.top)
        self.desc = Entry(self.top)
        self.x = Entry(self.top)
        self.y = Entry(self.top)
        self.r = Entry(self.top)

        liste_niv = list(self.root.wmap[chap]["cmap"])
        self.locked = ttk.Combobox(self.top, values = ["Oui", "Non"])
        self.linked = ttk.Combobox(self.top, values = liste_niv)

        if set:
            # Données à charger si le niveau est édité
            with open(join(".", "data", chap, ex, "enonce.txt"), 'r', encoding="UTF-8") as f:
                enonce = f.readlines()
                for s in enonce:
                    self.enonce.insert(END, s)

            with open(join(".", "data", chap, ex, "test.txt"), 'r', encoding="UTF-8") as f:
                test = f.readlines()
                for s in test:
                    self.test.insert(END, s)


            self.nom.insert(END, self.ex)
            self.nom.config(state="disabled")

            self.desc.insert(END, self.root.wmap[chap]["cmap"][ex]["description"])
            self.x.insert(END, self.root.wmap[chap]["cmap"][ex]["x"])
            self.y.insert(END, self.root.wmap[chap]["cmap"][ex]["y"])
            self.r.insert(END, self.root.wmap[chap]["cmap"][ex]["r"])

            if self.root.wmap[chap]["cmap"][ex]["locked"]:
                self.locked.current(0)
            else:
                self.locked.current(1)

            for i in range(len(liste_niv)):
                if ex in root.wmap[chap]["cmap"][liste_niv[i]]["link"]:
                    self.linked.current(i)
                    break
        
    
        else :
            # Préremplissage si c'est un nouveau niveau
            self.test.insert(END, "TYPE : \nSIGN : \nCTXT : \nDATA :")


        ### GRID

        # Ligne 1
        Label(self.top, text = "enoncé").grid(row = 1, column = 1, columnspan=2)
        Label(self.top, text = "test").grid(row = 1, column = 3, columnspan=2)

        # Ligne 2
        self.enonce.grid(row = 2, column=1, columnspan=2)
        self.test.grid(row = 2, column=3, columnspan=2)

        # Ligne 3+

        self.nom.grid(row = 3, column = 2, sticky= W)
        self.desc.grid(row = 4 , column = 2, sticky= W)
        self.locked.grid(row =5 , column = 2, sticky= W)
        self.linked.grid(row = 6, column = 2, sticky= W)

        self.x.grid(row = 3, column = 4, sticky= W)
        self.y.grid(row = 4, column = 4, sticky= W)
        self.r.grid(row = 5, column = 4, sticky= W)  

        Label(self.top, text = "Nom : ").grid(column = 1, row = 3, sticky= E)
        Label(self.top, text = "Description :").grid(column = 1, row = 4, sticky= E)
        Label(self.top, text = "Vérouillé :").grid(column = 1, row = 5, sticky= E)
        Label(self.top, text = "Niveau précédent").grid(column = 1, row = 6, sticky= E)

        Label(self.top, text = "x :").grid(column = 3, row = 3, sticky= E)
        Label(self.top, text = "y :").grid(column = 3, row = 4, sticky= E)
        Label(self.top, text = "r :").grid(column = 3, row = 5, sticky= E)

        but = ttk.Button(self.top, text = "Valider", command = self.valider)
        but.grid(column = 3, row = 6, columnspan=2)
            






    def valider(self):
        """ Récupère et sauvegarde le nouveau niveau / le nouveau chapitre."""
        try :
        
            # On vérifie que tous les champs ont été remplis
            assert self.locked.get() != ""
            assert self.desc.get() != ""
            assert self.locked.get() != ""
            assert self.x.get() != ""
            assert self.y.get() != ""
            assert self.r.get() != ""

            # Mise à jour de la wmap du LM
            self.root.wmap[self.chap]["cmap"][self.nom.get()] = {
                "nom": self.nom.get(),
                "description" : self.desc.get(),
                "locked": False,
                "x": int(self.x.get()),
                "y": int(self.y.get()),
                "r": int(self.r.get()),
                "link": []
            }
            self.root.prog["niv"][self.chap][self.nom.get()] = {
                "locked" : False,
                "done" : False
            }
            if self.locked.get() == "Oui":
                self.root.wmap[self.chap]["cmap"][self.nom.get()]["locked"] = True
                self.root.prog["niv"][self.nom.get()]["locked"] = True 

            if self.linked.get() != "":
                self.root.wmap[self.chap]["cmap"][self.linked.get()]["link"].append(self.nom.get())
                self.root.wmap[self.chap]["cmap"][self.linked.get()]["link"] = sans_doublon(self.root.wmap[self.chap]["cmap"][self.linked.get()]["link"])

            # Mise à jour du fichier wmap
            self.root.save()
            self.root.add_files()

            # Mise à jour des fichiers ennoncé et test
            self.ex = self.nom.get()
            with open(join(".", "data", self.chap, self.ex, "enonce.txt"), 'w', encoding="UTF-8") as f:
                print(join(".", "data", self.chap, self.ex, "enonce.txt"))
                f.write(self.enonce.get("1.0", END))
            with open(join(".", "data", self.chap, self.ex, "test.txt"), 'w', encoding="UTF-8") as f:
                f.write(self.test.get("1.0", END))

            # Retour au treeview
            self.top.destroy()
            self.root.reload_tree()
            

        except AssertionError:
            tkinter.messagebox.showwarning(title="Erreur", message="Donnée manquante")



class ChapterCreator():

    def __init__(self, root, chap = ""):
        """ Classe servant à créer un chapitre.
        --- root : le tk parent.
        --- chap : le chapitre du niveau ("" pour nouveau).
        """

        # Nouveau niveau ou édition d'un niveau existant
        set = (chap!="") 

        # Vérifications
        if set:
            assert chap in root.wmap

        # Attributs simples
        self.chap = chap

        # Fenêtres 
        self.root = root
        self.top = TToplevel(root, chap)

        # Widgets
        self.nom = Entry(self.top)
        self.desc = Entry(self.top)
        self.x = Entry(self.top)
        self.y = Entry(self.top)
        self.r = Entry(self.top)

        liste_chap = list(self.root.wmap.keys())

        self.locked = ttk.Combobox(self.top, values = ["Oui", "Non"])
        self.linked = ttk.Combobox(self.top, values = liste_chap)

        if set:
            self.nom.insert(END, self.chap)
            self.nom.config(state="disabled")

            self.desc.insert(END, self.root.wmap[chap]["description"])
            self.x.insert(END, self.root.wmap[chap]["x"])
            self.y.insert(END, self.root.wmap[chap]["y"])
            self.r.insert(END, self.root.wmap[chap]["r"])

            if self.root.wmap[chap]["locked"]:
                self.locked.current(0)
            else:
                self.locked.current(1)

            for i in range(len(liste_chap)):

                if chap in root.wmap[liste_chap[i]]["link"]:
                    self.linked.current(i)
                    break
        


        ### GRID


        # Ligne 3+

        self.nom.grid(row = 3, column = 2, sticky= W)
        self.desc.grid(row = 4 , column = 2, sticky= W)
        self.locked.grid(row =5 , column = 2, sticky= W)
        self.linked.grid(row = 6, column = 2, sticky= W)

        self.x.grid(row = 3, column = 4, sticky= W)
        self.y.grid(row = 4, column = 4, sticky= W)
        self.r.grid(row = 5, column = 4, sticky= W)  

        Label(self.top, text = "Nom : ").grid(column = 1, row = 3, sticky= E)
        Label(self.top, text = "Description :").grid(column = 1, row = 4, sticky= E)
        Label(self.top, text = "Vérouillé :").grid(column = 1, row = 5, sticky= E)
        Label(self.top, text = "Chapitre précédent").grid(column = 1, row = 6, sticky= E)

        Label(self.top, text = "x :").grid(column = 3, row = 3, sticky= E)
        Label(self.top, text = "y :").grid(column = 3, row = 4, sticky= E)
        Label(self.top, text = "r :").grid(column = 3, row = 5, sticky= E)

        but = ttk.Button(self.top, text = "Valider", command = self.valider)
        but.grid(column = 3, row = 6, columnspan=2)
            






    def valider(self):
        """ Récupère et sauvegarde le nouveau niveau / le nouveau chapitre."""
        try :
        
            # On vérifie que tous les champs ont été remplis
            assert self.locked.get() != ""
            assert self.desc.get() != ""
            assert self.locked.get() != ""
            assert self.x.get() != ""
            assert self.y.get() != ""
            assert self.r.get() != ""

            # Mise à jour de la wmap du LM
            self.chap =  self.nom.get()
            link = []
            cmap = {}
            if self.chap in self.root.wmap:
                link = self.root.wmap[self.chap]["link"]
                cmap = self.root.wmap[self.chap]["cmap"]

            self.root.wmap[self.chap] = {
                "nom": self.chap,
                "description" : self.desc.get(),
                "locked": False,
                "x": int(self.x.get()),
                "y": int(self.y.get()),
                "r": int(self.r.get()),
                "link" : link,
                "cmap" : cmap
            }
            self.root.prog["self.chap"] = {}
            if self.locked.get() == "Oui":
                self.root.wmap[self.chap]["locked"] = True

            if self.linked.get() != "":
                self.root.wmap[self.linked.get()]["link"].append(self.chap)
                self.root.wmap[self.linked.get()]["link"] = sans_doublon(self.root.wmap[self.linked.get()]["link"])

            # Mise à jour du fichier wmap
            self.root.save()

            # Retour au treeview
            self.top.destroy()
            self.root.reload_tree()
            

        except AssertionError:
            tkinter.messagebox.showwarning(title="Erreur", message="Donnée manquante")






def sans_doublon(t):
    return list(set(t))
 
LM = LevelManager()         
LM.show_info()


LM.mainloop()


"""
LM.save()

LM.show_info()

LM.mainloop()
"""