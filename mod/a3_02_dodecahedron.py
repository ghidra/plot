import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist3 import artist3
from segment import segment
from vector import *
from matrix import *

class a3_02_dodecahedron(artist3):
	def __init__(self,dimensions,skateheight):
		super().__init__(dimensions,skateheight)

		self.copies = 22

		self.rnm = matrix4()
		self.rnm = self.rnm.translate( vector3(0.0,0.0,-2.0) )

		self.load_asset("dodecahedron")

		#now duplicate the asset a bunch
		for i in range(self.copies-1):
			self.assets.append(dict(self.assets[0]))
		
		self.setup({"rx":4.0,"ry":4.0,"rz":4.0})
		
		self.render()
	
	# def update(self):
	# 	super().update()
	# 	return self.dispatch()
	def setup(self,payload):
		for i in range(self.copies):
			self.assets[i]["rnm"] = matrix4()
			self.assets[i]["rnm"] = self.assets[i]["rnm"].scale_uniform( 1.0-(i/self.copies) ).rotate_x(float(i+1)*payload["rx"]).rotate_x(float(i+1)*payload["ry"]).rotate_x(float(i+1)*payload["rz"])#.rotate_y(i*2.0)


	def configure(self,tk,canvas):
		self.canvas=canvas
		c = configure_artist(tk,self.configure_callback)


	def configure_callback(self,payload):
		self.canvas.delete("artist")
		self.setup(payload)
		self.render()
		self.flashed=False


#---------------------
#  settings
#---------------------
from tkinter import *
from tkhelpers import dialog

class configure_artist(dialog):
	def __init__(self,parent,callback):

		self.callback=callback

		self.e = {} # these are the tkinter elements that are made
		self.v = {} # these are the tkinter variables that are made
		self.payload = {}

		dialog.__init__(self, parent, "artist settings")

	def body(self, master):


		Label(master, text="rotation x:").grid(row=0)
		self.v["rx"] = DoubleVar()
		self.v["rx"].set(0)
		self.e["rx"] = Scale(master,variable = self.v["rx"],orient=HORIZONTAL, from_=0, to=360,resolution=0.1)
		self.e["rx"].grid(row=0,column=1)

		Label(master, text="rotation y:").grid(row=1)
		self.v["ry"] = DoubleVar()
		self.v["ry"].set(0)
		self.e["ry"] = Scale(master,variable = self.v["ry"],orient=HORIZONTAL, from_=0, to=360,resolution=0.1)
		self.e["ry"].grid(row=1,column=1)

		Label(master, text="rotation z:").grid(row=2)
		self.v["rz"] = DoubleVar()
		self.v["rz"].set(0)
		self.e["rz"] = Scale(master,variable = self.v["rz"],orient=HORIZONTAL, from_=0, to=360,resolution=0.1)
		self.e["rz"].grid(row=2,column=1)

	def buttonbox(self):
		box = Frame(self)
		w = Button(box, text="Apply", width=10, command=self.apply, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		w = Button(box, text="OK", width=10, command=self.ok)
		w.pack(side=LEFT, padx=5, pady=5)

		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()

	def apply(self):
		for v in self.v:
			self.payload[v]=self.v[v].get()
		self.callback(self.payload)

		pass