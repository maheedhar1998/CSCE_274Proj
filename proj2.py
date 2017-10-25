import time
import rInterface
iRobot = rInterface.rInterface()
iRobot.changeState('start')
iRobot.changeState('full')
iRobot.playSong(0)
time.sleep(4)
iRobot.playSong(1)
time.sleep(4)
iRobot.playSong(2)
time.sleep(4)
iRobot.playSong(3)
time.sleep(4)
while True:
	iRobot.directDrive(100, 100, 500)
	iRobot.getDistance()
	iRobot.getAngle()
	#print "rotating"
	iRobot.rotateRandom180()
	iRobot.getDistance()
	iRobot.getAngle()
