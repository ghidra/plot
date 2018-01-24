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
		self.setup()
		self.render()
	
	# def update(self):
	# 	super().update()
	# 	return self.dispatch()