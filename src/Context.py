from tkinter import *
from tkinter import ttk


def contextFrame(t, root, w, h, event):
    win = Toplevel(root)
    win.overrideredirect(1)

    x = win.winfo_x()
    y = win.winfo_y()
    win.geometry("+%d+%d" %(x + root.winfo_pointerx()-690, y + root.winfo_pointery()-20))

    border = ttk.Frame(win, style = 'context_border.TFrame')
    border.grid()

    text = Text(border, 
                width = w, 
                height = h, 
                wrap = WORD, 
                bg = root.style["context_bg"], 
                fg = root.style["context_fg"], 
                font = "courier 18",
)
    
    text.insert(END, t)
    text.config(state = "disabled")
    text.grid(padx = 2, pady = 2)
    win.bind('<Leave>', lambda e: win.destroy())
    win.mainloop()



def confirmation(text, root, command, condition = True):
    if condition:
        win = Toplevel(root)

        border = ttk.Frame(win, style = "context_border.TFrame")
        border.grid()
        frame = ttk.Frame(border, style = "context.TFrame")
        

        win.grid_columnconfigure(1, weight=1)
        win.grid_rowconfigure(1, weight=1)
        

        frame.grid(row = 1, column = 1, sticky = "NSEW", padx = 2, pady=2)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        win.overrideredirect(1)
        
        
        lab= ttk.Label(frame, text=text, style = 'context_clickable.TLabel')

        lab.grid(row = 1, column = 1, columnspan=2)

        def oui():
            win.destroy()
            command()
            
        b1= ttk.Label(frame, text="> Oui",   style = 'context_clickable.TLabel', padding=(2,2,2,2))
        b2= ttk.Label(frame, text="> Non",  style = 'context_clickable.TLabel', padding=(2,2,2,2))

        b1.grid(row = 2, column = 1)
        b2.grid(row = 2, column = 2)

        for child in frame.winfo_children(): 
                child.grid_configure(padx=10, pady=10)

        b1.bind('<1>', lambda e: oui())
        b2.bind('<1>', lambda e: win.destroy())

        b1.bind('<Enter>', lambda e: b1.config(style = 'context_hovered.TLabel'))
        b1.bind('<Leave>', lambda e: b1.config(style = 'context_clickable.TLabel'))

        b2.bind('<Enter>', lambda e: b2.config(style = 'context_hovered.TLabel'))
        b2.bind('<Leave>', lambda e: b2.config(style = 'context_clickable.TLabel'))
        
        win.bind('<Return>', lambda e: oui())
        win.bind('<Escape>', lambda e: win.destroy())

        win.focus_set()

        win.tk.call('tk::PlaceWindow', win)



    else:
        command()




    
    

