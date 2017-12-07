#this class is the base class of any modules used to draw with the after
import v
import time

class a:
	def __init__(self,tkinter):
		self.tk = tkinter
		self.last = time.time()
		self.tick = 0.0
		self.elapse = 0.0
		self.turtle = v.vector2()
		
	def update(self):
		print("we are updating from base")