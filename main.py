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
else:
	sys.path.append(os.getcwd()+"/src")
	sys.path.append(os.getcwd()+"/mod")
from preferences import preferences
from nudge import nudge
from vector import *
from segment import segment
from grbl import grbl

from artist_loader import artist_loader

#---------------------------------------------
tk = Tk()
tk.title( "plot" )
#---------------------------------------------
artists=artist_loader()
#---------------------------------------------

# Define command line argument interface
parser = argparse.ArgumentParser(description='')
parser.add_argument('-c', '--connect', action='store_true', default=False, help='connect to serial')
parser.add_argument('-v', '--verbose', action='store_true', default=False, help='print gcode to console')
parser.add_argument('-d', '--debug', action='store_true', default=False, help='skip the configure step, go strait to artist')
args = parser.parse_args()
#---------------------------------------------
#configure
config_file = 'config.json'
configure_file = open(config_file,'r')
configure_data = json.loads(configure_file.read())

def call_preferences(event):
	pref_window = preferences(tk,file=config_file)

plotter_aspect = configure_data["plotter_width"]/configure_data["plotter_height"]
plotter_dimensions = vector3( float(configure_data["plotter_width"]),float(configure_data["plotter_height"]), 1.0 )
gcode_ratio = vector3( float(configure_data["gcode_x_ratio"]),float(configure_data["gcode_y_ratio"]), float(configure_data["gcode_z_ratio"]) )
canvas_max_pixels = configure_data["canvas_max_pixels"]
width = canvas_max_pixels
height = canvas_max_pixels*(1/plotter_aspect)
afterSpeed = int(configure_data["artist_delay"] * 1000) #convert to milliseconds ,how often a new line is made in automatic draw
serial_address = configure_data["plotter_serial"] #plotter connection
maxArtistSegmentBufferSize = configure_data["artist_max_buffer_size"]#this will stop automatic drawing at a certain point if need be
percentEveryNthLine = 10 #every 10 lines in verbose mode, tell me the eprcentage complete

#---------------------------------------------
threads = []
segmentBuffer = []
artistSegmentBuffer = []
artistConfigured = args.debug
#---------------------------------------------
canvas = Canvas(tk, width = width, height = height)
canvas.pack(fill=BOTH, expand=1)

#status = Text(tk,state='disabled', width=80, height=1, wrap='none')
status_string = StringVar()
status = Entry(canvas,textvariable=status_string, state=DISABLED)
status.config(borderwidth=0,justify=CENTER,relief=FLAT)
status_string.set('preview')

canvas.create_window(0, 0, window=status,anchor=NW)
#status.pack()

#status.insert(INSERT,"preview")
if artistConfigured:
	status_string.set('plot')

#status.config(state=DISABLED)
#status.config(state=NORMAL)
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
		
		segmentBuffer.append( segment( vector3(mouseStartPos[0],mouseStartPos[1],0.0), vector3(mouseStartPos[0],mouseStartPos[1],configure_data["plotter_skate_height"]), True ) )#lift pen
		segmentBuffer.append( segment( vector3(mouseStartPos[0],mouseStartPos[1],configure_data["plotter_skate_height"]), vector3(event.x, event.y,configure_data["plotter_skate_height"]), True ) )#get to point to drop pen
		segmentBuffer.append( segment( vector3(event.x, event.y,configure_data["plotter_skate_height"]), vector3(event.x, event.y,0.0) ) )#drop pen
		
		mouseStartPos = [ event.x, event.y ]
		mousePlotting = True
	else:
		canvas.create_line(mouseStartPos[0],mouseStartPos[1],event.x,event.y,fill="#476042",tags="manual")
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

# _drawThread = drawThread(width, height)
# threads.append(_drawThread)
#_artist = artists.list[artists.getRandom()]( vector2(width,height), configure_data["plotter_skate_height"] )
_artist = artists.list[artists.getRandom()]( vector2(plotter_dimensions.x,plotter_dimensions.y), configure_data["plotter_skate_height"] )

print(artists.loaded_artist)

def load_artist(event):
	artists.load(tk,load_callback)
def load_callback(artist_name):
	global _artist
	canvas.delete("artist")
	del artistSegmentBuffer[:]
	print("width:"+str(width)+" height:"+str(height)+" skate:"+str(configure_data["plotter_skate_height"])+" artist:"+artist_name)
	#_artist = artists.list[artist_name]( vector2(width,height), configure_data["plotter_skate_height"] )
	_artist = artists.list[artist_name]( vector2(plotter_dimensions.x,plotter_dimensions.y), configure_data["plotter_skate_height"] )


segmentsGenerated=0 #im not even sure I am using this anyway
def draw(  ):
	global _artist, width, height, plotter_dimensions
	if len(artistSegmentBuffer)<maxArtistSegmentBufferSize:
		
		# 	print("clearing")
		# 	print(len(canvas.gettags("artist")))
		#print(canvas.find_withtag("artist"))
		#print("---------------")
			#canvas.delete("artist")

		seg = _artist.update()
		segmentsGenerated=_artist.segment_count

		if seg[0].valid:
			artistSegmentBuffer.extend(seg)
			if(len(seg)>1):

				segments_flat = []#lets test out flattening this thing to see if its any faster
				line_done = False #a flag that wait for us to hit a skate point, sop we can draw the sline
				for s in seg:
					if s.draw:
						line_done=False

						#assume all positions are mm 
						#so we need to scale the to the width height of this canvas
						w_mult = (width/plotter_dimensions.x)#*gcode_ratio.x
						h_mult = (height/plotter_dimensions.y)#*gcode_ratio.y

						#print("------ x: "+str(s.p1.x)+", y: "+str(s.p1.y))
						#segments_flat.extend([s.p1.x,height-s.p1.y,s.p2.x,height-s.p2.y])
						segments_flat.extend([s.p1.x*w_mult,height-(s.p1.y*h_mult),s.p2.x*w_mult,height-(s.p2.y*h_mult)])
						segment_last_x = s.p2.x #x is correct #print(s.p2.y)
						segment_last_y = height-s.p2.y #y needs to be inverted
					else:
						if(not line_done and len(segments_flat)>0):
							canvas.create_line( segments_flat, fill=s.color, tags="artist")
							segments_flat = [] #empty this out for the next go around
						line_done=True
			else:
				#segments are coming in one at a time, just draw this guy
				if seg[0].draw:
					canvas.create_line( [seg[0].p1.x,seg[0].p1.y,seg[0].p2.x,seg[0].p2.y], fill=seg[0].color, tags="artist")
			
	tk.after(afterSpeed,draw)

draw()

#-------------------------------------------------------------
# Start plotting
#-------------------------------------------------------------
def start_plotting(event):
	global artistConfigured, status_string
	if not artistConfigured:
		#print("done configuring start plotting")
		artistConfigured = True
		status_string.set('plot')
#-------------------------------------------------------------
#  plotter
#------------------------------------------------------------
grblPlotting = True #this makes it so we can turn off the while loop basically. otherwise it hangs the prompt
segmentsPlotted=0
class gcodeThread(threading.Thread):
	def __init__( self, serial_address, connect, verbose ):
		threading.Thread.__init__(self)
		self.grbl = grbl(self,serial_address,connect,verbose=verbose)
		self._stop_event = threading.Event()

	def run(self):
		gcode( self.grbl )


def gcode( g ):
	global grblPlotting, width, height, configure_data, plotter_dimensions, artistConfigured, segmentsPlotted, segmentsGenerated #, status_string, _artist
	# print("start streaming gcode in thread")
	numSegments = len(artistSegmentBuffer)
	while grblPlotting:
		if artistConfigured:
			#status_string.set('plotting '+ str(segmentsGenerated) + ':' + str(segmentsPlotted) )
			#status_string.set('plotting ' + str(segmentsPlotted) )
			if len(artistSegmentBuffer)>0:
				seg = artistSegmentBuffer.pop(0)
				#before we send this along, lets do some math on it, so that its the right length relative to the ploter
				#y in the cavas goes DOWN from the top... so I want to invert it so that it goes up from bottom. Bottom left corner is 0,0
				#np1 = vector3( seg.p1.x/float(width), 1.0-(seg.p1.y/float(height)), seg.p1.z ) * plotter_dimensions
				#np2 = vector3( seg.p2.x/float(width), 1.0-(seg.p2.y/float(height)), seg.p2.z ) * plotter_dimensions
				#np1 = vector3( seg.p1.x*gcode_ratio.x, seg.p1.y*gcode_ratio.y, seg.p1.z )
				#np2 = vector3( seg.p2.x*gcode_ratio.x, seg.p2.y*gcode_ratio.y, seg.p2.z )
				x_safe = True
				y_safe = True
				z_safe = True
				p1x = seg.p1.x
				p2x = seg.p2.x
				p1y = seg.p1.y
				p2y = seg.p2.y
				p1z = seg.p1.z
				p2z = seg.p2.z
				if( p1x > plotter_dimensions.x ):
					p1x = plotter_dimensions.x
					x_safe = False;
				if( p1x < 0 ):
					p1x = 0
					x_safe = False
				if( p2x > plotter_dimensions.x ):
					p2x = plotter_dimensions.x
					x_safe = False;
				if( p2x < 0 ):
					p2x = 0
					x_safe = False
				if( p1y > plotter_dimensions.y ):
					p1y = plotter_dimensions.y
					y_safe = False;
				if( p1y < 0 ):
					p1y = 0
					y_safe = False
				if( p2y > plotter_dimensions.y ):
					p2y = plotter_dimensions.y
					y_safe = False;
				if( p2y < 0 ):
					p2y = 0
					y_safe = False

				np1 = vector3( p1x*gcode_ratio.x, p1y*gcode_ratio.y, seg.p1.z )
				np2 = vector3( p2x*gcode_ratio.x, p2y*gcode_ratio.y, seg.p2.z )
				ns = segment(np1,np2,seg.rapid)

				g.line(ns,configure_data['plotter_feedrate'])
				segmentsPlotted+=1

				if(args.verbose):
					if(segmentsPlotted%10==0):
						print("-------- "+str( (segmentsPlotted/numSegments)*100 )+"% Sent")
					if(segmentsPlotted/numSegments>=1):
						print("-------- 100% Sent")


_gcodeThread = gcodeThread(serial_address,args.connect,args.verbose)
threads.append(_gcodeThread)

#-------------------------------------------------------------
#  calling of nudge tool
#------------------------------------------------------------
def nudge_callback(payload):
	_gcodeThread.grbl.move(payload,configure_data['plotter_feedrate']);
def nudge_closed():
	_gcodeThread.grbl.setOrigin()
	_gcodeThread.grbl.resetMode()
def call_nudge(event):
	if not artistConfigured and _gcodeThread.grbl.ready:
		_gcodeThread.grbl.setIncremental()
		nudge_window = nudge(tk,nudge_callback,nudge_closed)
	else:
		if not _gcodeThread.grbl.ready:
			print("please wait for plotter to be ready")
		else:
			print("nudge can only be called when in preview mode")
	#status.delete(1.0,END)
	#status.insert(INSERT,"plot")

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
#-------------------------------------------------------------
#  button bindings
#------------------------------------------------------------
canvas.bind_all( "<p>", call_preferences )
canvas.bind_all( "<n>", call_nudge )
canvas.bind_all( "<l>", load_artist )
canvas.bind_all( "<a>", lambda e:_artist.configure(tk,canvas,artistSegmentBuffer) )
canvas.bind_all( "<space>", start_plotting )
#canvas.bind_all( "<s>", lambda e:_artist.configure(tk) )
#-------------------------------------------------------------
#  main loop
#------------------------------------------------------------
mainloop()
#-------------------------------------------------------------
#https://www.python-course.eu/tkinter_canvas.php
#https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
#http://effbot.org/zone/tkinter-window-size.htm
