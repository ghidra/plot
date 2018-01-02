import math
#import numbers
from vector import *

class matrix3:
	def __init__(self,r1=None,r2=None,r3=None):
		
		if r1 is None:
			r1 = vector3(1.0,0.0,0.0)
		if r2 is None:
			r2 = vector3(0.0,1.0,0.0)
		if r3 is None:
			r1 = vector3(0.0,0.0,1.0)

		self._n11 = r1.x
		self._n12 = r1.y
		self._n13 = r1.z
		
		self._n21 = r2.x
		self._n22 = r2.y
		self._n23 = r2.z
		
		self._n31 = r3.x
		self._n32 = r3.y
		self._n33 = r3.z

class matrix4(matrix3):
	def __init__(self,r1=None,r2=None,r3=None,r4=None):

 		super().__init__( r1,r2,r3 )

 		if r1 is None:
			self._n14 = 0.0
		else:
			self._n14 = r1.w

		if r2 is None:
			self._n24 = 0.0
		else:
			self._n24 = r2.w

		if r3 is None:
			self._n34 = 0.0
		else:
			self._n34 = r3.w

		if r4 is None:
			r4 = vector4(0.0,0.0,0.0,1.0)
		
		self._n41 = r4.x 
		self._n42 = r4.y
		self._n43 = r4.z 
		self._n44 = r4.w 

	def __add__(self,v):
		if isinstance(v,(numbers.Number)):
			return vector2(self.x+v,self.y+v)
		else:
			return vector2(self.x+v.x,self.y+v.y)
	
	def __sub__(self,v):
		if isinstance(v,(numbers.Number)):
			return vector2(self.x-v,self.y-v)
		else:
			return vector2(self.x-v.x,self.y-v.y)
	
	def __mul__(self,m):
		a = m._n11*self._n11+m._n12*self._n21+m._n13*self._n31+m._n14*self._n41;
		b = m._n11*self._n12+m._n12*self._n22+m._n13*self._n32+m._n14*self._n42;
		c = m._n11*self._n13+m._n12*self._n23+m._n13*self._n33+m._n14*self._n43;
		d = m._n11*self._n14+m._n12*self._n24+m._n13*self._n34+m._n14*self._n44;
	
		e = m._n21*self._n11+m._n22*self._n21+m._n23*self._n31+m._n24*self._n41;
		f = m._n21*self._n12+m._n22*self._n22+m._n23*self._n32+m._n24*self._n42;
		g = m._n21*self._n13+m._n22*self._n23+m._n23*self._n33+m._n24*self._n43;
		h = m._n21*self._n14+m._n22*self._n24+m._n23*self._n34+m._n24*self._n44;
	
		i = m._n31*self._n11+m._n32*self._n21+m._n33*self._n31+m._n34*self._n41;
		j = m._n31*self._n12+m._n32*self._n22+m._n33*self._n32+m._n34*self._n42;
		k = m._n31*self._n13+m._n32*self._n23+m._n33*self._n33+m._n34*self._n43;
		l = m._n31*self._n14+m._n32*self._n24+m._n33*self._n34+m._n34*self._n44;
	 
		m = m._n41*self._n11+m._n42*self._n21+m._n43*self._n31+m._n44*self._n41;
		n = m._n41*self._n12+m._n42*self._n22+m._n43*self._n32+m._n44*self._n42;
		o = m._n41*self._n13+m._n42*self._n23+m._n43*self._n33+m._n44*self._n43;
		p = m._n41*self._n14+m._n42*self._n24+m._n43*self._n34+m._n44*self._n44;

		return matrix4(vector4(a,b,c,d),vector4(e,f,g,h),vector4(i,j,k,l),vector4(m,n,o,p))

	def transpose(self):
		a = self._n11;
		b = self._n21;
		c = self._n31;
		d = -self._n14;
		
		e = self._n12;
		f = self._n22;
		g = self._n32;
		h = -self._n24;
		
		i = self._n13;
		j = self._n23;
		k = self._n33;
		l = -self._n34;
		
		m = self._n14;
		n = self._n24;
		o = self._n34;
		p = self._n44;

		return matrix4(vector4(a,b,c,d),vector4(e,f,g,h),vector4(i,j,k,l),vector4(m,n,o,p))

	def translate(self,v):
		return self * matrix4(1, 0, 0, v.x, 0, 1, 0, v.y, 0, 0, 1, v.z, 0, 0, 0, 1 )

	def translate_side(self,d):
		self._n14+=self._n11*d;
		self._n24+=self._n12*d;
		self._n34+=self._n13*d;

	def translate_up(self,d):
		self._n14+=self._n21*d;
		self._n24+=self._n22*d;
		self._n34+=self._n23*d;

	def translate_out(self,d):
		self._n14+=self._n31*d;
		self._n24+=self._n32*d;
		self._n34+=self._n33*d;

	#this is a helper function
	def clamp_angle(self,a):
		d = d % 360
		if d < 0:
			d += 360
		return d

	def rotate_x(self,d):
		d = self.clamp_angle(d)
	
		pitchsin = math.sin(d)
		pitchcos = math.cos(d)

		return self * matrix4( 1, 0, 0, 0, 0, pitchcos, -pitchsin, 0, 0, pitchsin, pitchcos, 0, 0, 0, 0, 1 )
	
	def rotate_y(self,d):
		d = self.clamp_angle(d)
	
		yawsin = math.sin(d)
		yawcos = math.cos(d)

		return self * matrix4( yawcos, 0, yawsin, 0, 0, 1, 0, 0, -yawsin, 0, yawcos, 0, 0, 0, 0, 1 )

	def rotate_z(self,d):
		d = self.clamp_angle(d)
	
		rollsin = math.sin(d)
		rollcos = math.cos(d)

		return self * matrix4( rollcos, -(rollsin),	0, 0, rollsin, rollcos,	0, 0, 0, 0, 1, 0, 0, 0, 0, 1 )