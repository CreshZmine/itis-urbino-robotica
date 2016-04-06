import RoboSerial
import time

robo = RoboSerial.RoboSerial()

print (robo.openConnection())

#print robo.goForward()
#print robo.goBack()
#print robo.goBackGrad()
#print robo.goRight()
#print robo.goLeft()
#print robo.goStop()
#for i in range(1, 10):
#sens = [1,2,4,5]
while True:
    for i in range(1,6):
#   for s in sens:
        print str(i) + str(robo.requestSensor(i)) + " ",
    print ''
    time.sleep(0.1)
