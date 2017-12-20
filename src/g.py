#	grbl streamer

import serial #"python -m pip install pyserial"
import threading
from v import *

class g:
	def __init__(self,thread,address,connected=False):
		self.thread = thread #this is the thread that called this... so we can return the favor and start it later
		self.address = address
		self.connected = connected # this is just here if we are testing without a plotter connected, we bypass all plotter code

		self.baud = 9600
		self.inBuffer = [] # Track number of characters in grbl serial read buffer
		self.RX_BUFFER_SIZE = 128
		self.device = 0

		if connected:
			self.device = serial.Serial(serial_address,baud)
			self.device.write("\r\n\r\n")
		
		threading.Timer(2, self.flushOnWake).start()
		#print("init gcode thread")

	def flushOnWake(self):
		if self.connected:
			self.device.flushInput()
		self.thread.start()

	def stream(self,gcode):
		block = gcode.strip()
		self.inBuffer.append(len(block)+1) # Track number of characters in grbl serial read buffer

		while sum(self.inBuffer) >= RX_BUFFER_SIZE-1 | s.inWaiting() :
			out_temp = s.readline().strip() # Wait for grbl response
			if out_temp.find('ok') < 0 and out_temp.find('error') < 0 :
				print ("  Debug: ",out_temp) # Debug response
			else :
				del self.inBuffer[0] # Delete the block character count corresponding to the last 'ok'
		s.write(block + '\n') # Send g-code block to grbl

	def line(self,segment):
		#this draws a line from a given segment
		print("make a line from p1: "+str(segment.p1.x)+","+str(segment.p1.y)+" p2: "+str(segment.p2.y)+","+str(segment.p2.y) )

