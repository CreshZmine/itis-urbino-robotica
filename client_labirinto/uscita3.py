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
Una "casella" e' di 0.033 (1/30) cm
'''

'''
robot[0] = x
robot[1] = y
'''
robot = [MAX_MAP/2, MAX_MAP/2]

mov = RoboSerial.RoboSerial()
mov.openConnection()

sensori_distanza = []
sensori_distanza.append(sensore.Sensore(1, mov))    #Sensore davanti
sensori_distanza[-1].dx = 0
sensori_distanza[-1].dy = 5/30.0
sensori_distanza[-1].offset = 0
sensori_distanza.append(sensore.Sensore(2, mov))    #Sensore destra-alto
sensori_distanza[-1].dx = 7.5/30.0
sensori_distanza[-1].dy = 5/30.0
sensori_distanza[-1].offset = -math.pi/2
sensori_distanza.append(sensore.Sensore(3, mov))    #Sensore destra-basso
sensori_distanza[-1].dx = 7.5/30.0
sensori_distanza[-1].dy = -5/30.0
sensori_distanza[-1].offset = -math.pi/2
sensori_distanza.append(sensore.Sensore(4, mov))    #Sensore sinistra-alto
sensori_distanza[-1].dx = -7.5/30.0
sensori_distanza[-1].dy = 5/30.0
sensori_distanza[-1].offset = math.pi/2
sensori_distanza.append(sensore.Sensore(5, mov))    #Sensore sinistra-basso
sensori_distanza[-1].dx = -7.5/30.0
sensori_distanza[-1].dy = -5/30.0
sensori_distanza[-1].offset = math.pi/2

sensore_angolo = sensore.Sensore(6, mov)
sensore_luminosita = sensore.Sensore(7, mov)

sensore_temperatura = sensore.Sensore(8, mov)

sensore_velocita = sensore.Sensore(9, mov)
sensore_distanza_p = sensore.Sensore(10, mov) #Distanza percorsa

def elabora_sensore(theta, sensore):
    '''
    theta e' l'angolo del robot rispetto al punto iniziale
    sensore e' il sensore da analizzare
    '''
    dist = sensore.leggi()
    dist /= 30.0 #Lo porto nella unita di misura "casella"
    x_sensore = robot[0]+sensore.dx*math.cos(theta)-sensore.dy*math.sin(theta)
    y_sensore = robot[1]+sensore.dx*math.sin(theta)+sensore.dy*math.cos(theta)
    x_coor = x_sensore+dist*math.cos(theta+sensore.offset)
    y_coor = y_sensore+dist*math.sin(theta+sensore.offset)

    x_coor_approx = int(math.ceil(x_coor)) if (x_coor % 1) > 0.5 else int(math.floor(x_coor))
    y_coor_approx = int(math.ceil(y_coor)) if (y_coor % 1) > 0.5 else int(math.floor(y_coor))
    prima_casella = (math.trunc(x_coor), math.trunc(y_coor))
    if maht.fabs(y_coor_approx - y_coor) < maht.fabs(x_coor_approx - x_coor):
        seconda_casella = (prima_casella[0], prima_casella[1] + (1 if (y_coor % 1) > 0.5 else -1))
    else:
        seconda_casella = (prima_casella[0] + (1 if (x_coor % 1) > 0.5 else -1), prima_casella[1])
    muri += (prima_casella, seconda_casella)
    #imposto le caselle tra la mia posizione e il rilevamento a 0 (vuoto)
    dx, dy = math.cos(theta+sensore.offset), math.sin(theta+sensore.offset)
    cx, cy = dx, dy
    for i in range(dist):
        try:
            grid[int(x_sensore + cx)][y_sensore + cy] = 1
        except IndexError:
            pass
        cx, cy = cx+dx, cy+dy

def elabora_velocita(theta, distanza_precedente, distanza_corrente, sensore_velocita):
    '''
    Aggiorna la posizione del robot tenendo conto della velocita
    '''
    delta_distanza = distanza_corrente - distanza_precedente
    delta_distanza /= 30.0
    robot[0] += delta_distanza*math.cos(theta)
    robot[1] += delta_distanza*math.sin(theta)


#moves = movimenti.Robo_moves()

'''
1 - vuoto
2 - non esplorato

grid viene inizializzato come non esplorato
Una cella di grid è di 30 cm
'''
grid = [[int(2) for x in xrange(MAX_MAP+1)] for y in xrange(MAX_MAP+1)]

'''
[((1,1),(1,2)),((3,2),(2,2))]
    ^     ^
    |     |
    -------
'''
muri = []

theta = sensore_angolo.leggi()*math.pi/180;

distanza_precedente = sensore_distanza_p.leggi();

while True:
    for s in sensori_distanza:
        elabora_sensore(theta, s)
    distanza_corrente = sensore_distanza_p.leggi()
    elabora_velocita(theta, distanza_precedente, distanza_corrente, sensore_velocita)
    distanza_precedente = distanza_corrente
