import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from a import a
from s import s
from v import *
import n

class a_02(a):
	def __init__(self,startPos):
		super().__init__()
		self.turtle = startPos
	
	def update(self):
		super().update()

		np = n.curl3( vector3(self.turtle.x+9.34,self.turtle.y,self.elapse)*0.01 ) * 100.0 * self.tick

		self.advect( vector2(np.x,np.y) )
		self.update_finish()

		return self.segment