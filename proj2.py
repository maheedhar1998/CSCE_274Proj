import time
import rInterface
iRobot = rInterface.rInterface()
iRobot.changeState('start')
iRobot.changeState('full')
while True:
	iRobot.directDrive(100, 100, 500)
	iRobot.rotateRandom180()
