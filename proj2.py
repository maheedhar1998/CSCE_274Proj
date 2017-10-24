import time
import rInterface
iRobot = rInterface.rInterface()
iRobot.changeState('start')
iRobot.changeState('full')
#while True :
	#x = iRobot.stateOfButtons()
	#y = iRobot.getBumpsAndWheelDrops()
	#z = iRobot.checkClass()
	#if(x[7] or y[0] or y[1] or y[2] or y[3] or z[0] or z[1] or z[2] or z[3]):
		#iRobot.directDrive(500, 500)
		#iRobot.rotateRandom180()
		#iRobot.directDrive(500, 500)
#x = iRobot.checkCliffs()
#iRobot.rotateRandom180()
while True:
	iRobot.directDrive(100, 100, 500)
	iRobot.rotateRandom180()
