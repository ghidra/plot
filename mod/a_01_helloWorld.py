import os
os.path.abspath(os.path.join(os.getcwd(), os.pardir))
from a import a

class a_01_helloWorld(a):
	def __init__(self,tkinter):
		super().__init__(tkinter)
		print("we are a module!")
	
	def update(self):
		print("we are updating")