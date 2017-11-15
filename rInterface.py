#imports the time python module
import time
#imports the struct python module
import struct
#imports the random pyhton module
import random
import math
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
		self.lightBumpers = 45
		self.lightBumpLeft = 46
		self.lightBumpFrontLeft = 47
		self.lightBumpCenterLeft = 48
		self.lightBumpCenterRight = 49
		self.lightBumpFrontRight = 50
		self.lightBumpRight = 51
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
		self.setPoint = 23
		self.kp = 1
		self.kd = .1
		self.error = 0
		self.prevError = 0
		self.createSongs()
		self.playSong(0)
		time.sleep(5)
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
	"""This function takes in an instance of the object and returns a list of booleans that determine whether or not the buttons are pressed
	The list will be interpretted in this order: [Clock, Schedule, Day, Hour, Minute, Dock, Spot, Clean]
	The hexadecimal numbers in this function are interpreted from the info in the roomba open interface spec"""
	def stateOfButtons(self):
		self.robot.sendMult([self.sensors, self.buttonPacketID])
		data = self.robot.readData(1)
		data = struct.unpack('B', data)[0]
		return [bool(data & 0x80), bool(data & 0x40), bool(data & 0x20), bool(data & 0x10), bool(data & 0x08), bool(data & 0x04), bool(data & 0x02), bool(data & 0x01)]
	#returns data from the bumps and wheel drop sensors
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
	#This function checks for cliffs
	def checkCliffs(self):
		#Gets data from the left cliff sensor
		self.robot.sendMult([self.sensors, self.leftCliff])
		leftData = self.robot.readData(1)
		leftData = struct.unpack('B', leftData)[0]
		#Gets data from the front left cliff sensor
		self.robot.sendMult([self.sensors, self.frontLeftCliff])
		frontLeftData = self.robot.readData(1)
		frontLeftData = struct.unpack('B', frontLeftData)[0]
		#Gets data from the front right cliff sensor
		self.robot.sendMult([self.sensors, self.frontRightCliff])
		frontRightData = self.robot.readData(1)
		frontRightData = struct.unpack('B', frontRightData)[0]
		#Gets data from the right cliff sensor
		self.robot.sendMult([self.sensors, self.rightCliff])
		rightData = self.robot.readData(1)
		rightData = struct.unpack('B', rightData)[0]
		cliffData = [bool(leftData & 0x01), bool(frontLeftData & 0x01), bool(frontRightData & 0x01), bool(rightData & 0x01)]
		return cliffData
	#get the distance from the distance and unpacks that data into and int
	def getDistance(self):
		self.robot.sendMult([self.sensors, self.distanceSensor])
		dist = self.robot.readData(2)
		dist = struct.unpack('>h', dist)[0]
		self.appendLogFile(str(time.ctime(time.time())+', distance: '+str(dist)+'\n'))
		return dist
	#return data from the angle sensor
	def getAngle(self):
		self.robot.sendMult([self.sensors, self.angleSensor])
		angle = self.robot.readData(2)
		angle = struct.unpack('>h', angle)[0]
		self.appendLogFile(str(time.ctime(time.time())+', angle: '+str(angle)+'\n'))
		return angle
	#implimenting drive direct and sets the velocity of the wheels. ALso stops the robot after a given amount of time
	def directDrive(self, rightVelocity, leftVelocity, sec):
		right = self.getBytes(rightVelocity)
		left = self.getBytes(leftVelocity)
		if(self.canContinue):
			self.robot.sendMult([self.driveDirect, right[0], right[1], left[0], left[1]])
			self.sleepCheck(sec)
			return
		else:
			while True:
				x = self.stateOfButtons()
				#if clean button is pressed
				if(x[7]):
					#initates the while loop
					self.canContinue = True
					self.directDrive(rightVelocity, leftVelocity, sec)
					return
	"""defining the robots rotation
	checks all sensors except for cliffs and bumps while rotating"""
	def directDriveRotate(self, rightVelocity, leftVelocity, sec):
		right = self.getBytes(rightVelocity)
		left = self.getBytes(leftVelocity)
		if(self.canContinue):
			self.robot.sendMult([self.driveDirect, right[0], right[1], left[0], left[1]])
			run = time.time()+sec-.075
			while (time.time() < run):
				a = self.stateOfButtons()
				b = self.getBumpsAndWheelDrops()
				c = self.calcPDVal(self.getLightBumpRight())
				d = self.getLightBumpers()
				if(self.getLightBumpRight()<2):
					self.drivesAround()
					return
				if(d[2]):
					self.rotateAngle(100,90)
					return
				#if the clean button is pressed or if the wheel drop sensors specified return true then stop driving
				if(a[7] or b[0] or b[1] or c<5 and c>-5):
					#this is specifically for the clean button:
					if(a[7]):
						self.appendLogFile(str(time.ctime(time.time())+',BUTTON\n'))
						self.playSong(1)
						time.sleep(4)
						self.canContinue = False
						self.stopDrive()
						return
					#and this is specifically for the wheel drop sensors:
					else:
						self.appendLogFile(str(time.ctime(time.time())+',UNSAFE\n'))
						return
					if(b[0] or b[1]):
						self.playSong(3)
						time.sleep(3)
						exit()
		else:
			while True:
				x = self.stateOfButtons()
				if(x[7]):
					self.canContinue = True
					self.directDriveRotate(rightVelocity, leftVelocity, sec)
					return
	"""takes in an int and splits into seprerate bytes
	just to make it easier for the user so you don't have to set the individual byte code for each velocity"""
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
	#tells the robot how much to rotate based of a random angle between 150 and 210 degrees
	def rotateRandom180(self, vel):
		angle = random.randint(150, 210)
		dist = (angle*self.robotCircumference)/360
		tim = self.calcTime(dist, vel)
		#after getting the bumps and wheel drops data and determines which direction to turn based of that data
		x = self.getBumpsAndWheelDrops()
		if(x[2] and not x[3]):
			self.directDriveRotate(vel*-1, vel, tim)
		elif(x[3] and not x[2]):
			self.directDriveRotate(vel, vel*-1, tim)
		#if both bump sensors are pressed then it determines a random direction to turn
		elif(x[3] and x[2]):
			a = [-1, 1]
			b = random.randint(0,1)
			b = a[b]
			self.directDriveRotate(vel*b, vel*b*-1, tim)
	#this function rotates the robot in palce a given angle
	def rotateAngle(self, vel, angle):
		dist = (angle*self.robotCircumference)/360
		tim = self.calcTime(dist, vel)
		#after getting the bumps and wheel drops data and determines which direction to turn based of that data
		x = self.getBumpsAndWheelDrops()
		if(x[2] and not x[3]):
			self.directDriveRotate(vel*-1, vel, tim)
		elif(x[3] and not x[2]):
			self.directDriveRotate(vel, vel*-1, tim)
		#if both bump sensors are pressed then it determines a random direction to turn
		elif(x[3] and x[2]):
			a = [-1, 1]
			b = random.randint(0,1)
			b = a[b]
			self.directDriveRotate(vel*b, vel*b*-1, tim)
		else:
			self.directDriveRotate(vel, vel*-1, tim)
	#This function calcualtes time based on distance and velocity
	def calcTime(self, distance, vel):
		return abs(distance/vel)
	#creates songs
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
	#plays Songs
	def playSong(self, num):
		self.robot.sendMult([self.play, num])
	#checks for buttons, bumps, cliffs, and wheeldrops
	def sleepCheck(self, sec):
		run = time.time()+sec-.075
		#while loop runs until the current time = the goal time
		while(time.time() < run):
			a = self.stateOfButtons()
			b = self.getBumpsAndWheelDrops()
			c = self.checkCliffs()
			d = self.calcPDVal(self.getLightBumpRight())
			e = self.getLightBumpRight()
			f = self.getLightBumpers()
			if(e < 2):
				self.drivesAround()
				return
			if(f[2]):
				self.rotateAngle(100,90)
				return
			#while it is running, it checks for the following sensors and stops driving if they return true
			if(a[7] or b[0] or b[1] or b[2] or b[3] or c[0] or c[1] or c[2] or c[3]  or d>5 or d<-5):
				#the following is for the clean button
				if(a[7]):
					self.appendLogFile(str(time.ctime(time.time())+',BUTTON\n'))
					self.playSong(1)
					time.sleep(4)
					self.canContinue = False
					self.stopDrive()
					return
				else:
					self.appendLogFile(str(time.ctime(time.time())+',UNSAFE\n'))
					b = self.getBumpsAndWheelDrops()
					#the following is for the wheel drop
					if(b[0] or b[1]):
						self.playSong(3)
						time.sleep(4)
						self.saveLogFile()
						exit()
					#the following is for the cliff sensors
					elif(c[0] or c[1] or c[2] or c[3]):
						self.playSong(2)
						time.sleep(4)
						self.canContinue = False
					return
				return
	#stops the robot
	def stopDrive(self):
		self.robot.sendMult([self.drive, 0, 0, 0, 0])
	#This function takes in 4 integers and a float then usese the srive opcode to send the robot its velocity turning radius and how long to continue the motion
	def drives(self, velocity, radius, sec):
		vel = self.getBytes(velocity)
		rad = self.getBytes(radius)
		self.robot.sendMult([self.drive, vel[0], vel[1], rad[0], rad[1]])
		self.sleepCheck(sec)
		self.stopDrive()
	#This function drives around walls
	def drivesAround(self):
		byte = self.getBytes(-280)
		self.robot.sendMult([self.drive, 0, 100, byte[0], byte[1]])
		while True:
			a = self.calcPDVal(self.getLightBumpRight())
			b = self.getLightBumpers()
			if(a<5 and a>-5 or b[2]):
				return
	#this function return a list of booleans that tell you which light bump sensors detect walls
	def getLightBumpers(self):
		self.robot.sendMult([self.sensors, self.lightBumpers])
		lightBump = self.robot.readData(1)
		lightBump = struct.unpack('B', lightBump)[0]
		return [bool(lightBump&0x20), bool(lightBump&0x10), bool(lightBump&0x08), bool(lightBump&0x04), bool(lightBump&0x02), bool(lightBump&0x01)]
	#The following get the data form the corresponding light bump sensors
	def getLightBumpLeft(self):
		self.robot.sendMult([self.sensors, self.lightBumpLeft])
		leftBump = self.robot.readData(2)
		leftBump = struct.unpack('>H', leftBump)[0]
		leftBump = math.sqrt(leftBump)
		return leftBump
	def getLightBumpFrontLeft(self):
		self.robot.sendMult([self.sensors, self.lightBumpFrontLeft])
		frontLeftBump = self.robot.readData(2)
		frontLeftBump = struct.unpack('>H', frontLeftBump)[0]
		frontLeftBump = math.sqrt(frontLeftBump)
		return frontLeftBump
	def getLightBumpCenterLeft(self):
		self.robot.sendMult([self.sensors, self.lightBumpCenterLeft])
		centerLeftBump = self.robot.readData(2)
		centerLeftBump = struct.unpack('>H', centerLeftBump)[0]
		centerLeftBump = math.sqrt(centerLeftBump)
		return centerLeftBump
	def getLightBumpCenterRight(self):
		self.robot.sendMult([self.sensors, self.lightBumpCenterRight])
		centerRightBump = self.robot.readData(2)
		centerRightBump = struct.unpack('>H', centerRightBump)[0]
		centerRightBump = math.sqrt(centerRightBump)
		return centerRightBump
	def getLightBumpFrontRight(self):
		self.robot.sendMult([self.sensors, self.lightBumpFrontRight])
		frontRightBump = self.robot.readData(2)
		frontRightBump = struct.unpack('>H', frontRightBump)[0]
		frontRightBump = math.sqrt(frontRightBump)
		return frontRightBump
	def getLightBumpRight(self):
		self.robot.sendMult([self.sensors, self.lightBumpRight])
		rightBump = self.robot.readData(2)
		rightBump = struct.unpack('>H', rightBump)[0]
		rightBump = math.sqrt(rightBump)
		return rightBump
	#the following calculates the PD Value
	def calcPDVal(self, current):
		self.error = self.setPoint-current
		pVal = self.kp*self.error
		dVal = self.kd*(self.error-self.prevError)
		self.prevError = self.error
		PDVal = pVal+dVal
		return PDVal
	#This function Aligns the robot to the wall
	def alignToWall(self):
		a = self.calcPDVal(self.getLightBumpRight())
		if(a>5):
			self.directDriveRotate(-50,50,100)
		elif(a<-5):
			self.directDriveRotate(50,-50,100)
	#The following append and save the log file
	def appendLogFile(self, line):
		self.logFile.write(line)
	def saveLogFile(self):
		self.logFile.close()
