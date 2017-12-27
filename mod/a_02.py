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
		self.turtle = dimensions*0.55

		self.radius = vector2.length(self.turtle-self.center)
		self.speed = 0.49
		self.collapse = 0.01 #how fast it goes toward the center...
		self.phase = 6.5 #how often we are "off"

		self.noisemag = 3.33
		self.noisescale = 0.001

		self.noisemag2 = 0.01
		self.noisescale2 = 0.005

		self.wait = 2 #i need to wait 2 ticks before I start drawing... cause those first 2 are bogus
		self.waitcount = 0
		self.ready = False # i want to wait before recording

		self.turtle = self.getcircle()
	
	def update(self):
		super().update()

		# np = n.curl3( vector3(self.turtle.x+9.34,self.turtle.y,self.elapse)*0.001 ) * 100.0 * self.tick

		if self.radius > 0.0:
			self.radius-=self.collapse
			# rate = self.elapse*self.speed
			cleantarget = self.getcircle()
			direction = cleantarget-self.turtle

			self.advect( direction ) 
			self.update_finish()
		else:
			self.segment = s(vector2(),vector2())

		if self.ready:
			return self.segment
		else:
			if self.waitcount > self.wait:
				self.ready = True
			self.waitcount+=1
			return s(vector2(),vector2())

	def getcircle(self):
		rate = self.elapse*self.speed
		return self.center + (vector2(math.sin(rate),math.cos(rate)) * self.radius) + self.getnoise()

	def getnoise(self):
		noise = n.curl3( vector3(self.turtle.x+9.34,self.turtle.y,self.elapse*self.phase)*self.noisescale ) * 100.0 * self.tick
		noise2 = n.curl3( vector3(self.turtle.x-3.17,self.turtle.y,self.elapse*self.phase)*self.noisescale2 ) * 100.0 * self.tick
		
		return (vector2(noise.x,noise.y)*self.noisemag) + (vector2(noise2.x,noise2.y)*self.noisemag2)