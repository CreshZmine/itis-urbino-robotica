import RoboSerial

robo = RoboSerial.RoboSerial()

robo.goForward()
robo.goBack()
robo.goBackGrad()
robo.goRight()
robo.goLeft()
robo.goStop()
for i in range(1, 10):
    robo.requestSensor(i)
