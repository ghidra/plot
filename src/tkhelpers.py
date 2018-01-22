#tkinter helper classes
import os
from tkinter import *

# class popup():
#     def __init__(self,tk):
#         self.menu = Menu(tk, tearoff=0)
#         self.menu.add_command(label="Undo", command=self.hello)
#         self.menu.add_command(label="Redo", command=self.hello)

#     def hello(self):
#         print("I was touched, deeply")

#     def post(self):
#         self.menu.post(200,200)

#-------------------------------

class dialog(Toplevel):
    def __init__(self,parent,title = None,buttonBox =True,buttonBoxType = 0,applyCallback=None,cancelCallback=None):
        Toplevel.__init__(self, parent)

        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        #self.result = None
        self.e = {} # these are the tkinter elements that are made
        self.v = {} # these are the tkinter variables that are made
        self.payload = {}

        self.callback = applyCallback
        self.onclose = cancelCallback

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)
        if buttonBox:
            self.buttonbox(buttonBoxType)

        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self,type=0):
        # add standard button box. override if you don't want the

        box = Frame(self)

        if type==0:

            w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
            w.pack(side=LEFT, padx=5, pady=5)
            w = Button(box, text="Cancel", width=10, command=self.cancel)
            w.pack(side=LEFT, padx=5, pady=5)

        elif type==1:

            w = Button(box, text="Apply", width=10, command=self.apply, default=ACTIVE)
            w.pack(side=LEFT, padx=5, pady=5)
            w = Button(box, text="OK", width=10, command=self.ok)
            w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #------------------------------------------
    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def apply(self):
        for v in self.v:
            self.payload[v]=self.v[v].get()
        if self.callback is not None:
            self.callback(self.payload)

    def cancel(self, event=None):
        if self.onclose is not None:
            self.onclose()
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #------------------------------------------

    def validate(self):
        return 1 # override

    #UTILITY FUNCTION

    #loops the folder to find what we want to populate the drop down with
    def gatherFiles(self,directory,extension=".json"):
        tmp = []
        for filename in os.listdir(directory):
            if filename.endswith(extension): 
                tmp.append(filename)
        return tmp

    #when a file is choosen from the drop down, we can load it i guess
    def optionPicked(self,*args):
        #print("-----"+self.v["file"].get())
        pass

    #this will update a options menu, it needs
    #the option menu you want to update
    #the options
    #and the string var that holds the selected value
    def updateOptionsMenu(self,optionMenu,options,stringVar):
        menu = optionMenu["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string, command=lambda value=string: stringVar.set(value))

        