import RoboSerial
import time

robo = RoboSerial.RoboSerial()

#print (robo.openConnection())

while True:
	print ("== Debug RoboSerial ==")
	print ("1 Forward")
	print ("2 Left")
	print ("3 Right")
	print ("4 Back")
	print ("5 Stop")
	print ("6 Sensor single test")
	print ("7 Sensor non-stop test")
	print ("0 Exit")
	print (" ")

	sel = raw_input()

	print (" ")

	if(sel == '1'):
		print robo.goForward()

	if(sel == '2'):
		print robo.goLeft()
	if(sel == '3'):
		print robo.goRight()
	if(sel == '4'):
		print robo.goBack()
	if(sel == '5'):
		print robo.goStop()
	if(sel == '6'):
		for i in range(1,11):
			print str(i) + str(robo.requestSensor(i)) + " ",
			print " "
	if(sel == '7'):
		while True:
			for i in range(1,11):
				print str(i) + str(robo.requestSensor(i)) + " ",
			print " "
			time.sleep(0.1)
	if(sel == '0'):
		break
	print (" ")
