class sInterface:
	import serial
	def _init_():
		serial = serial.Serial
	def connect ():
		serial('/dev/ttyUSB0',115200)
		serial.open()
		return
	def send(opCode):
		serial.write(chr(opCode))
		return
	def send(opCodes):
		x = ""
		for i in range(0, opCodes.len):
			x = x+chr(opCodes[i])
		serial.write(x)
		return
	def read():
		x = serial.inWaiting()
		return serial.read(x)
	def close():
		serial.close()
		return
class rInterface:
	def _init_():
		robot = sInterface()
		robot.connect
		start = 128
		reset = 7
		stop = 173
		safe = 131
		sensors = 142
		buttonPacketID = 18
		drive = 137
	def changeState(s,a):
		if(s.lower() == 'start' or s.lower() == 'passive'):
			robot.send(start)
		elif(s.lower() == 'reset'):
			robot.send(reset)
		elif(s.lower() == 'stop'):
			robot.send(stop)
		elif(s.lower() == 'safe'):
			robot.send(safe)
		else:
			print "Error: Invalid arguement"
	def stateOfButton(button):
		robot.send({sensors, buttonPacketID})
		state = robot.read
		state = int(state)
		if(button.lower() == 'clock'):
			return bool(state & 0x80)
		elif(button.lower() == 'schedule'):
			return bool(state & 0x40)
		elif(button.lower() == 'day'):
			return bool(state & 0x20)
		elif(button.lower() == 'hour'):
			return bool(state & 0x10)
		elif(button.lower() == 'minute'):
			return bool(state & 0x08)
		elif(button.lower() == 'dock'):
			return bool(state & 0x04)
		elif(button.lower() == 'spot'):
			return bool(state & 0x02)
		elif(button.lower() == 'clean'):
			return bool(state & 0x01)
	def drive(velocityH, velocityL, radiusH, radiusL):
		robot.send(chr(drive)+chr(velocityH)+chr(velocityL)+chr(radiusH)+chr(radiusL))
		return
class main:
	iRobot = rInterface()
	iRobot.changeState('start')
