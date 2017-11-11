import rInterface
iRobot = rInterface.rInterface()
iRobot.changeState('start')
iRobot.changeState('safe')
"""if front right is greater than 1 and center right is greater than 0 then it is a left turn
if center right is zero and front right is zero then right turn"""
iRobot.directDrive(100,100,100)
