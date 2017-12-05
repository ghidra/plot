from tkinter import *

import sys
import os
sys.path.append(is.getcwd()+"\\src")

import v
import n


tk = Tk()
tk.title( "plot" )

width = 800
height = 400

canvas = Canvas(tk,width = width, height = height)
canvas.pack(fill=BOTH, expand=1)

#-------------------------------------------------------------
#  on resize
#------------------------------------------------------------

#http://effbot.org/zone/tkinter-window-size.htm
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

	# python_green = "#476042"
	# x1, y1 = ( event.x - 1 ), ( event.y - 1 )
	# x2, y2 = ( event.x + 1 ), ( event.y + 1 )
	# canvas.create_oval( x1, y1, x2, y2, fill = python_green )


canvas.bind( "<B1-Motion>", mousePlot )
canvas.bind( "<ButtonRelease-1>", mouseRelease )


#-------------------------------------------------------------
#  automatic drawing
#------------------------------------------------------------
# n = snoise2(0.0,0.0);
# startPos = [n[0],n[1]]
# def draw():
# 	np = snoise2(startPos[0],startPos[1])
# 	startPos[0]

# #https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop

# tk.after(1000,draw)

mainloop()

#https://www.python-course.eu/tkinter_canvas.php