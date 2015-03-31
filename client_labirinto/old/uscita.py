#!/usr/bin/python
import mapper
import pyglet
from pyglet.gl import *
import random
import movimenti
import math
import sys

def checkValidita(coor):
    if grid[coor[0]][coor[1]] == 1:
        return False
    return True

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

random.seed()

robot[0] = sys.argv[3]
robot[1] = sys.argv[4]
robo_dx = math.cos(math.radians((float(sys.argv[5]))))
robo_dy = math.sin(math.radians((float(sys.argv[5]))))
nodi_grafo = []
#moves = movimenti.Robo_moves()

#'''
#0 - vuoto
#1 - muro
#2 - non esplorato

#grid viene inizializzato come non esplorato
#'''
#grid = [[int(2) for x in xrange(401)] for y in xrange(401)]
grid = [[int(0) for x in xrange(401)] for y in xrange(401)]
for point in mappa:
    grid[int(point[0])][int(point[1])] = 1

for i in range(100):
    valido = False
    while not valido:
        coor = (random.randint(0, 400), random.randint(0, 400))
        valido = checkValidita(coor)
    nodi_grafo.append(coor)

def nodi():
    d = 4.0
    for x,y in nodi_grafo:
            glBegin(GL_LINE_STRIP)
            glColor3f(255,0,0)
            glVertex2f(x-d, y-d)
            glVertex2f(x-d, y+d)
            glVertex2f(x+d, y+d)
            glVertex2f(x+d, y-d)
            glVertex2f(x-d, y-d)
            glEnd()


def quadro():
    d = 4.0
    for x in range(401):
        for y in range(401):
            if grid[x][y] == True:
                glBegin(GL_LINE_STRIP)
                glColor3f(255,255,255)
                glVertex2f(x-d, y-d)
                glVertex2f(x-d, y+d)
                glVertex2f(x+d, y+d)
                glVertex2f(x+d, y-d)
                glVertex2f(x-d, y-d)
                glEnd()

win = pyglet.window.Window()

@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    quadro()
    nodi()

pyglet.app.run()
