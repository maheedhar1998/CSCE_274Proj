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
		self.noteLength = 16
		self.isMoving = False
		self.canMove = False
		self.canContinue = True
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
		print leftData
		leftData = struct.unpack('B', leftData)[0]
		#Gets data from the front left cliff sensor
		self.robot.sendMult([self.sensors, self.frontLeftCliff])
		frontLeftData = self.robot.readData(1)
		print frontLeftData
		frontLeftData = struct.unpack('B', leftData)[0]
		#Gets data from the front right cliff sensor
		self.robot.sendMult([self.sensors, self.frontRightCliff])
		frontRightData = self.robot.readData(1)
		print frontRightData
		frontRightData = struct.unpack('B', leftData)[0]
		#Gets data from the right cliff sensor
		self.robot.sendMult([self.sensors, self.rightCliff])
		rightData = self.robot.readData(1)
		print rightData
		rightData = struct.unpack('B', leftData)[0]
		cliffData = [bool(leftData & 0x01), bool(frontLeftData & 0x01), bool(frontRightData & 0x01), bool(rightData & 0x01)]
		return cliffData
	def getDistance(self):
		self.robot.sendMult([self.sensors, self.distanceSensor])
		dist = self.robot.readData(2)
		dist = struct.unpack('h', dist)
		return dist
	def getAngle(self):
		self.robot.sendMult([self.sensors, self.angleSensor])
		angle = self.robot.readData(2)
		angle = struct.unpack('h', angle)
		return angle
	def directDrive(self, rightVelocity, leftVelocity, sec):
		right = self.getBytes(rightVelocity)
		left = self.getBytes(leftVelocity)
		self.robot.sendMult([self.driveDirect, right[0], right[1], left[0], left[1]])
		self.sleepCheck(sec)
		self.stopDrive()
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
			data = data*-1
			data = data ^ 0xFFFFFFFF
			data = data+1
			if(data > 255):
				Bytes[0] = 1
				Bytes[1] = data-256
			else:
				Bytes[1] = data
			return Bytes
	def rotateRandom180(self):
		angle = random.randint(150, 210)
		
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
	def playSong(self, num):
		self.robot.sendMult([self.play, num])
	def sleepCheck(self, sec):
		run = time.time()+sec
		while(time.time() < run):
			print 'checking'
			a = self.stateOfButtons()
			b = self.getBumpsAndWheelDrops()
			#c = self.checkCliffs()
			if(a[7] or b[0] or b[1] or b[2] or b[3])# or c[0] or c[1] or c[2] or c[3]):
				self.stopDrive()
		print 'done'
	def stopDrive(self):
		self.robot.sendMult([self.directDrive, 0, 0, 0, 0])
	#This fumction takes in 4 integers and a float then usese the srive opcode to send the robot its velocity turning radius and how long to continue the motion
	def drives(self, velocity, radius, sec):
		if(self.canContinue == True):
			vel = self.getBytes(velocity)
			rad = self.getBytes(radius)
			self.robot.sendMult([self.drive, vel[0], vel[1], rad[0], rad[1]])
			self.sleepCheck(sec)
			self.stopDrive()
