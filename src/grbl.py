#	grbl streamer

import serial #"python -m pip install pyserial"
import threading
import itertools #this is so I can know what type of vectors we are working with
from vector import *

class grbl:
	def __init__(self,thread,address,connected=False,inches=False,incremental=False,verbose=False):
		self.thread = thread #this is the thread that called this... so we can return the favor and start it later
		self.address = address
		self.connected = connected # this is just here if we are testing without a plotter connected, we bypass all plotter code
		self.verbose = verbose

		self.baud = 9600
		self.inBuffer = [] # Track number of characters in grbl serial read buffer
		self.RX_BUFFER_SIZE = 128
		self.device = 0

		self.measurement = 'G20' if inches else 'G21'
		self.mode = 'G91' if incremental else 'G90'
		self.incremental = incremental

		if connected:
			self.device = serial.Serial(self.address,self.baud)
			self.device.write(bytes("\r\n\r\n", 'UTF-8'))
		
		threading.Timer(2, self.flushOnWake).start()
		#print("int gcode thread")

	def flushOnWake(self):
		if self.connected:
			self.device.flushInput()
		self.stream(self.mode)
		self.stream(self.measurement)
		self.thread.start()

	def stream(self,gcode):
		block = gcode.strip()

		if self.connected:
			self.inBuffer.append(len(block)+1) # Track number of characters in grbl serial read buffer

			while sum(self.inBuffer) >= self.RX_BUFFER_SIZE-1 | self.device.inWaiting() :
				out_temp = self.device.readline().strip().decode('utf-8') # Wait for grbl response
				if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
					print ("  Debug: ",out_temp) # Debug response
				else :
					del self.inBuffer[0] # Delete the block character count corresponding to the last 'ok'
			self.device.write(bytes(block + "\n", 'UTF-8')) # Send g-code block to grbl
		
		if self.verbose:
			print(block)

	def line(self,segment,feedrate):
		#if type(segment.p1).__name__ is 'vector3':

		if self.incremental:
			#this is the incremental mode... so we have to do some calulating here
			direction = segment.p2-segment.p1
			code = 'G1 X'+str(direction.x)+' Y'+str(direction.y)
			if type(direction).__name__ is 'vector3':
				code +=  ' Z'+str(direction.z)
			self.stream( code+' F'+str(feedrate) )
		else:
			#this is absolute mode
			code = 'G0' if segment.rapid else 'G1'
			code += ' X'+str(segment.p2.x)+' Y'+str(segment.p2.y)
			if type(segment.p2).__name__ is 'vector3':
				code +=  ' Z'+str(segment.p2.z)
			self.stream( code+' F'+str(feedrate) )
		#this draws a line from a given segment
		#print("make a line from p1: "+str(segment.p1.x)+","+str(segment.p1.y)+" p2: "+str(segment.p2.x)+","+str(segment.p2.y) )

