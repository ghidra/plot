import os
import platform

#this class id for dealing with the artist in the mod folder, and can load them from other folders too
class artist_loader():
	def __init__(self):

		self.directory="mod"
		self.list = {}
		self.names = self.findArtist()

		for a in self.names:
			m = __import__(a, fromlist=[a])
			self.list[a] = getattr(m, a)
			#print("imported artist: "+ a)

	def findArtist(self):
		tmp = []
		for filename in os.listdir(self.directory):
			if filename.endswith(".py"): 
				tmp.append(filename.split(".")[0])
		return tmp

	#-------
	#i need to call this from the main script
	def load(self,tk,callback):
		self.callback=callback
		c = configure_loader(tk,self.directory,self.load_callback)


	def load_callback(self,payload):
		#self.canvas.delete("artist")
		#first, if this is not an internal folder, we need to load in the files

		#now we can pass this to the program to use
		self.callback("newArtist")
		#self.load_asset(payload["path"]+"/"+payload["file"],True)
		

#-----------------------------------------
#here is where the tkinter stuff starts

from tkinter import *
from tkinter import filedialog
from tkhelpers import dialog

class configure_loader(dialog):
	def __init__(self,parent,directory,callback):

		self.directory=directory

		dialog.__init__(self, parent, "artist loader", buttonBoxType=1,applyCallback=callback)
		

	def body(self, master):

		#box = Frame(self)
		self.v["path"] = StringVar()
		self.v["path"].set(self.directory)
		self.e["path"] = Entry(master,textvariable = self.v["path"], width=40)
		self.e["path"].grid(row=0,column=0)

		w = Button(master, text="Browse", width=10, command=self.changeDirectory, default=ACTIVE)
		w.grid(row=0,column=1)

		self.v["file"] = StringVar()
		choices = self.gatherFiles(self.directory,".py")
		self.v["file"].set(choices[0])
		self.e["file"] = OptionMenu(master,self.v["file"], *choices )
		self.e["file"].grid(row=1,column=0)

		#this is strange, to get a callback on when the dropdown choce is made, this is how it is connected
		self.v["file"].trace('w', self.optionPicked)

	#-------------------------------------------------------------
	#CUSTOM methods to this --------------------------------------
	#button to change directoy was pressed, this throws up a file browser
	def changeDirectory(self):
		prev = self.directory
		self.directory = filedialog.askdirectory(initialdir = self.directory,title = "Select directory")
		#only proceed if we change the directory
		if prev != self.directory:
			choices = self.gatherFiles(self.directory,".py")
			self.v["file"].set(choices[0])
			self.v["path"].set(self.directory)
			#this is a helper function to refil the dropdown menu
			self.updateOptionsMenu(self.e["file"],choices,self.v["file"])