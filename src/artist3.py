import os
import json
import platform
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist import artist
from matrix import *
from vector import *

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
		self.trm = matrix4()
		self.rnm = matrix4()
		
		self.pm	= matrix4()#projection matrix
		self.vm	= matrix4()#view matrix
		self.rm	= matrix4()
		
		self.frustum = self.make_frustum();

		self.assets = []
	
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
		self.vm = matrix4( vector4(99,0,0,self.dimensions.x),vector4(0,99,0,self.dimensions.y) ) # i dobnt know what the 99 is
		self.rm = self.pm.multiply(self.vm)

	def load_asset(self,asset):

		path="mod"
		if(platform.system() == "Windows"):
			path+="\\assets\\"
		else:
			path+="/assets/"

		configure_file = open(path+asset+".json",'r')
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

		#for each asset, lets start transforming points
		for asset in self.assets:
			
			newttm = matrix4()
			newttm = newttm.multiply( self.rnm ).multiply( asset["rnm"] )
			newttm = newttm.multiply( self.rm )

			#store out newly transformed points
			new_points = []
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

				new_points.append( vector3(ux,uy,uz) )

				#print("x:"+str(ux)+", y:"+str(uy))
