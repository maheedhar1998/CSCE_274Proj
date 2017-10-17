#imports the time python library
import time
#imports the serial python library
import serial
class sInterface:
	#This commmand initializes the instance of this object to connect to the Roomba
	def __init__(self):
		self.serialC = serial.Serial('/dev/ttyUSB0', 115200)
	#This function opens a connection to the robot through serial cable
	def connect (self):
		self.serialC.close()
		time.sleep(1)
		self.serialC.open()
		time.sleep(1)
	#This function takes in an int and sends that int's corresponding character to the robot
	def send(self, opCode):
		self.serialC.write(chr(opCode))
		time.sleep(0.015)
	#This function takes in a list of integers and uses the previos send command to send one after another
	def sendMult(self, opCodes):
		for i in range(0, len(opCodes)):
			self.send(opCodes[i])
	#This function reads the data returned by the robot
	def readData(self, size):
		while True:
			x = self.serialC.inWaiting()
			if(x == size):
				return self.serialC.read(x)
	#This function closes the connection
	def close(self):
		self.serialC.close()
