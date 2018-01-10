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

		#self.sequential = True
		self.copies = 4
		#self.copy_counter = 0

		self.rnm = matrix4()
		self.rnm = self.rnm.translate( vector3(0.0,0.0,-2.0) )

		self.load_asset("dodecahedron")

		#now duplicate the asset a bunch
		for i in range(self.copies-1):
			self.assets.append(dict(self.assets[0]))
			#make the transform modifications now
			self.assets[i+1]["rnm"] = self.assets[i+1]["rnm"].scale_uniform( 1.0-(i/self.copies) ).rotate_x(i*4.0)#.rotate_y(i*2.0)
		
		self.render()
	
	def update(self):
		super().update()

		# if self.copy_counter <= self.copies:
		# 	self.assets[0]["rnm"] = matrix4()
		# 	self.assets[0]["rnm"] = self.assets[0]["rnm"].scale_uniform( 1.0-(self.copy_counter/self.copies) ).rotate_x(self.copy_counter*2.0).rotate_y(self.copy_counter*2.0)
		# 	self.copy_counter += 1
		# 	#self.assets[0]["rnm"] = self.assets[0]["rnm"].translate( vector3(0.0,self.copy_counter*0.01,0.0) )
		# else:
		# 	self.sequential = False

		return self.dispatch()

	def configure(self,tk):
		c = configure_artist(tk)
		print("update settings")


#---------------------
#  settings
#---------------------
from tkinter import *
from tkhelpers import dialog

class configure_artist(dialog):
	def __init__(self,parent):

		self.e = {} # these are the tkinter elements that are made
		self.v = {} # these are the tkinter variables that are made

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
		# first = int(self.e1.get())
		# second = int(self.e2.get())
		print("lets try to apply these")
		pass