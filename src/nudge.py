#this class helsp us move the plotter manually, ie zero it out
from tkinter import *
import json
import re
from tkhelpers import dialog
from vector import vector3

class nudge(dialog):

    def __init__(self,parent,callback,onclose,title = None):

        self.value_element = None # these are the tkinter elements that are made
        self.value_variable = StringVar() # these are the tkinter variables that are made

        self.callback = callback
        self.onclose = onclose

        dialog.__init__(self, parent, "nudge", False)

    def body(self, master):

        box = Frame(self)

        w = Button(box, text="Y", width=4, command=lambda: self.apply(vector3(0.0,1.0,0.0)), default=ACTIVE)
        w.grid(row=0,column=0)
        w = Button(box, text="-Y", width=4, command=lambda: self.apply(vector3(0.0,-1.0,0.0)), default=ACTIVE)
        w.grid(row=1,column=0)

        w = Button(box, text="-X", width=4, command=lambda: self.apply(vector3(-1.0,0.0,0.0)), default=ACTIVE)
        w.grid(row=2,column=1)
        w = Button(box, text="X", width=4, command=lambda: self.apply(vector3(1.0,0.0,0.0)))
        w.grid(row=2,column=2)
        
        w = Button(box, text="Z", width=4, command=lambda: self.apply(vector3(0.0,0.0,1.0)), default=ACTIVE)
        w.grid(row=0,column=2)
        w = Button(box, text="-Z", width=4, command=lambda: self.apply(vector3(0.0,0.0,-1.0)))
        w.grid(row=1,column=1)

        self.value_variable.set("1.0")
        self.value_element = Entry(box,textvariable = self.value_variable,width=4)
        self.value_element.grid(row=2,column=0)

        box.pack()

        self.bind("<Escape>", self.cancel)


    def apply(self,direction):
        
        direction *= float(re.findall('\d+', self.value_variable.get() )[0])
        self.callback(direction)
        #print("nudge this"+direction.printable())
        # first = int(self.value_variable.get())
        # second = int(self.e2.get())
        # print(first) 
        # print(second) # or something

    def cancel(self, event=None):
        self.onclose()
        dialog.cancel(self,event)
