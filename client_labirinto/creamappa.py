import movimenti
import math
import pyglet
from pyglet.gl import *

robot = movimenti.Robo_moves()
mappa=[[False for x in range(400)] for x in range(400)]
x = 200
y = 200
theta = math.pi/2

def elabora_sensore(theta):
    dist = float(robot.sense(0))
    x_coor = x+dist*math.cos(theta)
    y_coor = y+dist*math.sin(theta)
    print "Punto a:"
    print "X: " + str(int(x_coor))
    print "Y: " + str(int(y_coor))
    if not(int(x_coor) >= 400 or int(x_coor) < 0 or int(y_coor) >= 400 or int(y_coor) < 0):
        mappa[int(x_coor)][int(y_coor)] = True
        print "Passato"

def quadro():
    d = 4.0
    for x in range(400):
        for y in range(400):
            if mappa[x][y] == True:
                glBegin(GL_LINE_STRIP)
                glVertex2f(x-d, y-d)
                glVertex2f(x-d, y+d)
                glVertex2f(x+d, y+d)
                glVertex2f(x+d, y-d)
                glVertex2f(x-d, y-d)
                glEnd()

win = pyglet.window.Window()

while theta <  math.pi*5/2:
    elabora_sensore()
    robot.turn(0.052)
    theta += 0.052
    print str(theta)

robot.termina()

@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    quadro()

pyglet.app.run()
