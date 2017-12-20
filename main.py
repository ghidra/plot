from tkinter import *
import threading
import sys
import os
# import serial #"python -m pip install pyserial"
#import re
import time

import platform
if(platform.system() == "Windows"):
	sys.path.append(os.getcwd()+"\\src")
	sys.path.append(os.getcwd()+"\\mod")
else:
	sys.path.append(os.getcwd()+"/src")
	sys.path.append(os.getcwd()+"/mod")

from v import *
from s import s
#import n
from g import g

import a_01_helloWorld

#---------------------------------------------

#canvas size
width = 800
height = 400

#how often a new line is made in automatic draw
afterSpeed = 100

#plotter connection
serial_address = "/dev/ttyUSB0"

#---------------------------------------------

#this is the array of segments.
segmentBuffer = []
artistSegmentBuffer = []

#this will stop automatic drawing at a certain point if need be
maxArtistSegmentBufferSize = 200

#---------------------------------------------

#tkinter
tk = Tk()
tk.title( "plot" )
canvas = Canvas(tk,width = width, height = height)
canvas.pack(fill=BOTH, expand=1)

#-------------------------------------------------------------
#  on resize
#------------------------------------------------------------

def configure(event):
	#canvas.delete("all")
	global width, height
	width, height = event.width, event.height

canvas.bind("<Configure>", configure)

#-------------------------------------------------------------
#  manual drawing
#-------------------------------------------------------------
mousePlotting = False
mouseStartPos = []

def mouseRelease(event):
	global mousePlotting
	mousePlotting = False

def mousePlot(event):
	global mousePlotting, mouseStartPos
	if not mousePlotting:
		mouseStartPos = [ event.x, event.y ]
		mousePlotting = True
	else:
		canvas.create_line(mouseStartPos[0],mouseStartPos[1],event.x,event.y,fill="#476042")
		segmentBuffer.append([vector2(mouseStartPos[0],mouseStartPos[1]),vector2(event.x,event.y)])
		mouseStartPos = [ event.x, event.y ]


canvas.bind( "<B1-Motion>", mousePlot )
canvas.bind( "<ButtonRelease-1>", mouseRelease )

#-------------------------------------------------------------
#  automatic drawing
#------------------------------------------------------------

class drawThread(threading.Thread):
	def __init__( self, width, height ):
		threading.Thread.__init__(self)
		self.artist = a_01_helloWorld.a_01_helloWorld( vector2(width/2.0,height/2.0) )
		self.start()

	def run(self):
		print( "start drawing thread" )
		draw( self.artist )

def draw( artist ):

	if len(artistSegmentBuffer)<maxArtistSegmentBufferSize:
		segment = artist.update()
		canvas.create_line(segment.p1.x,segment.p1.y,segment.p2.x,segment.p2.y,fill=segment.color)
		artistSegmentBuffer.append([segment.p1,segment.p2])

	tk.after(afterSpeed,draw,artist)

_drawThread = drawThread(width, height)

#-------------------------------------------------------------
#  plotter
#------------------------------------------------------------

class gcodeThread(threading.Thread):
   
	def __init__( self ):#, serial_address, baud, buffer_size):
		threading.Thread.__init__(self)
		self.grbl = g(self,serial_address,False)

	def run(self):
		#print("start gcode thread")
		gcode( self.grbl )


def gcode( grbl ):
	print("gcoding it up")
	while len(segmentBuffer)>0:
		segment = segmentBuffer.pop(0)
		print(*segmentBuffer)

_gcodeThread = gcodeThread()#serial_address, baud, buffer_size)
#-------------------------------------------------------------

mainloop()

#-------------------------------------------------------------
#https://www.python-course.eu/tkinter_canvas.php
#https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
#http://effbot.org/zone/tkinter-window-size.htm
