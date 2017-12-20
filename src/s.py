#	segment
#	2 vector points to define a line, p1 p2

from v import *
class s:
	def __init__(self, p1, p2, color=None):
		self.p1 = p1
		self.p2 = p2

		self.valid = True
		if vector2.length(p1-p2) <= 0.00001 :
			self.valid = False

		if color is None:
			self.color = "#476042"
		else:
			self.color = color