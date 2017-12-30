#this class is the base class for any artist modules 
#used to draw with the after method on the tkinter canvas
#update should return a segment, class "s"
import time
from vector import *
from segment import segment

class artist:
	def __init__(self,dimensions,skateheight):
		self.last = time.time()
		self.tick = 0.0
		self.elapse = 0.0
		self.dimensions = dimensions
		self.skateheight = skateheight
		self.center = dimensions*0.5
		self.speed = 1.0
		self.turtle = vector2()
		self.turtle_last = vector2()
		self.segment = [ segment(vector3(),vector3()) ]

		self.skating = False
		
	def update(self):
		self.tick = (time.time()-self.last)
		self.elapse += self.tick
		# self.last = time.time()
		# return s(vector2(),vector2())

	def lift(self, position):
		self.skating = True
		seg = segment( vector3(position.x,position.y,0.0), vector3(position.x,position.y,self.skateheight ), True, False )
		return seg
	def skate(self,a,b):
		seg = segment( vector3(a.x,a.y,self.skateheight), vector3(b.x, b.y,self.skateheight), True, False )
		return seg
	def drop(self, position) :
		self.skating = False
		seg = segment( vector3(position.x, position.y,self.skateheight), vector3(position.x, position.y,0.0), draw=False )
		return seg

	def advect(self,v):
		newpos = self.turtle + v
		self.segment = [ segment( vector3(self.turtle.x,self.turtle.y,0.0), vector3(newpos.x,newpos.y,0.0) ) ]
		self.turtle = newpos

	def update_finish(self):
		self.last = time.time()