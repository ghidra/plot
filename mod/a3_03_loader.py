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

		self.directory = "" #to make sure that we load this these are empty, and we senf them in setup
		self.filename = ""
		self.segmentBuffer = None

		self.setup( {"path":"mod/assets","file":"test_slice.json"} )	
		self.render()
		

	def load_asset(self,asset,explicit=False):
		del self.assets[:]
		del self.segment[:] #this isnt actually doing anything
		super().load_asset(asset,explicit)
		
	
	def setup(self,payload={}):
		super().setup(payload)

		self.attributes["path"] = payload["path"] if "path" in payload else self.directory
		self.attributes["file"] = payload["file"] if "file" in payload else self.filename
		self.attributes["rx"] = payload["rx"] if "rx" in payload else 0.0
		self.attributes["ry"] = payload["ry"] if "ry" in payload else 0.0
		self.attributes["rz"] = payload["rz"] if "rz" in payload else 0.0

		#make sure we only load once
		if(self.attributes["path"] != self.directory or self.attributes["file"] != self.filename):
			self.directory = self.attributes["path"]
			self.filename = self.attributes["file"]
			#this allows us to erase the segments that have already been sent to main.
			#but we dont have it if we start with this, so we have to wait till we have it
			if(self.segmentBuffer!=None):
				del self.segmentBuffer[:]
			self.load_asset(payload["path"]+"/"+payload["file"],True)

		self.assets[0]["rnm"] = matrix4()
		self.assets[0]["rnm"] = self.assets[0]["rnm"].rotate_x(self.attributes["rx"]).rotate_y(self.attributes["ry"]).rotate_z(self.attributes["rz"])#.rotate_y(i*2.0)


	def configure(self,tk,canvas,segmentBuffer):
		self.canvas=canvas
		self.segmentBuffer=segmentBuffer
		c = configure_artist(tk,self.attributes,self.configure_callback)


#---------------------
#  settings
#---------------------
from tkinter import *
from artist3 import artist3_dialog

class configure_artist(artist3_dialog):
	def __init__(self,parent,attributes,callback):

		self.directory=attributes["path"] #sp I can access it in change dir
		self.choices = []

		super().__init__( parent, attributes, callback)
		

	def body(self, master):
		super().body(master)

		group = LabelFrame(self.mainframe, text="Artist Settings", padx=1, pady=1)
		group.grid(row=1, padx=1, pady=1)

		#box = Frame(self)
		self.v["path"] = StringVar()
		self.v["path"].set(self.attributes["path"])# if "path" in self.attributes else 0)
		self.e["path"] = Entry(group,textvariable = self.v["path"], width=40)
		self.e["path"].grid(row=0,column=0)

		w = Button(group, text="Browse", width=10, command=self.changeDirectory, default=ACTIVE)
		w.grid(row=0,column=1)

		self.v["file"] = StringVar()
		self.choices = self.gatherFiles(self.attributes["path"])
		self.v["file"].set(self.choices[0])
		self.e["file"] = OptionMenu(group,self.v["file"], *self.choices )
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
