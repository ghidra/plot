#https://docs.python.org/3/tutorial/classes.html
#https://www.tutorialspoint.com/python/python_classes_objects.htm
import math
import numbers

class vector2:
	def __init__(self,x=None,y=None):
	 	if x is None:
	 		self.x = 0.0
	 	else:
	 		self.x = x
	 	if y is None:
	 		self.y = 0.0
	 	else:
	 		self.y = y

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
	
	def __mul__(self,v):
		if isinstance(v,(numbers.Number)):
			return vector2(self.x*v,self.y*v)
		else:
			return vector2(self.x*v.x,self.y*v.y)

	def length(self):
		return math.sqrt( (self.x*self.x) + (self.y*self.y) )

	def normalize(self):
		nlength = self.length()
		if nlength == 0 : #if magnitude comes back as 0 avoid dividing by 0
			self.x=0.0
			self.y=0.0
		else:
			self.x = self.x / nlength
			self.y = self.y / nlength

	def dot(self,v):
		return ( self.x * v.x + self.y * v.y )

	def printable(self):
		return "x:"+str(self.x)+", y:"+str(self.y)

	#-------STATIC
	def length(v):
		return math.sqrt( (v.x*v.x) + (v.y*v.y) )

	def normalize(v):
		nlength = math.sqrt( (v.x*v.x) + (v.y*v.y) )
		if nlength == 0 : #if magnitude comes back as 0 avoid dividing by 0
			return vector2 (0.0,0.0)
		else:
			return vector2 (v.x / nlength, v.y / nlength)

	def dot(v1,v2):
		return ( v1.x * v2.x + v1.y * v2.y )

#==================================================================

class vector3(vector2):
	def __init__(self,x=None,y=None,z=None):
	 	super().__init__(x,y)
	 	if z is None:
	 		self.z = 0.0
	 	else:
	 		self.z = z

	def __add__(self,v):
		if isinstance(v,(numbers.Number)):
			return vector3(self.x+v,self.y+v,self.z+v)
		else:
			return vector3(self.x+v.x,self.y+v.y,self.z+v.z)
	
	def __sub__(self,v):
		if isinstance(v,(numbers.Number)):
			return vector3(self.x-v,self.y-v,self.z-v)
		else:
			return vector3(self.x-v.x,self.y-v.y,self.z-v.z)
	
	def __mul__(self,v):
		if isinstance(v,(numbers.Number)):
			return vector3(self.x*v,self.y*v,self.z*v)
		else:
			return vector3(self.x*v.x,self.y*v.y,self.z*v.z)
	
	def length(self):
		return math.sqrt( (self.x*self.x) + (self.y*self.y)+ (self.z*self.z) )
	
	def normalize(self):
		nlength = self.length()
		if nlength == 0 : #if magnitude comes back as 0 avoid dividing by 0
			self.x=0.0
			self.y=0.0
			self.z=0.0
		else:
			self.x = self.x / nlength
			self.y = self.y / nlength
			self.z = self.z / nlength

	def dot(self,v):
		return ( self.x * v.x + self.y * v.y + self.z * v.z )
	
	def cross(self,v):
		return(	(self.y * v.z) - (self.z * v.y) , (self.z * v.x) - (self.x * v.z) , (self.x * v.y) - (self.y * v.x))

	def printable(self):
		return super().printable() +" ,z:"+str(self.z)

	#MATRIC METHODS

	def mult_matrix3(self,m):    
		x = m._n11 * self.x + m._n12 * self.y + m._n13 * self.z
		y = m._n14 * self.x + m._n21 * self.y + m._n22 * self.z
		z = m._n23 * self.x + m._n24 * self.y + m._n31 * self.z

		return vector3(x,y,z)

	def mult_matrix4(self,m):
		x = m._n11 * self.x + m._n12 * self.y + m._n13 * self.z + m._n14 #* self.w;
		y = m._n21 * self.x + m._n22 * self.y + m._n23 * self.z + m._n24 #* self.w;
		z = m._n31 * self.x + m._n32 * self.y + m._n33* self.z + m._n34 #* self.w;
		#w = m._n41* self.x + m._n42* self.y + m._n43* self.z + m._n44 * self.w;
		
		return vector3(x,y,z)

	#------STATIC
	def length(v):
		return math.sqrt( (v.x*v.x) + (v.y*v.y) + (v.z*v.z) )
	def normalize(v):
		nlength = math.sqrt( (v.x*v.x) + (v.y*v.y) + (v.z*v.z) )
		if nlength == 0 : #if magnitude comes back as 0 avoid dividing by 0
			return vector3 (0.0,0.0,0.0)
		else:
			return vector3 (v.x / nlength, v.y / nlength, v.z / nlength)
	def dot(v1,v2):
		return ( v1.x * v2.x + v1.y * v2.y + v1.z * v2.z )

	def cross(v1,v2):
		return(	(v1.y * v2.z) - (v1.z * v2.y) , (v1._z * v2.x) - (v1._x * v2.z) , (v1._x * v2.y) - (v1._y * v2.x) )

#==================================================================

class vector4(vector3):
	def __init__(self,x=None,y=None,z=None,w=None):
		super().__init__(x,y,z)
		if w is None:
			self.w = 0.0
		else:
			self.w = w

	def printable(self):
		return super().printable() + " ,w:"+str(self.w)

	def mult_matrix4(self,m):
		x = m._n11 * self.x + m._n12 * self.y + m._n13 * self.z + m._n14 * self.w;
		y = m._n21 * self.x + m._n22 * self.y + m._n23 * self.z + m._n24 * self.w;
		z = m._n31 * self.x + m._n32 * self.y + m._n33* self.z + m._n34 * self.w;
		w = m._n41* self.x + m._n42* self.y + m._n43* self.z + m._n44 * self.w;

		return vector4(x,y,z,w)
