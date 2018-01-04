import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist3 import artist3
from segment import segment
from vector import *
import n

class a3_01_cube(artist3):
	def __init__(self,dimensions,skateheight):
		super().__init__(dimensions,skateheight)
		self.turtle = self.dimensions*0.5

		self.load_asset("cube")
	
	def update(self):
		super().update()

		np = n.snoise3( vector3(self.turtle.x+9.34,self.turtle.y,self.elapse) ) * 100.0 * self.tick

		self.advect( vector2(np.x,np.y) )
		self.update_finish()

		return self.segment