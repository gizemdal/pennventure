# Tkinter test
try:
    import tkinter
    from tkinter import *
except ImportError:
    from Tkinter import *
    import Tkinter as tkinter

def clicked():
    res = 'Hello ' + txt.get()
    lbl.configure(text=res)

window = Tk()
window.title("Welcome to Pennventure")
window.geometry('350x200')
lbl = Label(window, text='Hello')
lbl.grid(column=0, row=0)
txt = Entry(window, width=20)
txt.grid(column=0, row=1)
btn = Button(window, text='click me', command=clicked)
btn.grid(column=1, row=0)
window.mainloop()
