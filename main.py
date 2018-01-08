from tkinter import *
import threading
import sys
import os
import time
import json
import argparse
import platform
if(platform.system() == "Windows"):
	sys.path.append(os.getcwd()+"\\src")
	sys.path.append(os.getcwd()+"\\mod")
	# sys.path.append(os.getcwd()+"\\mod\\assets")
else:
	sys.path.append(os.getcwd()+"/src")
	sys.path.append(os.getcwd()+"/mod")
	# sys.path.append(os.getcwd()+"/mod/assets")

from preferences import preferences

from vector import *
from segment import segment
#import n
from grbl import grbl

# import a_01_helloWorld
# import a_02
import a3_02_dodecahedron

#---------------------------------------------

tk = Tk()
tk.title( "plot" )

#---------------------------------------------

# Define command line argument interface
parser = argparse.ArgumentParser(description='')
parser.add_argument('-c', '--connect', action='store_true', default=False, help='connect to serial')
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print gcode to console')
args = parser.parse_args()

#---------------------------------------------

#configure
config_file = 'config.json'
configure_file = open(config_file,'r')
configure_data = json.loads(configure_file.read())
#print( configure_data["plotter_serial"] )

def call_preferences(event):
	pref_window = preferences(tk,file=config_file)

plotter_aspect = configure_data["plotter_width"]/configure_data["plotter_height"]
plotter_dimensions = vector3( float(configure_data["plotter_width"]),float(configure_data["plotter_height"]), 1.0 )
canvas_max_pixels = configure_data["canvas_max_pixels"]
width = canvas_max_pixels
height = canvas_max_pixels*(1/plotter_aspect)
afterSpeed = int(configure_data["artist_delay"] * 1000) #convert to milliseconds ,how often a new line is made in automatic draw
serial_address = configure_data["plotter_serial"] #plotter connection
maxArtistSegmentBufferSize = configure_data["artist_max_buffer_size"]#this will stop automatic drawing at a certain point if need be



#---------------------------------------------

threads = []
segmentBuffer = []
artistSegmentBuffer = []

#---------------------------------------------

canvas = Canvas(tk, width = width, height = height)
canvas.pack(fill=BOTH, expand=1)
canvas.bind_all("<p>", call_preferences)

#-------------------------------------------------------------
#  on resize
#------------------------------------------------------------

# def configure(event):
# 	global width, height
# 	width, height = event.width, event.height

# canvas.bind("<Configure>", configure)

#-------------------------------------------------------------
#  manual drawing
#-------------------------------------------------------------
mousePlotting = False
mouseStartPos = [0.0,height]#i have to do this cause y is inverted remember

def mouseRelease(event):
	global mousePlotting
	mousePlotting = False

def mousePlot(event):
	global mousePlotting, mouseStartPos
	if not mousePlotting:
		#lift pen
		segmentBuffer.append( segment( vector3(mouseStartPos[0],mouseStartPos[1],0.0), vector3(mouseStartPos[0],mouseStartPos[1],configure_data["plotter_skate_height"]), True ) )
		#get to point to drop pen
		segmentBuffer.append( segment( vector3(mouseStartPos[0],mouseStartPos[1],configure_data["plotter_skate_height"]), vector3(event.x, event.y,configure_data["plotter_skate_height"]), True ) )
		#drop pen
		segmentBuffer.append( segment( vector3(event.x, event.y,configure_data["plotter_skate_height"]), vector3(event.x, event.y,0.0) ) )
		
		mouseStartPos = [ event.x, event.y ]
		mousePlotting = True
	else:
		canvas.create_line(mouseStartPos[0],mouseStartPos[1],event.x,event.y,fill="#476042")
		seg = segment( vector3(mouseStartPos[0],mouseStartPos[1],0.0),vector3(event.x,event.y,0.0) )
		segmentBuffer.append(seg)
		mouseStartPos = [ event.x, event.y ]


canvas.bind( "<B1-Motion>", mousePlot )
canvas.bind( "<ButtonRelease-1>", mouseRelease )

#-------------------------------------------------------------
#  automatic drawing
#------------------------------------------------------------

# class drawThread(threading.Thread):
# 	def __init__( self, width, height ):
# 		threading.Thread.__init__(self)
# 		self.artist = a_01_helloWorld.a_01_helloWorld( vector2(width/2.0,height/2.0) )
# 		self.start()

# 	def run(self):
# 		print( "start drawing thread" )
# 		draw( self.artist )

def draw( artist ):

	if len(artistSegmentBuffer)<maxArtistSegmentBufferSize:
		seg = artist.update()
		if seg[0].valid:
			artistSegmentBuffer.extend(seg)
			for s in seg:
				if s.draw:
					canvas.create_line(s.p1.x,s.p1.y,s.p2.x,s.p2.y,fill=s.color)

	tk.after(afterSpeed,draw,artist)

# _drawThread = drawThread(width, height)
# threads.append(_drawThread)

_artist = a3_02_dodecahedron.a3_02_dodecahedron( vector2(width,height), configure_data["plotter_skate_height"] )
draw(_artist)

#-------------------------------------------------------------
#  plotter
#------------------------------------------------------------

grblPlotting = True #this makes it so we can turn off the while loop basically. otherwise it hangs the prompt

class gcodeThread(threading.Thread):
	def __init__( self, serial_address, connect, verbose ):
		threading.Thread.__init__(self)
		self.grbl = grbl(self,serial_address,connect,verbose=verbose)
		self._stop_event = threading.Event()

	def run(self):
		gcode( self.grbl )


def gcode( g ):
	global grblPlotting, width, height, configure_data, plotter_dimensions
	# print("start streaming gcode in thread")
	while grblPlotting:
		if len(artistSegmentBuffer)>0:
			seg = artistSegmentBuffer.pop(0)
			#before we send this along, lets do some math on it, so that its the right length relative to the ploter
			#y in the cavas goes DOWN from the top... so I want to invert it so that it goes up from bottom. Bottom left corner is 0,0
			np1 = vector3( seg.p1.x/float(width), 1.0-(seg.p1.y/float(height)), seg.p1.z ) * plotter_dimensions
			np2 = vector3( seg.p2.x/float(width), 1.0-(seg.p2.y/float(height)), seg.p2.z ) * plotter_dimensions
			ns = segment(np1,np2,seg.rapid)

			g.line(ns,configure_data['plotter_feedrate'])

_gcodeThread = gcodeThread(serial_address,args.connect,args.verbose)
threads.append(_gcodeThread)

#-------------------------------------------------------------
#  on close
#------------------------------------------------------------

def close():
	global grblPlotting, threads
	grblPlotting = False
	for t in threads:
		t.join()

	tk.destroy()

tk.protocol("WM_DELETE_WINDOW", close)



mainloop()

#-------------------------------------------------------------
#https://www.python-course.eu/tkinter_canvas.php
#https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
#http://effbot.org/zone/tkinter-window-size.htm
