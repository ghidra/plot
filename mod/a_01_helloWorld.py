import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from a import a
from s import s
from v import *
import n

class a_01_helloWorld(a):
	def __init__(self,dimensions):
		super().__init__(dimensions)
		self.turtle = self.dimensions*0.5
	
	def update(self):
		super().update()

		np = n.snoise3( vector3(self.turtle.x+9.34,self.turtle.y,self.elapse) ) * 100.0 * self.tick

		self.advect( vector2(np.x,np.y) )
		self.update_finish()

		return self.segment