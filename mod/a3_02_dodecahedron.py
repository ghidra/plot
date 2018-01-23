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
		if "copies" in payload:
			self.copies = payload["copies"]
			self.assets = self.assets[:1]
			for i in range(self.copies-1):
				self.assets.append(dict(self.assets[0]))
			#we need to clear this out and re render it
		for i in range(self.copies):
			self.assets[i]["rnm"] = matrix4()
			self.assets[i]["rnm"] = self.assets[i]["rnm"].scale_uniform( 1.0-(i/self.copies) ).rotate_x(float(i+1)*payload["rx"]).rotate_y(float(i+1)*payload["ry"]).rotate_z(float(i+1)*payload["rz"])#.rotate_y(i*2.0)


	def configure(self,tk,canvas):
		self.canvas=canvas
		c = configure_artist(tk,{"copies":self.copies},self.configure_callback)


	def configure_callback(self,payload):
		self.canvas.delete("artist")
		self.segment_count=0
		self.setup(payload)
		self.render()
		self.flashed=False


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

		group = LabelFrame(master, text="Artist Settings", padx=1, pady=1)
		group.grid(row=1, padx=1, pady=1)

		Label(group, text="copies:").grid(row=0)
		self.v["copies"] = IntVar()
		self.v["copies"].set(self.attributes["copies"])
		self.e["copies"] = Scale(group,variable = self.v["copies"],orient=HORIZONTAL, from_=1, to=32,resolution=1.0)
		self.e["copies"].grid(row=0,column=1)

		Label(group, text="rotation x:").grid(row=1)
		self.v["rx"] = DoubleVar()
		self.v["rx"].set(0)
		self.e["rx"] = Scale(group,variable = self.v["rx"],orient=HORIZONTAL, from_=0, to=10,resolution=0.01)
		self.e["rx"].grid(row=1,column=1)

		Label(group, text="rotation y:").grid(row=2)
		self.v["ry"] = DoubleVar()
		self.v["ry"].set(0)
		self.e["ry"] = Scale(group,variable = self.v["ry"],orient=HORIZONTAL, from_=0, to=10,resolution=0.01)
		self.e["ry"].grid(row=2,column=1)

		Label(group, text="rotation z:").grid(row=3)
		self.v["rz"] = DoubleVar()
		self.v["rz"].set(0)
		self.e["rz"] = Scale(group,variable = self.v["rz"],orient=HORIZONTAL, from_=0, to=10,resolution=0.01)
		self.e["rz"].grid(row=3,column=1)