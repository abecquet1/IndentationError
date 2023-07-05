from tkinter import *
from tkinter import ttk
from random import choice


class LabeledEntry():
    def __init__(self, parent, **kwargs):
        self.frame = Frame(parent)
        self.entry = Entry(self.frame)
        self.label = Label(self.frame, text = kwargs.get('text', ""))
        
    def grid(self, *args, **kwargs): 
        self.frame.grid(*args, **kwargs)
        self.label.grid(row = 1, column = 1, sticky = E)
        self.entry.grid(row = 1, column = 2, sticky = W)


        

class LevelCreator(Tk):
    def __init__(self):
        super().__init__()

        # Fenetre
        self.title("Créateur de niveau")

        # Widgets
        self.enonce = Text(self, width=50, height=30)
        self.test = Text(self, width=50, height=30)
        self.chap = LabeledEntry(self, text = "Chapitre :")
        self.nom = LabeledEntry(self, text = "Nom :")

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


    def save(self):
        pass


test = Tk()
tree = ttk.Treeview(test)
tree['columns'] = ('nb_ex', 'type')
tree.column('nb_ex', anchor='center')
tree.column('type', anchor='center')



tree.heading('nb_ex', text='nombre exercices')
tree.heading('type', text='type')



for i in range(1,9):
    tree.insert('', 'end', f'p{i}', text=f'p{i}')
    tree.set(f'p{i}', 'nb_ex', '3')

    for j in range(1,4):
        tree.insert(f'p{i}', 'end', f'p_{i}/ex{j}', text=f'ex{j}')
        tree.set(f'p_{i}/ex{j}', 'type', choice(["CCC", "FAO", "CCC", "FCC", "FAR"]))

    
tree.grid(row = 1, column = 1, columnspan= 5)





test.mainloop()



