#!/usr/bin/python
import pyglet
import time
from pyglet.gl import *
import random
import RoboSerial
import math
import sys

'''
robot[0] = x
robot[1] = y
'''
robot = [200, 200]

robo_dx = 0
robo_dy = 1

mov = RoboSerial.RoboSerial()
mov.openConnection()

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

def elabora_sensore(theta, angolo_sensore):
    '''
    theta e' l'angolo del robot rispetto al punto iniziale
    angolo_sensore e' l'angolo del sensore rispetto al davanti del robot
    '''
    dist = float(mov.sense(0))
    x_coor = robot[0]+dist*math.cos(theta+angolo_sensore)
    y_coor = robot[1]+dist*math.sin(theta+angolo_sensore)
    if not(int(x_coor) >= 400 or int(x_coor) < 0 or int(y_coor) >= 400 or int(y_coor) < 0):
        grid[int(x_coor)][int(y_coor)] = 1
    #imposto le caselle tra la mia posizione e il rilevamento a 0 (vuoto)
    dx, dy = math.cos(theta+angolo_sensore), math.sin(theta+angolo_sensore)
    cx, cy = dx, dy
    for i in range(dist):
        grid[int(robot[0] + cx)][robot[1] + cy] = 0
        cx, cy = cx+dx, cy+dy

def elabora_velocita(theta, t):
    vel_dritto = float(mov.sense(1)) #Cambiare 1 con il sensore di velocita
    vel = []
    vel.append(vel_dritto*math.cos(theta))
    vel.append(vel_dritto*math.sin(theta))
    dx, dy = map(lambda (x): x*t, vel)
    robot[0] += dx
    robot[1] += dy

#moves = movimenti.Robo_moves()

'''
0 - vuoto
1 - muro
2 - non esplorato

grid viene inizializzato come non esplorato
'''
grid = [[int(2) for x in xrange(401)] for y in xrange(401)]

theta = math.pi/2;

while True:
    start_time = time.time()
    elabora_sensore(theta, 0)
    elapsed = time.time() - start_time
    elabora_velocita(theta, elapsed)

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
    #nodi()

pyglet.app.run()
