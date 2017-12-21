#programs preference dialog
from tkinter import *
from t import dialog

class preferences(dialog):

    def __init__(self,parent,title = None,file=None):
        dialog.__init__(self, parent, "plot preferences")

    def body(self, master):

        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        first = int(self.e1.get())
        second = int(self.e2.get())
        print(first) 
        print(second) # or something