from tkinter import *

import sys
import os
import time
sys.path.append(os.getcwd()+"\\src")

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
#https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python
last=time.time()
tick=0.0
elapse=0.0

nn = n.snoise3(v.vector3(4.01,6.761,elapse*0.32));
turtle = v.vector2(width/2.0,height/2.0)

def draw():
	global turtle, last, elapse, tick

	tick=(time.time()-last)
	elapse+=tick

	np = n.snoise3( v.vector3(turtle.x+9.34,turtle.y,elapse) ) * 100.0 * tick
	newpos = turtle + v.vector2(np.x,np.y)
	print(np.x)
	canvas.create_line(turtle.x,turtle.y,newpos.x,newpos.y,fill="#476042")
	turtle=newpos
	#print("we be drawing: "+str(turtle.x)+","+str(turtle.y)+" : "+str(newpos.x)+","+str(newpos.y))
	last=time.time()
	tk.after(100,draw)

#https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop

tk.after(100,draw)

mainloop()

#https://www.python-course.eu/tkinter_canvas.php