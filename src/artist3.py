import os
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist import artist
from matrix import *

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
		
		self.ttm = matrix4();
		self.trm = matrix4();
		self.rnm = matrix4();
		
		self.pm	= matrix4();#projection matrix
		self.vm	= matrix4();#view matrix
		self.rm	= matrix4();
		
		self.frustum = self.make_frustum();
	
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
		
		# this._obj[0] = new geometry();//create the frustum object
		
		# this._obj[0].addpoint ([x_near, y_near, this._near]); // Near, right, top
		# this._obj[0].addpoint ([x_near,-y_near, this._near]); // Near, right, bottom
		# this._obj[0].addpoint ([-x_near,-y_near, this._near]); // Near, left, bottom
		# this._obj[0].addpoint ([-x_near, y_near, this._near]); // Near, left, top
		
		# this._obj[0].addpoint ([x_far,  y_far,  this._far]);  // Far, right, top
		# this._obj[0].addpoint ([x_far, -y_far,  this._far]);  // Far, right, bottom
		# this._obj[0].addpoint ([-x_far, -y_far,  this._far]);  // Far, left, bottom
		# this._obj[0].addpoint ([-x_far,  y_far,  this._far]);  // Far, left, top
		
		# this._obj[0].addpoly([0,1,2,3],"wire");//near//I'm building all this polys counter closck wise to build positve normals pointing into frustum
		# this._obj[0].addpoly([7,6,5,4],"wire");//far	
		# this._obj[0].addpoly([4,5,1,0],"wire");//right
		# this._obj[0].addpoly([7,3,2,6],"wire");//left
		# this._obj[0].addpoly([4,0,3,7],"wire");//top
		# this._obj[0].addpoly([1,5,6,2],"wire");//bottom

		# this._obj[0]._normallist[0]._w = -this._near;
		# this._obj[0]._normallist[1]._w = -this._far;
		# this._obj[0]._normallist[2]._w = 0;
		# this._obj[0]._normallist[3]._w = 0;
		# this._obj[0]._normallist[4]._w = 0;
		# this._obj[0]._normallist[5]._w = 0;
		
		# this._obj[0].find_bounding_sphere();