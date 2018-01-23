import os
import json
import platform
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist import artist
from matrix import *
from vector import *
from segment import segment

class artist3(artist):
	def __init__(self,dimensions,skateheight,fov=None,near=None,far=None):
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
		self.rfov = fov*(3.14159265 / 180.0) #focal view in radians
		self.near = near
		self.far = far
		self.ratio	= dimensions.x/dimensions.y
		
		self.ttm = matrix4()
		# self.trm = matrix4()
		self.rnm = matrix4()
		
		self.pm	= matrix4()#projection matrix
		self.vm	= matrix4()#view matrix
		self.rm	= matrix4()

		#default outward translation
		self.rnm = self.ttm.rotate_x(0.0).rotate_y(33.0).translate( vector3(0.0,0.0,-2.0) )
		self.rnm.transpose()
		
		self.frustum = self.make_frustum();

		self.assets = []

		self.flashed = False #after sending this to plotter, stop sending it
	
	def make_frustum(self):
		cosf = math.cos(math.sqrt(self.rfov))
		sinf = math.sin(math.sqrt(self.rfov))
		nf = 1-self.near/self.far
		tang = 	2*(math.tan(math.sqrt(self.rfov)))
		y_near = tang * self.near          
		x_near = y_near * self.ratio
		y_far = tang * self.far
		x_far = y_far * self.ratio
		
		self.near = -self.near
		self.far = -self.far
		
		self.pm = matrix4( vector4(cosf,0,0,0),vector4(0,-cosf,0,0),vector4(0,0,sinf/nf,-(math.sin(1)/nf)*self.near),vector4(0,0,sinf,0) )
		self.vm = matrix4( vector4(self.dimensions.x,0,0,self.dimensions.x*0.5),vector4(0,self.dimensions.y,0,self.dimensions.y*0.5) ) # i dobnt know what the 99 is
		self.rm = self.pm.multiply(self.vm)

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
				new_points = []
				for i in range( len(configure_data[pref])//3 ):
					new_points.append(vector3(configure_data[pref][i*3],configure_data[pref][i*3+1],configure_data[pref][i*3+2]))
				new_asset["points"] = new_points
			#------------------------------------
			if pref == "segments":
				new_asset["segments"] = list(configure_data[pref])
			#------------------------------------
			new_asset["rnm"] = matrix4()

		self.assets.append(new_asset)

	def render(self):
		#we need to move the assets to render space

		# render = []
		self.segment = []
		#counter=0
		segment_insert_index=0 #if we have multiple assets, we need to insert skates at the right index
		#for each asset, lets start transforming points
		for asset in self.assets:
			
			newttm = matrix4()
			newttm = newttm.multiply( asset["rnm"] ).multiply( self.rnm )
			#newttm = newttm.multiply( self.rnm ).multiply( asset["rnm"] )
			newttm = newttm.multiply( self.rm )

			#store out newly transformed points
			points = []
			#transform each point
			# print(self.rnm.printable())
			# print(asset["rnm"].printable())
			# print(self.rm.printable())
			for p in asset["points"]:
				point = vector4(p.x,p.y,p.z,1.0)
				point = point.mult_matrix4( newttm );

				
				ux = point.x / point.w;
				uy = point.y / point.w;
				uz = point.z / point.w; #z is kind of useless in this case

				points.append( vector3(ux,uy,0.0) )

				# print("x:"+str(ux)+", y:"+str(uy))
			
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
				

##---------------------
from tkinter import *
from tkhelpers import dialog

class artist3_dialog(dialog):
	def __init__(self,parent,attributes,callback):
		self.attributes=attributes #incoming dictionary or attributes I want to reference
		dialog.__init__(self, parent, "artist settings",buttonBoxType=1,applyCallback=callback)

	def body(self, master):
		group = LabelFrame(master, text="Camera", padx=1, pady=1)
		group.grid(row=0, padx=1, pady=1)

		groupt = LabelFrame(group, text="Translate", padx=1, pady=1)
		groupt.grid(row=0, padx=1, pady=1)

		groupr = LabelFrame(group, text="Rotate", padx=1, pady=1)
		groupr.grid(row=1, padx=1, pady=1)

		Label(groupt, text="x:").grid(row=0)
		self.v["cam_tx"] = DoubleVar()
		self.v["cam_tx"].set(0)
		self.e["cam_tx"] = Scale(groupt,variable = self.v["cam_tx"],orient=HORIZONTAL, from_=0, to=360,resolution=1.0)
		self.e["cam_tx"].grid(row=0,column=1)

		Label(groupt, text="y:").grid(row=1)
		self.v["cam_ty"] = DoubleVar()
		self.v["cam_ty"].set(0)
		self.e["cam_ty"] = Scale(groupt,variable = self.v["cam_ty"],orient=HORIZONTAL, from_=0, to=360,resolution=1.0)
		self.e["cam_ty"].grid(row=1,column=1)

		Label(groupt, text="z:").grid(row=2)
		self.v["cam_tz"] = DoubleVar()
		self.v["cam_tz"].set(0)
		self.e["cam_tz"] = Scale(groupt,variable = self.v["cam_tz"],orient=HORIZONTAL, from_=0, to=360,resolution=1.0)
		self.e["cam_tz"].grid(row=2,column=1)

		Label(groupr, text="x:").grid(row=0)
		self.v["cam_rx"] = DoubleVar()
		self.v["cam_rx"].set(0)
		self.e["cam_rx"] = Scale(groupr,variable = self.v["cam_rx"],orient=HORIZONTAL, from_=0, to=360,resolution=1.0)
		self.e["cam_rx"].grid(row=0,column=1)

		Label(groupr, text="y:").grid(row=1)
		self.v["cam_ry"] = DoubleVar()
		self.v["cam_ry"].set(0)
		self.e["cam_ry"] = Scale(groupr,variable = self.v["cam_ry"],orient=HORIZONTAL, from_=0, to=360,resolution=1.0)
		self.e["cam_ry"].grid(row=1,column=1)

		Label(groupr, text="z:").grid(row=2)
		self.v["cam_rz"] = DoubleVar()
		self.v["cam_rz"].set(0)
		self.e["cam_rz"] = Scale(groupr,variable = self.v["cam_rz"],orient=HORIZONTAL, from_=0, to=360,resolution=1.0)
		self.e["cam_rz"].grid(row=2,column=1)
