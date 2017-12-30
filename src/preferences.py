#programs preference dialog
from tkinter import *
import json
from tkhelpers import dialog

class preferences(dialog):

    def __init__(self,parent,title = None,file=None):

        self.file = file
        self.e = {} # these are the tkinter elements that are made
        self.v = {} # these are the tkinter variables that are made

        dialog.__init__(self, parent, "plot preferences")

    def body(self, master):

        if self.file:
            configure_file = open(self.file,'r')
            configure_data = json.loads(configure_file.read())

            counter=0
            for pref in configure_data:
                
                Label(master, text=pref+":").grid(row=counter)

                if type( configure_data[pref] ) is str:
                    self.v[pref] = StringVar()
                    self.v[pref].set(configure_data[pref])
                    self.e[pref] = Entry(master,textvariable = self.v[pref])
                elif type( configure_data[pref] ) is bool:
                    self.v[pref] = IntVar()
                    self.v[pref].set(configure_data[pref])
                    self.e[pref] = Checkbutton(master,variable = self.v[pref])
                elif type( configure_data[pref] ) is int:
                    self.v[pref] = IntVar()
                    self.v[pref].set(configure_data[pref])
                    min_ = configure_data[pref]-(configure_data[pref]*0.5)
                    max_ = configure_data[pref]+(configure_data[pref]*0.5)
                    self.e[pref] = Scale(master,variable = self.v[pref],orient=HORIZONTAL, from_=min_, to=max_)
                elif type( configure_data[pref] ) is float:
                    self.v[pref] = DoubleVar()
                    self.v[pref].set(configure_data[pref])
                    min_ = configure_data[pref]-(configure_data[pref]*0.5)
                    max_ = configure_data[pref]+(configure_data[pref]*0.5) if pref != "artist_delay" else 1.0
                    self.e[pref] = Scale(master,variable = self.v[pref],orient=HORIZONTAL, from_=min_, to=max_,resolution=0.001)

                self.e[pref].grid(row=counter,column=1)
                counter += 1

        # return self.e1 # initial focus

    def apply(self):
        # first = int(self.e1.get())
        # second = int(self.e2.get())
        # print(first) 
        # print(second) # or something
        pass