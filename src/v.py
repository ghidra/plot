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

	def normalized(v):
		nlength = math.sqrt( (v.x*v.x) + (v.y*v.y) )
		if nlength == 0 : #if magnitude comes back as 0 avoid dividing by 0
			return vector2 (0.0,0.0)
		else:
			return vector2 (v.x / nlength, v.y / nlength)

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

	def normalized(v):
		nlength = math.sqrt( (v.x*v.x) + (v.y*v.y) + (v.z*v.z) );
		if nlength == 0 : #if magnitude comes back as 0 avoid dividing by 0
			return vector3 (0.0,0.0,0.0);
		else:
			return vector3 (v.x / nlength, v.y / nlength, v.z / nlength);