from tkinter import *
import sys
import os
import time

sys.path.append(os.getcwd()+"\\src")
from v import *
from s import s
import n

sys.path.append(os.getcwd()+"\\mod")
import a_01_helloWorld

#---------------------------------------------

width = 800
height = 400
afterSpeed = 100

#---------------------------------------------

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

artist = a_01_helloWorld.a_01_helloWorld( vector2(width/2.0,height/2.0) )

def draw():

	segment = artist.update()
	canvas.create_line(segment.p1.x,segment.p1.y,segment.p2.x,segment.p2.y,fill=segment.color)
	tk.after(afterSpeed,draw)

tk.after(afterSpeed,draw)

#-------------------------------------------------------------

mainloop()

#-------------------------------------------------------------
#https://www.python-course.eu/tkinter_canvas.php
#https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
#http://effbot.org/zone/tkinter-window-size.htm