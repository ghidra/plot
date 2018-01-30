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

		self.copies = 8

		self.load_asset("dodecahedron")
		self.setup({"rx":4.0,"ry":4.0,"rz":4.0})
		self.render()
	
	def setup(self,payload={}):
		super().setup(payload);

		self.attributes["copies"] = payload["copies"] if "copies" in payload else self.copies
		self.copies = self.attributes["copies"]
		self.attributes["rx"] = payload["rx"] if "rx" in payload else 4.0
		self.attributes["ry"] = payload["ry"] if "ry" in payload else 4.0
		self.attributes["rz"] = payload["rz"] if "rz" in payload else 4.0

		self.assets = self.assets[:1]

		for i in range(self.copies-1):
			self.assets.append(dict(self.assets[0]))
		
		for i in range(self.copies):
			self.assets[i]["rnm"] = matrix4()
			self.assets[i]["rnm"] = self.assets[i]["rnm"].scale_uniform( 1.0-(i/self.copies) ).rotate_x(float(i+1)*self.attributes["rx"]).rotate_y(float(i+1)*self.attributes["ry"]).rotate_z(float(i+1)*self.attributes["rz"])#.rotate_y(i*2.0)


	def configure(self,tk,canvas,segmentBuffer):
		self.canvas=canvas
		c = configure_artist(tk,self.attributes,self.configure_callback)


#---------------------
#  settings
#---------------------
from tkinter import *
from artist3 import artist3_dialog

class configure_artist(artist3_dialog):
	#def __init__(self,parent,callback):

	#	dialog.__init__(self, parent, "artist settings",buttonBoxType=1,applyCallback=callback)

	def body(self, master):
		super().body(master)

		group = LabelFrame(self.mainframe, text="Artist Settings", padx=1, pady=1)
		group.grid(row=1, padx=1, pady=1)

		Label(group, text="copies:").grid(row=0)
		self.v["copies"] = IntVar()
		self.v["copies"].set( self.attributes["copies"] if "copies" in self.attributes else 0 )
		self.e["copies"] = Scale(group,variable = self.v["copies"],orient=HORIZONTAL, from_=1, to=32,resolution=1.0)
		self.e["copies"].grid(row=0,column=1)

		Label(group, text="rotation x:").grid(row=1)
		self.v["rx"] = DoubleVar()
		self.v["rx"].set( self.attributes["rx"] if "rx" in self.attributes else 0.0 )
		self.e["rx"] = Scale(group,variable = self.v["rx"],orient=HORIZONTAL, from_=0, to=10,resolution=0.01)
		self.e["rx"].grid(row=1,column=1)

		Label(group, text="rotation y:").grid(row=2)
		self.v["ry"] = DoubleVar()
		self.v["ry"].set( self.attributes["ry"] if "ry" in self.attributes else 0.0 )
		self.e["ry"] = Scale(group,variable = self.v["ry"],orient=HORIZONTAL, from_=0, to=10,resolution=0.01)
		self.e["ry"].grid(row=2,column=1)

		Label(group, text="rotation z:").grid(row=3)
		self.v["rz"] = DoubleVar()
		self.v["rz"].set( self.attributes["rz"] if "rz" in self.attributes else 0.0 )
		self.e["rz"] = Scale(group,variable = self.v["rz"],orient=HORIZONTAL, from_=0, to=10,resolution=0.01)
		self.e["rz"].grid(row=3,column=1)