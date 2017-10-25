#imports the time python module
import time
#imports the struct python module
import struct
#imports the random pyhton module
import random
#imports the file sInterface.py
import sInterface
class rInterface:
	#This function initializes the instances of rInterface with the following arrtibutes
	def __init__(self):
		self.robot = sInterface.sInterface()
		self.robot.connect()
		#The following are opcodes and other values needed to control the robot
		self.start = 128
		self.reset = 7
		self.stop = 173
		self.safe = 131
		self.full = 132
		self.sensors = 142
		self.buttonPacketID = 18
		self.bumpsAndDrops = 7
		self.leftCliff = 9
		self.frontLeftCliff = 10
		self.frontRightCliff = 11
		self.rightCliff = 12
		self.distanceSensor = 19
		self.angleSensor = 20
		self.drive = 137
		self.driveDirect = 145
		self.song = 140
		self.play = 141
		self.robotRadius = 235/2 #in mm(milli meters)
		self.robotCircumference = 2*3.1415926535*self.robotRadius
		self.furElise = [76, 75, 76, 75, 76, 71, 74, 72, 69]
		self.harryPotter = [71, 76, 79, 78, 76, 83, 81, 78, 76, 79, 78]
		self.flashTheme = [62, 65, 69, 70, 69, 65, 62, 65, 69, 70, 69, 65, 62, 65, 62, 65]
		self.fairyTail = [74, 76, 74, 72, 69, 67, 69, 72, 74, 72, 74, 76, 74, 72, 69, 67] 
		self.noteLength = 16
		self.canContinue = False
		self.createSongs()
		self.logFile = open('iRobot_Log.txt', 'w')
	#This function takes in a string and changes the state of the robot to the state given in the string
	def changeState(self, state):
		if(str(state) == 'start' or str(state) == 'passive'):
			self.robot.send(self.start)
		elif(str(state) == 'reset'):
			self.robot.send(self.reset)
		elif(str(state) == 'stop'):
			self.robot.send(self.stop)
		elif(str(state) == 'safe'):
			self.robot.send(self.safe)
		elif(str(state) == 'full'):
			self.robot.send(self.full)
		else:
			print "Error: Invalid arguement"
		time.sleep(2)
	#This function takes in an instance of the object and returns a list of booleans that determine whether or not the buttons are pressed
	#The list will be interpretted in this order: [Clock, Schedule, Day, Hour, Minute, Dock, Spot, Clean]
	#The hexadecimal numbers in this function are interpreted from the info in the roomba open interface spec
	def stateOfButtons(self):
		self.robot.sendMult([self.sensors, self.buttonPacketID])
		data = self.robot.readData(1)
		#print('Press the Clean Button to start robot')
		data = struct.unpack('B', data)[0]
		return [bool(data & 0x80), bool(data & 0x40), bool(data & 0x20), bool(data & 0x10), bool(data & 0x08), bool(data & 0x04), bool(data & 0x02), bool(data & 0x01)]
	def getBumpsAndWheelDrops(self):
		self.robot.sendMult([self.sensors, self.bumpsAndDrops])
		data = self.robot.readData(1)
		data = struct.unpack('B', data)[0]
		bumpData = [False, False, False, False]
		if(bool(data & 0x01)):
			bumpData[3] = True
		if(bool(data & 0x02)):
			bumpData[2] = True
		if(bool(data & 0x04)):
			bumpData[1] = True
		if(bool(data & 0x08)):
			bumpData[0] = True
		return bumpData
	def checkCliffs(self):
		#Gets data from the left cliff sensor
		self.robot.sendMult([self.sensors, self.leftCliff])
		leftData = self.robot.readData(1)
		#print leftData
		leftData = struct.unpack('B', leftData)[0]
		#Gets data from the front left cliff sensor
		self.robot.sendMult([self.sensors, self.frontLeftCliff])
		frontLeftData = self.robot.readData(1)
		#print frontLeftData
		frontLeftData = struct.unpack('B', frontLeftData)[0]
		#Gets data from the front right cliff sensor
		self.robot.sendMult([self.sensors, self.frontRightCliff])
		frontRightData = self.robot.readData(1)
		#print frontRightData
		frontRightData = struct.unpack('B', frontRightData)[0]
		#Gets data from the right cliff sensor
		self.robot.sendMult([self.sensors, self.rightCliff])
		rightData = self.robot.readData(1)
		#print rightData
		rightData = struct.unpack('B', rightData)[0]
		cliffData = [bool(leftData & 0x01), bool(frontLeftData & 0x01), bool(frontRightData & 0x01), bool(rightData & 0x01)]
		#print cliffData
		return cliffData
	def getDistance(self):
		self.robot.sendMult([self.sensors, self.distanceSensor])
		dist = self.robot.readData(2)
		dist = struct.unpack('h', dist)[0]
		self.appendLogFile(str(time.ctime(time.time())+','+str(dist)+'\n'))
		return dist
	def getAngle(self):
		self.robot.sendMult([self.sensors, self.angleSensor])
		angle = self.robot.readData(2)
		angle = struct.unpack('h', angle)[0]
		self.appendLogFile(str(time.ctime(time.time())+','+str(angle)+'\n'))
		return angle
	def directDrive(self, rightVelocity, leftVelocity, sec):
		right = self.getBytes(rightVelocity)
		left = self.getBytes(leftVelocity)
		#print right
		#print left
		#self.playSong(0)
		if(self.canContinue):
			self.robot.sendMult([self.driveDirect, right[0], right[1], left[0], left[1]])
			self.sleepCheck(sec)
			self.stopDrive()
			print "stopped"
		else:
			while True:
				x = self.stateOfButtons()
				if(x[7]):
					self.canContinue = True
					return
	def directDriveRotate(self, rightVelocity, leftVelocity, sec):
		right = self.getBytes(rightVelocity)
		left = self.getBytes(leftVelocity)
		#print right
		#print left
		if(self.canContinue):
			self.robot.sendMult([self.driveDirect, right[0], right[1], left[0], left[1]])
			run = time.time()+sec
			while (time.time() < run):
				a = self.stateOfButtons()
				b = self.getBumpsAndWheelDrops()
				if(a[7] or b[0] or b[1]):
					self.stopDrive()
					if(a[7]):
						self.appendLogFile(str(time.ctime(time.time())+',BUTTON\n'))
						self.playSong(2)
						time.sleep(4)
						self.canContinue = False
					else:
						self.appendLogFile(str(time.ctime(time.time())+',UNSAFE\n'))
					if(b[0] or b[1]):
						self.playSong(2)
						time.sleep(3)
						exit()
			self.stopDrive()
		else:
			while True:
				x = self.stateOfButtons()
				if(x[7]):
					self.canContinue = True
					return
	def getBytes(self, data):
		Bytes = [0, 0]
		if(data > 0):
			if(data > 255):
				Bytes[0] = 1
				Bytes[1] = data-256
			else:
				Bytes[1] = data
			return Bytes
		else:
			data = struct.pack('P', data)
			Bytes[0] = struct.unpack('B', data[1])[0]
			Bytes[1] = struct.unpack('B', data[0])[0]
			return Bytes
	def rotateRandom180(self):
		angle = random.randint(150, 210)
		dist = (angle*self.robotCircumference)/360
		tim = self.calcTime(dist, 500)
		x = self.getBumpsAndWheelDrops()
		if(x[2] and not x[3]):
			self.directDriveRotate(-500, 500, tim)
		elif(x[3] and not x[2]):
			self.directDriveRotate(500, -500, tim)
		elif(x[3] and x[2]):
			a = [-1, 1]
			b = random.randint(0,1)
			b = a[b]
			self.directDrive(500*b, 500*b*-1, tim)
	def calcTime(self, distance, vel):
		return distance/vel
	def createSongs(self):
		#Song 0 Fur Elise
		print 'Writing Song 0 -- Fur Elise by Beethoven'
		self.robot.sendMult([self.song, 0, 9, self.furElise[0], self.noteLength, self.furElise[1], self.noteLength, self.furElise[2], self.noteLength,
		self.furElise[3], self.noteLength, self.furElise[4], self.noteLength, self.furElise[5], self.noteLength, self.furElise[6], self.noteLength,
		self.furElise[7], self.noteLength, self.furElise[8], self.noteLength*2])
		print 'Done'
		#Song 1 Harry Potter
		print 'Writing Song 1 -- Harry Potter Theme'
		self.robot.sendMult([self.song, 1, 11, self.harryPotter[0], self.noteLength, self.harryPotter[1], self.noteLength*2, self.harryPotter[2], self.noteLength, self.harryPotter[3], self.noteLength,
		self.harryPotter[4], self.noteLength*3, self.harryPotter[5], self.noteLength*4, self.harryPotter[6], self.noteLength*4, self.harryPotter[7], self.noteLength*2, self.harryPotter[8], self.noteLength,
		self.harryPotter[9], self.noteLength, self.harryPotter[10], self.noteLength*4])
		print 'Done'
		#Song 2 Flash Theme
		print 'Writing Song 2 -- The Flash by the CW Theme'
		self.robot.sendMult([self.song, 2, 16, self.flashTheme[0], self.noteLength/2, self.flashTheme[1], self.noteLength/2, self.flashTheme[2], self.noteLength/2, self.flashTheme[3], self.noteLength/2,
		self.flashTheme[4], self.noteLength/2, self.flashTheme[5], self.noteLength/2, self.flashTheme[6], self.noteLength/2, self.flashTheme[7], self.noteLength/2, self.flashTheme[8], self.noteLength/2,
		self.flashTheme[9], self.noteLength/2, self.flashTheme[10], self.noteLength/2, self.flashTheme[11], self.noteLength/2, self.flashTheme[12], self.noteLength/2, self.flashTheme[13], self.noteLength/2,
		self.flashTheme[14], self.noteLength/2, self.flashTheme[15], self.noteLength/2])
		print 'Done'
		#Song 3 Fairy Tail Anime Theme song
		print 'Writing Song 3 -- Fairy Tail Theme song'
		self.robot.sendMult([self.song, 3, 16, self.fairyTail[0], self.noteLength, self.fairyTail[1], self.noteLength/2, self.fairyTail[2], self.noteLength/2, self.fairyTail[3], self.noteLength,
		self.fairyTail[4], self.noteLength, self.fairyTail[5], self.noteLength, self.fairyTail[6], self.noteLength/2, self.fairyTail[7], self.noteLength/2, self.fairyTail[8], self.noteLength, 
		self.fairyTail[9], self.noteLength, self.fairyTail[10], self.noteLength, self.fairyTail[11], self.noteLength/2, self.fairyTail[12], self.noteLength/2, self.fairyTail[13], self.noteLength,
		self.fairyTail[14], self.noteLength, self.fairyTail[15], self.noteLength])
		print 'Done'
		time.sleep(2)
	def playSong(self, num):
		self.robot.sendMult([self.play, num])
	def sleepCheck(self, sec):
		run = time.time()+sec
		while(time.time() < run):
			#print 'checking'
			a = self.stateOfButtons()
			b = self.getBumpsAndWheelDrops()
			c = self.checkCliffs()
			#print c
			#print a
			if(a[7] or b[0] or b[1] or b[2] or b[3] or c[0] or c[1] or c[2] or c[3]):
				#print 'Stop Attempt'
				self.stopDrive()
				if(a[7]):
					self.appendLogFile(str(time.ctime(time.time())+',BUTTON\n'))
					self.playSong(2)
					time.sleep(4)
					self.canContinue = False
				else:
					self.appendLogFile(str(time.ctime(time.time())+',UNSAFE\n'))
					if(b[0] or b[1]):
						self.playSong(3)
						time.sleep(4)
						self.saveLogFile()
						exit()
					if(c[0] or c[1] or c[2] or c[3]):
						self.playSong(1)
						time.sleep(4)
						self.canContinue = False
				return
	def stopDrive(self):
		#print 'Stopping'
		self.robot.sendMult([self.drive, 0, 0, 0, 0])
	#This fumction takes in 4 integers and a float then usese the srive opcode to send the robot its velocity turning radius and how long to continue the motion
	def drives(self, velocity, radius, sec):
		vel = self.getBytes(velocity)
		rad = self.getBytes(radius)
		self.robot.sendMult([self.drive, vel[0], vel[1], rad[0], rad[1]])
		self.sleepCheck(sec)
		self.stopDrive()
	def appendLogFile(self, line):
		self.logFile.write(line)
	def saveLogFile(self):
		self.logFile.close()
