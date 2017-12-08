import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from a import a
from s import s
from v import *
import n

class a_01_helloWorld(a):
	def __init__(self,startPos):
		super().__init__()
		self.turtle = startPos
	
	def update(self):

		self.tick = (time.time()-self.last)
		self.elapse += self.tick

		np = n.snoise3( vector3(self.turtle.x+9.34,self.turtle.y,self.elapse) ) * 100.0 * self.tick
		newpos = self.turtle + vector2(np.x,np.y)

		segment = s( self.turtle, newpos )
		
		self.turtle = newpos
		self.last = time.time()

		return segment