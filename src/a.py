#this class is the base class for any artist modules 
#used to draw with the after method on the tkinter canvas
#update should return a segment, class "s"
import time
from v import vector2
from s import s

class a:
	def __init__(self,dimensions):
		self.last = time.time()
		self.tick = 0.0
		self.elapse = 0.0
		self.dimensions = dimensions
		self.center = dimensions*0.5
		self.speed = 1.0
		self.turtle = vector2()
		self.segment = s(vector2(),vector2())
		
	def update(self):
		self.tick = (time.time()-self.last)
		self.elapse += self.tick
		# self.last = time.time()
		# return s(vector2(),vector2())

	def advect(self,v):
		newpos = self.turtle + v
		self.segment = s( self.turtle, newpos )
		self.turtle = newpos

	def update_finish(self):
		self.last = time.time()