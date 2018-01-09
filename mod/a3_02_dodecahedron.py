import os
import time
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from artist3 import artist3
from segment import segment
from vector import *
import n

class a3_02_dodecahedron(artist3):
	def __init__(self,dimensions,skateheight):
		super().__init__(dimensions,skateheight)

		self.sequential = True
		self.copies = 12
		self.copy_counter = 0

		self.load_asset("dodecahedron")
		self.render()
	
	def update(self):
		super().update()

		if self.copy_counter <= self.copies:
			self.copy_counter += 1
			self.assets[0]["rnm"] = self.assets[0]["rnm"].scale_uniform( 1.0-(self.copy_counter/(self.copies-1)) ).rotate_x(self.copy_counter*2.0).rotate_y(self.copy_counter*2.0)
			#self.assets[0]["rnm"] = self.assets[0]["rnm"].translate( vector3(0.0,self.copy_counter*0.01,0.0) )
		else:
			self.sequential = False

		return self.dispatch()