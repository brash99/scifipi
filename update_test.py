from tkinter import *
import tkinter as tk
from time import sleep

#main = tkinter.Tk()
#txt = tkinter.Text(main)
#txt.grid()

root = tk.Tk()
var = IntVar()

class Application(tk.Frame):

    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):

        self.txt = tk.Text(self)

    def update_txt(self, event = None):
        vals = ['This is some text.','This is some more.','Blah blah blah']
        i=0
        while i < len(vals):
            self.txt.delete('1.0','end')
            self.txt.insert('1.0',vals[i])
            self.txt.update_idletasks()
            sleep(2)
            i=i+1
            i = i % 3

root.title("Update Test")
root.geometry("250x400")
app = Application(master=root)
#app.after(1000,update_txt)
app.mainloop()
