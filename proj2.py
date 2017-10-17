import rInterface
iRobot = rInterface()
iRobot.changeState('start')
iRobot.changeState('full')
iRobot.createSongs()
iRobot.playSong(0)
