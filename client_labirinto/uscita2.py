#!/usr/bin/python
from pyglet.gl import *
import math
import pyglet
import random
import RoboSerial
import sensore
import sys
import time

'''
MAX_MAP e' la grandezza della mappa
'''
MAX_MAP = 400

'''
robot[0] = x
robot[1] = y
'''
robot = [MAX_MAP/2, MAX_MAP/2]

robo_dx = 0
robo_dy = 1

mov = RoboSerial.RoboSerial()
mov.openConnection()

sensori_distanza = []
sensori_distanza.append(sensore.Sensore(1, mov))    #Sensore davanti
sensori_distanza[-1].dx = 0
sensori_distanza[-1].dy = 5
sensori_distanza[-1].offset = 0
sensori_distanza.append(sensore.Sensore(2, mov))    #Sensore destra-alto
sensori_distanza[-1].dx = 7.5
sensori_distanza[-1].dy = 5
sensori_distanza[-1].offset = -math.pi/2
sensori_distanza.append(sensore.Sensore(3, mov))    #Sensore destra-basso
sensori_distanza[-1].dx = 7.5
sensori_distanza[-1].dy = -5
sensori_distanza[-1].offset = -math.pi/2
sensori_distanza.append(sensore.Sensore(4, mov))    #Sensore sinistra-alto
sensori_distanza[-1].dx = -7.5
sensori_distanza[-1].dy = 5
sensori_distanza[-1].offset = math.pi/2
sensori_distanza.append(sensore.Sensore(5, mov))    #Sensore sinistra-basso
sensori_distanza[-1].dx = -7.5
sensori_distanza[-1].dy = -5
sensori_distanza[-1].offset = math.pi/2

sensore_angolo = sensore.Sensore(6, mov)
sensore_luminosita = sensore.Sensore(7, mov)

sensore_temperatura = sensore.Sensore(8, mov)
sensore_temperatura.angolo = 0

sensore_velocita = sensore.Sensore(9, mov)
sensore_distanza_p = sensore.Sensore(10, mov) #Distanza percorsa

def elabora_sensore(theta, sensore):
    '''
    theta e' l'angolo del robot rispetto al punto iniziale
    sensore e' il sensore da analizzare
    '''
    dist = sensore.leggi()
    x_sensore = robot[0]+sensore.dx*math.cos(theta)-sensore.dy*math.sin(theta)
    y_sensore = robot[1]+sensore.dx*math.sin(theta)+sensore.dy*math.cos(theta)
    x_coor = x_sensore+dist*math.cos(theta+sensore.offset)
    y_coor = y_sensore+dist*math.sin(theta+sensore.offset)
    if not(int(x_coor) >= MAX_MAP or int(x_coor) < 0 or int(y_coor) >= MAX_MAP or int(y_coor) < 0):
        grid[int(x_coor)][int(y_coor)] = 1
    #imposto le caselle tra la mia posizione e il rilevamento a 0 (vuoto)
    dx, dy = math.cos(theta+sensore.offset), math.sin(theta+sensore.offset)
    cx, cy = dx, dy
    for i in range(dist):
        grid[int(x_sensore + cx)][y_sensore + cy] = 0
        cx, cy = cx+dx, cy+dy

def elabora_velocita(theta, distanza_precedente, distanza_corrente, sensore_velocita):
    '''
    Aggiorna la posizione del robot tenendo conto della velocita
    '''
    delta_distanza = distanza_corrente - distanza_precedente
    robot[0] += delta_distanza*math.cos(theta)
    robot[1] += delta_distanza*math.sin(theta)

#moves = movimenti.Robo_moves()

'''
0 - vuoto
1 - muro
2 - non esplorato

grid viene inizializzato come non esplorato
'''
grid = [[int(2) for x in xrange(MAX_MAP+1)] for y in xrange(MAX_MAP+1)]

theta = math.pi/2;

distanza_precedente = 0

while True:
    for s in sensori_distanza:
        elabora_sensore(theta, s)
    distanza_corrente = sensore_distanza_p.leggi()
    elabora_velocita(theta, distanza_precedente, distanza_corrente, sensore_velocita)
    distanza_precedente = distanza_corrente
