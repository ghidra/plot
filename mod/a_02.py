import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from a import a
from s import s
from v import *
import n

class a_02(a):
	def __init__(self,dimensions):
		super().__init__(dimensions)
		#i want to start a little off center
		self.turtle = dimensions*0.75

		self.radius = vector2.length(self.turtle-self.center)
		self.speed = 0.89
		self.collapse = 0.01 #how fast it goes toward the center...
		self.phase = 0.5 #how often we are "off"
	
	def update(self):
		super().update()

		np = n.curl3( vector3(self.turtle.x+9.34,self.turtle.y,self.elapse)*0.001 ) * 100.0 * self.tick

		self.radius-=self.elapse*self.collapse
		rate = self.elapse*self.speed
		cleantarget = self.center + (vector2(math.sin(rate),math.cos(rate)) * self.radius) + (vector2(np.x,np.y) *3.43)
		direction = cleantarget-self.turtle

		self.advect( direction ) 
		self.update_finish()

		return self.segment