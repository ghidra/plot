import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from a3_03_loader import a3_03_loader
from segment import segment
from vector import *
import n

class a_03_loader(a3_03_loader):
	def __init__(self,dimensions,skateheight):
		super().__init__(dimensions,skateheight)

	def setup(self,payload={}):
		self.attributes["path"] = payload["path"] if "path" in payload else self.directory
		self.attributes["file"] = payload["file"] if "file" in payload else self.filename

		#make sure we only load once
		if(self.attributes["path"] != self.directory or self.attributes["file"] != self.filename):
			self.directory = self.attributes["path"]
			self.filename = self.attributes["file"]
			#this allows us to erase the segments that have already been sent to main.
			#but we dont have it if we start with this, so we have to wait till we have it
			if(self.segmentBuffer!=None):
				del self.segmentBuffer[:]
			self.load_asset(payload["path"]+"/"+payload["file"],True)

	def configure(self,tk,canvas,segmentBuffer):
		self.canvas=canvas
		self.segmentBuffer=segmentBuffer
		c = configure_artist(tk,self.attributes,self.configure_callback)

	def render(self):
		self.segment = []

		segment_insert_index=0 #if we have multiple assets, we need to insert skates at the right index
		oldTotal=0
		numpyTotal=0
		segTotal=0

		for asset in self.assets:

			if not self.useNumpy:
				'''newttm = matrix4()
				newttm = newttm.multiply( asset["rnm"] ).multiply( self.rnm )
				newttm = newttm.multiply( self.rm )
				'''
				points = []
				for p in asset["points"]:
					'''point = vector4(p.x,p.y,p.z,1.0)
					point = point.mult_matrix4( newttm );
					
					ux = point.x / point.w
					uy = point.y / point.w
					uz = point.z / point.w #z is kind of useless in this case
					'''
					ux = p.x
					uy = p.y

					points.append( vector3(ux,uy,0.0) )

				#NOW PREPARE THE SEGMENTS
				for seg in asset["segments"]:
					for i in range( len(seg)-1 ):
						self.segment.append( segment( points[seg[i]], points[seg[i+1]] ) )# print( points[seg[i]].printable() )
						self.segment_count+=1
						
					#now for each curve, do the lifting and skating and dropping
					self.segment.append( self.lift( self.segment[len(self.segment)-1].p2 ) ) #lift the pen from the last position of the last segment
					self.skate_to(self.segment[segment_insert_index].p1,index=segment_insert_index)#insert the lifing skating and droping to the first position of the curve
					#set data for next loop
					self.turtle_last = vector2(self.segment[len(self.segment)-1].p2.x,self.segment[len(self.segment)-1].p2.y)
					segment_insert_index = len(self.segment)
'''
			else:
				#numpy version

				newttm_n = np.identity(4)
				newttm_n = newttm_n * asset["rnm_n"]
				newttm_n = newttm_n * self.rnm_n
				newttm_n = newttm_n * self.rm_n
			
				points_n = asset["numpy_points"].dot(newttm_n)
				points_n = points_n[:,:2]/points_n[:,[3]]#if I want z, add a 3, ie [:,:3] to first delete
'''

#---------------------
#  settings
#---------------------
from tkinter import *
from artist import artist_dialog

class configure_artist(artist_dialog):
	def __init__(self,parent,attributes,callback):

		self.directory=attributes["path"] #sp I can access it in change dir
		self.choices = []
		#print("init configure")
		super().__init__( parent, attributes, callback)
		

	def body(self, master):
		super().body(master)

		#--------------

		group = LabelFrame(self.mainframe, text="Load JSON", padx=1, pady=1)
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