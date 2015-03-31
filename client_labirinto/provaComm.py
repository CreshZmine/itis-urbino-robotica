import RoboSerial

robo = RoboSerial.RoboSerial()

print (robo.openConnection())

print robo.goForward()
print robo.goBack()
print robo.goBackGrad()
print robo.goRight()
print robo.goLeft()
print robo.goStop()
for i in range(1, 10):
    print robo.requestSensor(i)
