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
		self.turtle_last = self.origin() # always start in the bottom corner
		self.segment = [ segment(vector3(),vector3()) ]

		self.skating = False

		self.wait = 0.0 #i need to wait 2 ticks before I start drawing... cause those first 2 are bogus
		self.waitcount = 0.001
		self.ready = False
		
	def update(self):
		self.tick = (time.time()-self.last)
		self.elapse += self.tick

	def update_finish(self):
		self.last = time.time()

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
	def origin(self):
		return vector2(0.0,self.dimensions.y)

	#this method basically, makes sure that you send the command to pick the pen up from origin
	#as well it takes into account the waiting
	def dispatch(self):
		self.update_finish()
		if self.ready:
			return self.segment
		else:
			return self.waiting()

	#this method actually does the initial lift of the pen from origin
	def waiting(self):
		if self.waitcount > self.wait:
			self.ready = True
			self.turle_last = self.origin()
			return [ self.lift( self.turle_last ) ]
		self.waitcount+=1
		return [ segment(vector3(),vector3()) ]


	#this is a simple 2d advect method. Send in a velocity to move the turle
	def advect(self,v):
		newpos = self.turtle + v
		self.segment = [ segment( vector3(self.turtle.x,self.turtle.y,0.0), vector3(newpos.x,newpos.y,0.0) ) ]
		self.turtle = newpos