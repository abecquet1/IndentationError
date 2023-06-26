from tkinter import *

def contextFrame(t, root, w, h, event):
    win = Toplevel(root)
    #win.geometry(f"500x500+{root.winfo_x()+event.x}+{root.winfo_y()+event.y}")
    win.overrideredirect(1)

    x = win.winfo_x()
    y = win.winfo_y()
    win.geometry("+%d+%d" %(x + root.winfo_pointerx()-390, y + root.winfo_pointery()-10))
    
    text = Text(win, width = w, height = h, wrap = WORD, bg ="black", fg = "white")
    text.insert(END, t)
    text.config( state = "disabled")
    text.grid()
    win.bind('<Leave>', lambda e: win.destroy())
    win.mainloop()


