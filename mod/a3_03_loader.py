import os
import time
import platform
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist3 import artist3
from segment import segment
from vector import *
from matrix import *

class a3_03_loader(artist3):
	def __init__(self,dimensions,skateheight):
		super().__init__(dimensions,skateheight)

		self.rnm = matrix4()
		self.rnm = self.rnm.translate( vector3(0.0,0.0,-2.0) )

		#default directory setting
		if(platform.system() == "Windows"):
			self.directory="mod\\assets"
		else:
			self.directory="mod/assets"

		self.load_asset("test_slice")
		
		#self.setup()#{"rx":4.0,"ry":4.0,"rz":4.0})
		
		

	def load_asset(self,asset,explicit=False):
		del self.assets[:]
		super().load_asset(asset,explicit)
		self.render()
	
	def setup(self,payload):
		pass
		# for i in range(self.copies):
		# 	self.assets[i]["rnm"] = matrix4()
		# 	self.assets[i]["rnm"] = self.assets[i]["rnm"].scale_uniform( 1.0-(i/self.copies) ).rotate_x(float(i+1)*payload["rx"]).rotate_y(float(i+1)*payload["ry"]).rotate_z(float(i+1)*payload["rz"])#.rotate_y(i*2.0)


	def configure(self,tk,canvas):
		self.canvas=canvas
		c = configure_artist(tk,self.directory,self.configure_callback)


	def configure_callback(self,payload):
		self.canvas.delete("artist")
		self.segment_count=0
		#self.setup(payload)
		#self.render()
		self.load_asset(payload["path"]+"/"+payload["file"],True)
		self.flashed=False


#---------------------
#  settings
#---------------------
from tkinter import *
from tkinter import filedialog
from tkhelpers import dialog

class configure_artist(dialog):
	def __init__(self,parent,directory,callback):

		self.directory=directory
		self.choices = []

		dialog.__init__(self, parent, "artist settings", buttonBoxType=1,applyCallback=callback)
		

	def body(self, master):

		#box = Frame(self)
		self.v["path"] = StringVar()
		self.v["path"].set(self.directory)
		self.e["path"] = Entry(master,textvariable = self.v["path"], width=40)
		self.e["path"].grid(row=0,column=0)

		w = Button(master, text="Browse", width=10, command=self.changeDirectory, default=ACTIVE)
		w.grid(row=0,column=1)

		self.v["file"] = StringVar()
		self.choices = self.gatherFiles(self.directory)
		self.v["file"].set(self.choices[0])
		self.e["file"] = OptionMenu(master,self.v["file"], *self.choices )
		self.e["file"].grid(row=1,column=0)

		#this is strange, to get a callback on when the dropdown choce is made, this is how it is connected
		self.v["file"].trace('w', self.optionPicked)
		#loop currently set folder to get the files

	#-------------------------------------------------------------
	#CUSTOM methods to this --------------------------------------
	#button to change directoy was pressed, this throws up a file browser
	def changeDirectory(self):
		prev = self.directory
		self.directory = filedialog.askdirectory(initialdir = self.directory,title = "Select directory")
		#only proceed if we change the directory
		if prev != self.directory:
			self.choices = self.gatherFiles(self.directory)
			self.v["file"].set(self.choices[0])
			self.v["path"].set(self.directory)
			#this is a helper function to refil the dropdown menu
			self.updateOptionsMenu(self.e["file"],self.choices,self.v["file"])
