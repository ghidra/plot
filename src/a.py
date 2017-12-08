#this class is the base class for any artist modules 
#used to draw with the after method on the tkinter canvas
#update should return a segment, class "s"
import time
from v import vector2
from s import s

class a:
	def __init__(self):
		self.last = time.time()
		self.tick = 0.0
		self.elapse = 0.0
		self.turtle = vector2()
		
	def update(self):
		print("we are updating from base, you shouldn't be")
		return s(vector2(),vector2())