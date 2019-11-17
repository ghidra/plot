import os
import json
import platform
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist import artist
from matrix import *
from vector import *
from segment import segment

import numpy as np
import time # measure if there is speed improvements

class artist3(artist):
	def __init__(self,dimensions,skateheight,fov=None,near=None,far=None,useNumpy=False):
		super().__init__(dimensions,skateheight)
		self.turtle = self.dimensions*0.5

		# this is basically a camera
		if fov is None:
			fov = 90.0
		if near is None:
			near = 0.1
		if far is None:
			far = 256.0

		self.fov = fov
		#self.rfov = fov*(3.14159265 / 180.0) #focal view in radians
		self.near = near
		self.far = far
		self.ratio	= dimensions.x/dimensions.y

		self.useNumpy = useNumpy

		if not useNumpy:
			#native matrices
			self.ttm = matrix4()
			self.rnm = matrix4()
			self.pm	= matrix4()#projection matrix
			self.vm	= matrix4()#view matrix
			self.rm	= matrix4()

		else:
			#numpy matrices
			#---------------------
			self.ttm_n = np.identity(4)
			self.rnm_n = np.identity(4)
			self.pm_n = np.identity(4)
			self.vm_n = np.identity(4)
			self.rm_n = np.identity(4)

		self.assets = []
		self.flashed = False #after sending this to plotter, stop sending it
	
	def make_frustum(self):
		rfov = self.fov*(3.14159265 / 180.0) #focal view in radians
		cosf = math.cos(math.sqrt(rfov))
		sinf = math.sin(math.sqrt(rfov))
		nf = 1-self.near/self.far
		tang = 	2*(math.tan(math.sqrt(rfov)))
		y_near = tang * self.near          
		x_near = y_near * self.ratio
		y_far = tang * self.far
		x_far = y_far * self.ratio
		
		self.near = -self.near
		self.far = -self.far
		
		if not self.useNumpy:
			self.pm = matrix4( vector4(cosf,0,0,0),vector4(0,-cosf,0,0),vector4(0,0,sinf/nf,-(math.sin(1)/nf)*self.near),vector4(0,0,sinf,0) )
			self.vm = matrix4( vector4(self.dimensions.x,0,0,self.dimensions.x*0.5),vector4(0,self.dimensions.y,0,self.dimensions.y*0.5) ) # i dobnt know what the 99 is
			self.rm = self.pm.multiply(self.vm)
		else:
			self.pm_n = np.matrix( [[cosf,0,0,0],[0,-cosf,0,0],[0,0,sinf/nf,sinf],[0,0,-(math.sin(1)/nf)*self.near,0]] )
			self.vm_n = np.matrix( [[self.dimensions.x,0,0,0],[0,self.dimensions.y,0,0],[0,0,1,0],[self.dimensions.x*0.5,self.dimensions.y*0.5,0,1]] ) # i dobnt know what the 99 is
			self.rm_n = self.pm_n * self.vm_n

		#print("-----makefrustum numpy")
		#print(self.rm_n.T)

	def load_asset(self,asset,explicit=False):

		if not explicit:
			path="mod"
			if(platform.system() == "Windows"):
				path+="\\assets\\"
			else:
				path+="/assets/"

			configure_file = open(path+asset+".json",'r')
		else:
			configure_file = open(asset,'r')

		configure_data = json.loads(configure_file.read())

		new_asset = {}

		for pref in configure_data:
			#------------------------------------
			if pref == "name":
				new_asset["name"] = configure_data[pref]
			#------------------------------------
			if pref == "points":
				new_asset["points"] = []
				new_asset["numpy_points"] = []
				for i in range( len(configure_data[pref])//3 ):
					if not self.useNumpy:
						new_asset["points"].append(vector3(configure_data[pref][i*3],configure_data[pref][i*3+1],configure_data[pref][i*3+2]))
					else:
						#numpy methods
						if(i==0):
							new_asset["numpy_points"] = np.array([[configure_data[pref][i*3],configure_data[pref][i*3+1],configure_data[pref][i*3+2],1]])
						else:
							new_asset["numpy_points"] = np.append(new_asset["numpy_points"],[[configure_data[pref][i*3],configure_data[pref][i*3+1],configure_data[pref][i*3+2],1]],axis=0)
			#------------------------------------
			if pref == "segments":
				new_asset["segments"] = list(configure_data[pref])
			#------------------------------------
			if not self.useNumpy:
				new_asset["rnm"] = matrix4()
			else:
				new_asset["rnm_n"] = np.identity(4)

		self.assets.append(new_asset)

	def setup(self,payload={}):
		self.attributes["cam_fov"] = payload["cam_fov"] if "cam_fov" in payload else self.fov
		self.fov = self.attributes["cam_fov"]
		self.attributes["cam_rx"] = payload["cam_rx"] if "cam_rx" in payload else 0.0
		self.attributes["cam_ry"] = payload["cam_ry"] if "cam_ry" in payload else 33.0
		self.attributes["cam_rz"] = payload["cam_rz"] if "cam_rz" in payload else 0.0
		self.attributes["cam_tx"] = payload["cam_tx"] if "cam_tx" in payload else 0.0
		self.attributes["cam_ty"] = payload["cam_ty"] if "cam_ty" in payload else 0.0
		self.attributes["cam_tz"] = payload["cam_tz"] if "cam_tz" in payload else -2.0

		if not self.useNumpy:
			self.rnm = matrix4()
			self.ttm = matrix4()
			self.rnm = self.ttm.rotate_x(self.attributes["cam_rx"]).rotate_y(self.attributes["cam_ry"]).rotate_z(self.attributes["cam_rz"]).translate( vector3(self.attributes["cam_tx"],self.attributes["cam_ty"],self.attributes["cam_tz"]) )
			self.rnm.transpose()
		else:
			self.ttm_n = np.identity(4)
			self.rnm_n = np.identity(4)
			self.rnm_n = np_translate( np_rotate_z(  np_rotate_y(  np_rotate_x(self.ttm_n,self.attributes["cam_rx"])  ,self.attributes["cam_ry"])  ,self.attributes["cam_rz"]) , self.attributes["cam_tx"],self.attributes["cam_ty"],self.attributes["cam_tz"] )

		self.make_frustum();


	def render(self):
		self.segment = []

		segment_insert_index=0 #if we have multiple assets, we need to insert skates at the right index
		oldTotal=0
		numpyTotal=0
		segTotal=0

		for asset in self.assets:

			if not self.useNumpy:
				newttm = matrix4()
				newttm = newttm.multiply( asset["rnm"] ).multiply( self.rnm )
				newttm = newttm.multiply( self.rm )

				points = []
				for p in asset["points"]:
					point = vector4(p.x,p.y,p.z,1.0)
					point = point.mult_matrix4( newttm );
					
					ux = point.x / point.w
					uy = point.y / point.w
					uz = point.z / point.w #z is kind of useless in this case

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

			else:
				#numpy version
				newttm_n = np.identity(4)
				newttm_n = newttm_n * asset["rnm_n"]
				newttm_n = newttm_n * self.rnm_n
				newttm_n = newttm_n * self.rm_n
			
				points_n = asset["numpy_points"].dot(newttm_n)
				points_n = points_n[:,:2]/points_n[:,[3]]#if I want z, add a 3, ie [:,:3] to first delete


	#override method
	def dispatch(self):
		self.update_finish()#dont really need this so it can be here for now
		if self.ready:
			if self.flashed:
				self.segment=[ segment(vector3(),vector3()) ]
			else:
			 	self.segment.insert( 0, self.lift( self.origin() ) ) #lift the pen off origin
			self.flashed = True
			return self.segment
		else:
			return self.waiting()

	def update(self):
		super().update()
		return self.dispatch()

	#=====================
	def configure(self,tk,canvas,segmentBuffer):
		self.canvas=canvas
		c = artist3_dialog(tk,self.attributes,self.configure_callback)

	def configure_callback(self,payload):
		self.canvas.delete("artist")
		self.segment_count=0
		self.setup(payload)
		self.render()
		self.flashed=False
				

##---------------------
from tkinter import *
from tkhelpers import dialog

class artist3_dialog(dialog):
	def __init__(self,parent,attributes,callback):
		self.attributes=attributes #incoming dictionary or attributes I want to reference
		super().__init__(parent, "artist settings",buttonBoxType=1,applyCallback=callback)

	def body(self, master):
		self.mainframe = LabelFrame(master, padx=1, pady=1)
		self.mainframe.grid()

		group = LabelFrame(self.mainframe, text="Camera", padx=1, pady=1)
		group.grid(row=0, padx=1, pady=1)

		Label(group, text="fov:").grid(row=0)
		self.v["cam_fov"] = DoubleVar()
		self.v["cam_fov"].set( self.attributes["cam_fov"] if "cam_fov" in self.attributes else 90.0 )
		self.e["cam_fov"] = Scale(group,variable = self.v["cam_fov"],orient=HORIZONTAL, from_=1, to=180,resolution=0.1)
		self.e["cam_fov"].grid(row=0,column=1)

		groupt = LabelFrame(group, text="Translate", padx=1, pady=1)
		groupt.grid(row=1, columnspan=2,padx=1, pady=1)

		groupr = LabelFrame(group, text="Rotate", padx=1, pady=1)
		groupr.grid(row=2, columnspan=2,padx=1, pady=1)

		Label(groupt, text="x:").grid(row=0)
		self.v["cam_tx"] = DoubleVar()
		self.v["cam_tx"].set( self.attributes["cam_tx"] if "cam_tx" in self.attributes else 0.0 )
		self.e["cam_tx"] = Scale(groupt,variable = self.v["cam_tx"],orient=HORIZONTAL, from_=-2, to=2,resolution=0.01)
		self.e["cam_tx"].grid(row=0,column=1)

		Label(groupt, text="y:").grid(row=1)
		self.v["cam_ty"] = DoubleVar()
		self.v["cam_ty"].set( self.attributes["cam_ty"] if "cam_ty" in self.attributes else 0.0 )
		self.e["cam_ty"] = Scale(groupt,variable = self.v["cam_ty"],orient=HORIZONTAL, from_=-2, to=2,resolution=0.01)
		self.e["cam_ty"].grid(row=1,column=1)

		Label(groupt, text="z:").grid(row=2)
		self.v["cam_tz"] = DoubleVar()
		self.v["cam_tz"].set( self.attributes["cam_tz"] if "cam_tz" in self.attributes else 0.0 )
		self.e["cam_tz"] = Scale(groupt,variable = self.v["cam_tz"],orient=HORIZONTAL, from_=-2, to=2,resolution=0.01)
		self.e["cam_tz"].grid(row=2,column=1)

		Label(groupr, text="x:").grid(row=0)
		self.v["cam_rx"] = DoubleVar()
		self.v["cam_rx"].set( self.attributes["cam_rx"] if "cam_rx" in self.attributes else 0.0 )
		self.e["cam_rx"] = Scale(groupr,variable = self.v["cam_rx"],orient=HORIZONTAL, from_=-180, to=180,resolution=1.0)
		self.e["cam_rx"].grid(row=0,column=1)

		Label(groupr, text="y:").grid(row=1)
		self.v["cam_ry"] = DoubleVar()
		self.v["cam_ry"].set( self.attributes["cam_ry"] if "cam_ry" in self.attributes else 0.0 )
		self.e["cam_ry"] = Scale(groupr,variable = self.v["cam_ry"],orient=HORIZONTAL, from_=-180, to=180,resolution=1.0)
		self.e["cam_ry"].grid(row=1,column=1)

		Label(groupr, text="z:").grid(row=2)
		self.v["cam_rz"] = DoubleVar()
		self.v["cam_rz"].set( self.attributes["cam_rz"] if "cam_rz" in self.attributes else 0.0 )
		self.e["cam_rz"] = Scale(groupr,variable = self.v["cam_rz"],orient=HORIZONTAL, from_=-180, to=180,resolution=1.0)
		self.e["cam_rz"].grid(row=2,column=1)

