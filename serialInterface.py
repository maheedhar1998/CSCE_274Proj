import time
import struct
import serial
class sInterface:
	def __init__(self):
		self.serialC = serial.Serial('/dev/ttyUSB0', 115200)
	def connect (self):
		self.serialC.close()
		time.sleep(1)
		self.serialC.open()
		time.sleep(1)
	def send(self, opCode):
		self.serialC.write(chr(opCode))
		time.sleep(0.015)
	#def sendMult(self, opCodes):
		#x = ""
		#for i in range(0, opCodes.len):
			#x = x+chr(opCodes[i])
		#self.serialC.write(x)
	def readD(self):
		x = self.serialC.inWaiting()
		#print(x)
		return self.serialC.read(x)
	def close(self):
		self.serialC.close()
class rInterface:
	def __init__(self):
		self.robot = sInterface()
		self.robot.connect()
		self.start = 128
		self.reset = 7
		self.stop = 173
		self.safe = 131
		self.sensors = 142
		self.buttonPacketID = 18
		self.drive = 137
	def changeState(self, state):
		if(str(state) == 'start' or str(state) == 'passive'):
			self.robot.send(self.start)
		elif(str(state) == 'reset'):
			self.robot.send(self.reset)
		elif(str(state) == 'stop'):
			self.robot.send(self.stop)
		elif(str(state) == 'safe'):
			self.robot.send(self.safe)
		else:
			print "Error: Invalid arguement"
		time.sleep(1)
	def stateOfButton(self, button):
		self.robot.send(self.sensors)
		self.robot.send(self.buttonPacketID)
		data = self.robot.readD()
		data = struct.unpack('B', data)[0]
		if(button.lower() == 'clock'):
			return bool(data & 0x80)
		elif(button.lower() == 'schedule'):
			return bool(data & 0x40)
		elif(button.lower() =='day'):
			return bool(data & 0x20)
		elif(button.lower() == 'hour'):
			return bool(data & 0x10)
		elif(button.lower() == 'minute'):
			return bool(data & 0x08)
		elif(button.lower() == 'dock'):
			return bool(data & 0x04)
		elif(button.lower() == 'spot'):
			return bool(data & 0x02)
		elif(button.lower() == 'clean'):
			return bool(data & 0x01)
	def drives(self, velocityH, velocityL, radiusH, radiusL):
		self.robot.send(self.drive)
		self.robot.send(velocityH)
		self.robot.send(velocityL)
		self.robot.send(radiusH)
		self.robot.send(radiusL)
class main:
	iRobot = rInterface()
	iRobot.changeState('start')
	iRobot.changeState('safe')
	iRobot.drives(0,57,0,0)
	print(iRobot.stateOfButton('clock'))
