#!/usr/python

import RoboSerial

robo = RoboSerial.RoboSerial()
robo.openConnection()


while True:
    print "--> "
    input = raw_input()
    try:
        print robo.requestSensor(int(input))
    except:
        pass
    if input == "stop":
        break
