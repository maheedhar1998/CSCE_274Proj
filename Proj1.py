import time
import struct
import serial
import threading
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
	def sendMult(self, opCodes):
		for i in range(0, len(opCodes)):
			self.send(opCodes[i])
	def readD(self):
		x = self.serialC.inWaiting()
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
		self.isMoving = False;
		self.canMove = True;
		self.canContinue = True;
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
		self.robot.sendMult([self.sensors, self.buttonPacketID])
		data = self.robot.readD()
		print(len(data))
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
		else:
			return False
	def drives(self, velocityH, velocityL, radiusH, radiusL, sec):
		self.robot.sendMult([self.drive, velocityH, velocityL, radiusH, radiusL])
		time.sleep(sec+0.02)
		self.robot.sendMult([self.drive, 0, 0, 0, 0])
	def checkButton(self):
		if(self.isMoving == True):
			while True :
				if(self.stateOfButton('clean')):
					self.canContinue = False
					return
		elif(self.isMoving == False):
			while True:
				if(self.stateOfButton('clean')):
					print('yeah boy')
					self.canMove = True
					return
	def drivePentagon(self):
		print('here we go')
		self.drives(1,44,0,0,1)
		for i in range(0, 4):
			self.drives(1,244,0,1,.28)
			self.drives(1,44,0,0,1)
class main:
	iRobot = rInterface()
	iRobot.changeState('start')
	iRobot.changeState('safe')
	#driving = threading.Thread(target = iRobot.drivePentagon())
	#chkButton = threading.Thread(target = iRobot.checkButton())
	#driving.start()
	#chkButton.start()
	#print(iRobot.stateOfButton('clock'))
	iRobot.drivePentagon()
