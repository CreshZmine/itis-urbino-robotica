#!/usr/bin/python
import mapper
import random
import movimenti
import math
import sys

def tp(x,y):
    return math.sqrt(x*x+y*y)

def distanza((x0,y0),(x1,y1)):
    dx =x1-x0
    dy =y1-y0
    return tp(dx,dy)

if len(sys.argv) < 6:
    print "Usage: python " + sys.argv[0] + " x_uscita y_uscita x_robot y_robot angle"
    exit(1)

mappa, robot = mapper.parseMapFile("mappaDef.map")

robot[0] = sys.argv[3]
robot[1] = sys.argv[4]
robo_dx = math.cos(math.radians((float(sys.argv[5]))))
robo_dy = math.sin(math.radians((float(sys.argv[5]))))
moves = movimenti.Robo_moves()


