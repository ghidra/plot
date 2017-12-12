from tkinter import *
import threading
import sys
import os
import serial #"python -m pip install pyserial"
#import re
import time

sys.path.append(os.getcwd()+"\\src")
from v import *
from s import s
import n

sys.path.append(os.getcwd()+"\\mod")
import a_01_helloWorld

#---------------------------------------------

#canvas size
width = 800
height = 400

#how often a new line is made in automatic draw
afterSpeed = 100

#---------------------------------------------

#plotter connection
buffer_size = 128
baud = 9600
serial_address = ""
doPlot = False # this is just here if we are testing without a plotter connected, we bypass all plotter code

#---------------------------------------------

#this is the array of segments.
segmentBuffer = []
maxSegmentBufferSize = 200

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

	if len(segmentBuffer)<maxSegmentBufferSize:
		segment = artist.update()
		canvas.create_line(segment.p1.x,segment.p1.y,segment.p2.x,segment.p2.y,fill=segment.color)
		segmentBuffer.append([segment.p1,segment.p2])

	tk.after(afterSpeed,draw,artist)

_drawThread = drawThread(width, height)

#-------------------------------------------------------------
#  plotter
#------------------------------------------------------------

class gcodeThread(threading.Thread):
   
	def __init__( self , serial_address, baud, buffer_size):
		threading.Thread.__init__(self)
		if doPlot:
			self.device = serial.Serial(serial_address,baud)
		self.baud = baud
		self.buffer_size = buffer_size

		## Wake up grbl
		if doPlot:
			self.device.write("\r\n\r\n")
		print("init gcode thread")
		threading.Timer(2, self.flushOnWake).start()

	def flushOnWake(self):
		if doPlot:
			self.device.flushInput()
		self.start()

	def run(self):
		print("start gcode thread")
		gcode()


def gcode():
	print("coding it up")
	if doPlot:
		while len(segmentBuffer)>0:
			segment = segmentBuffer.pop(0)
			#print(*myData)

_gcodeThread = gcodeThread(serial_address, baud, buffer_size)
#-------------------------------------------------------------

mainloop()

#-------------------------------------------------------------
#https://www.python-course.eu/tkinter_canvas.php
#https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
#http://effbot.org/zone/tkinter-window-size.htm