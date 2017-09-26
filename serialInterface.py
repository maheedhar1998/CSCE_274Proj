import serial
class sInterface:
	def __init__(self):
		serialC = serial.Serial('/dev/ttyUSB0', 115200)
	def connect (self):
		self.serialC.close()
		self.serialC.open()
		return
	def send(self, opCode):
		serialC.write(chr(opCode))
		return
	def send(self, opCodes):
		x = ""
		for i in range(0, opCodes.len):
			x = x+chr(opCodes[i])
		self.serialC.write(x)
		return
	def read(self):
		x = self.serialC.inWaiting()
		return self.serialC.read(x)
	def close(self):
		self.serialC.close()
		return
class rInterface:
	def __init__():
		robot = sInterface()
		robot.connect
		start = 128
		reset = 7
		stop = 173
		safe = 131
		sensors = 142
		buttonPacketID = 18
		drive = 137
	def changeState(self, state):
		if(str(state) == 'start' or str(state) == 'passive'):
			self.robot.send(start)
		elif(str(state) == 'reset'):
			self.robot.send(reset)
		elif(str(state) == 'stop'):
			self.robot.send(stop)
		elif(str(state) == 'safe'):
			self.robot.send(safe)
		else:
			print "Error: Invalid arguement"
	def stateOfButton(self, button):
		self.robot.send({sensors, buttonPacketID})
		data = self.robot.read
		data = int(state)
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
	def drive(self, velocityH, velocityL, radiusH, radiusL):
		self.robot.send(chr(drive)+chr(velocityH)+chr(velocityL)+chr(radiusH)+chr(radiusL))
		return
class main:
	iRobot = sInterface()
	iRobot.connect()
	iRobot.send(128)

