import rInterface
iRobot = rInterface.rInterface()
iRobot.changeState('start')
iRobot.changeState('safe')
while True:
	iRobot.alignToWall()
	iRobot.directDrive(50,50,100)
