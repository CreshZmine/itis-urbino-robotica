#!/usr/bin/python
from pyglet.gl import *
import math
import pyglet
import random
import RoboSerial
import sensore
import sys
import time
import timer

'''
MAX_MAP e' la grandezza della mappa
'''
MAX_MAP = 400

'''
RAMP_SECONDS sono i secondi per cui deve salire
o scendere il robot per considerare quel tratto come rampa
RAMP_TOLL e' il grado dopo il quale il tratto viene considerato in pendenza
'''
RAMP_SECONDS = 2
RAMP_TOLL = 2

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
t = timer.Timer()

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

sensore_giroscopio = sensore.Sensore(11, mov)

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
    if math.sqrt((x_coor_approx-x_coor)**2+(y_coor_approx-y_coor)**2) > 1/15.0: #Spigolo di 2 centimetri?
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
                grid[int(x_sensore + cx)][int(y_sensore + cy)] = 1
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

def elabora_giroscopio():
    incl = sensore_giroscopio.leggi()
    if math.fabs(incl) > RAMP_TOLL:
        if not t.running:
            rampa_tile_t = (robot[0],robot[1])
        t.start()
        if t.read() > RAMP_SECONDS: #Ci siamo mossi su un'altra griglia
            t.stop()
            if grid is grid1:
                grid = grid2
                muri = muri2
                rampa_tile1 = rampa_tile_t
                rampa_tile2 = (robot[0], robot[1])
            else:
                grid = grid1
                muri = muri1
                rampa_tile1 = (robot[0], robot[1])
                rampa_tile2 = rampa_tile_t
    else:
        t.stop()

#moves = movimenti.Robo_moves()

'''
0 - casella nera
1 - vuoto
2 - non esplorato

grid1 e 2 vengono inizializzate come non esplorato
grid e' la griglia corrente
Una cella di grid è di 30 cm
'''
grid1 = [[int(2) for x in xrange(MAX_MAP+1)] for y in xrange(MAX_MAP+1)]
grid2 = [[int(2) for x in xrange(MAX_MAP+1)] for y in xrange(MAX_MAP+1)]
grid = grid1

'''
rampa_tile1 e' il tile in cui c'è la rampa nel grid1
rampa_tile2 e' il tile in cui c'è la rampa nel grid2
'''
rampa_tile1 = (None, None)
rampa_tile2 = (None, None)
rampa_tile_t = (None, None)

'''
[((1,1),(1,2)),((3,2),(2,2))]
    ^     ^
    |     |
    -------
'''
muri1 = []
muri2 = []
muri = muri1

theta = sensore_angolo.leggi()*math.pi/180;

distanza_precedente = sensore_distanza_p.leggi();

while True:
    for s in sensori_distanza:
        elabora_sensore(theta, s)
    distanza_corrente = sensore_distanza_p.leggi()
    elabora_giroscopio()
    elabora_velocita(theta, distanza_precedente, distanza_corrente, sensore_velocita)
    distanza_precedente = distanza_corrente
