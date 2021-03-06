#!/usr/bin/python
import RoboSerial
import cluster
import grafo_cartesiano
import math
import random
import sensore
import sys
import thread
import time
import timer
import cluster_muri

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
robot_lock = thread.allocate_lock()
robot = [MAX_MAP/2, MAX_MAP/2]

mov = RoboSerial.RoboSerial()
mov.openConnection()
t = timer.Timer()

sensori_lock = thread.allocate_lock()
sensori_distanza = []
sensori_distanza.append(sensore.Sensore(1, mov))    #Sensore davanti
sensori_distanza[-1].dx = 0
sensori_distanza[-1].dy = 5/30.0
sensori_distanza[-1].offset = 0
sensori_distanza.append(sensore.Sensore(5, mov))    #Sensore destra-alto
sensori_distanza[-1].dx = 7.5/30.0
sensori_distanza[-1].dy = 5/30.0
sensori_distanza[-1].offset = -math.pi/2
sensori_distanza.append(sensore.Sensore(4, mov))    #Sensore destra-basso
sensori_distanza[-1].dx = 7.5/30.0
sensori_distanza[-1].dy = -5/30.0
sensori_distanza[-1].offset = -math.pi/2
sensori_distanza.append(sensore.Sensore(2, mov))    #Sensore sinistra-alto
sensori_distanza[-1].dx = -7.5/30.0
sensori_distanza[-1].dy = 5/30.0
sensori_distanza[-1].offset = math.pi/2
sensori_distanza.append(sensore.Sensore(3, mov))    #Sensore sinistra-basso
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
    sensori_lock.acquire()
    dist, val = sensore.leggi()
    sensori_lock.release()
    if val:
        dist /= 30.0 #Lo porto nella unita di misura "casella"
        robot_lock.acquire()
        x_sensore = robot[0]+sensore.dx*math.cos(theta)-sensore.dy*math.sin(theta)
        y_sensore = robot[1]+sensore.dx*math.sin(theta)+sensore.dy*math.cos(theta)
        robot_lock.release()
        x_coor = x_sensore+dist*math.cos(theta+sensore.offset)
        y_coor = y_sensore+dist*math.sin(theta+sensore.offset)

        x_coor_approx = int(math.ceil(x_coor)) if (x_coor % 1) > 0.5 else int(math.floor(x_coor))
        y_coor_approx = int(math.ceil(y_coor)) if (y_coor % 1) > 0.5 else int(math.floor(y_coor))
        prima_casella = (math.trunc(x_coor), math.trunc(y_coor))
        if math.sqrt((x_coor_approx-x_coor)**2+(y_coor_approx-y_coor)**2) > 1/15.0: #Spigolo di 2 centimetri?
            if math.fabs(y_coor_approx - y_coor) < math.fabs(x_coor_approx - x_coor):
                seconda_casella = (prima_casella[0], prima_casella[1] + (1 if (y_coor % 1) > 0.5 else -1))
            else:
                seconda_casella = (prima_casella[0] + (1 if (x_coor % 1) > 0.5 else -1), prima_casella[1])
            muri_lock.acquire()
            if not (prima_casella, seconda_casella) in muri and not (seconda_casella, prima_casella) in muri:
                muri.append((prima_casella, seconda_casella))
                if sensore.id == 5 or sensore.id == 4: #Se il muro e' alla mia destra
                    if muri is muri1:
                        muri1_passato.append(True)
                    else:
                        muri2_passato.append(True)
                else:
                    if muri is muri1:
                        muri1_passato.append(False)
                    else:
                        muri2_passato.append(False)
            muri_lock.release()
            #imposto le caselle tra la mia posizione e il rilevamento a 0 (vuoto)
            dx, dy = math.cos(theta+sensore.offset), math.sin(theta+sensore.offset)
            cx, cy = dx, dy
            for i in range(int(math.floor(dist))):
                grid_lock.acquire()
                try:
                    grid[int(x_sensore + cx)][int(y_sensore + cy)] = 1
                except IndexError:
                    pass
                grid_lock.release()
                cx, cy = cx+dx, cy+dy

def elabora_sensore_colore():
    sensori_lock.acquire()
    col, val = sensore_luminosita.leggi()
    if col == 255 and col == True:
        grid_lock.acquire()
        grid[int(robot[0])][int(robot[1])] = 0
        grid_lock.release()
    sensori_lock.release()

def elabora_posizione():
    grid_lock.acquire()
    grid[int(robot[0])][int(robot[1])] = 1
    grid_lock.release()

def elabora_velocita(theta, distanza_precedente, distanza_corrente, sensore_velocita):
    '''
    Aggiorna la posizione del robot tenendo conto della velocita
    '''
    delta_distanza = distanza_corrente - distanza_precedente
    delta_distanza /= 30.0
    robot_lock.acquire()
    robot[0] += delta_distanza*math.cos(theta)
    robot[1] += delta_distanza*math.sin(theta)
    robot_lock.release()

def elabora_giroscopio():
    sensori_lock.acquire()
    incl, val = sensore_giroscopio.leggi()
    sensori_lock.release()
    if val:
        if math.fabs(incl) > RAMP_TOLL:
            if not t.running:
                robot_lock.acquire()
                rampa_lock.acquire()
                rampa_tile_t = (robot[0],robot[1])
                rampa_lock.release()
                robot_lock.release()
            t.start()
            if t.read() > RAMP_SECONDS: #Ci siamo mossi su un'altra griglia
                t.stop()
                grid_lock.acquire()
                muri_lock.acquire()
                if grid is grid1:
                    grid = grid2
                    muri = muri2
                    rampa_lock.acquire()
                    rampa_tile1 = rampa_tile_t
                    robot_lock.acquire()
                    rampa_tile2 = (robot[0], robot[1])
                    rampa_lock.release()
                    robot_lock.release()
                else:
                    grid = grid1
                    muri = muri1
                    robot_lock.acquire()
                    rampa_lock.acquire()
                    rampa_tile1 = (robot[0], robot[1])
                    robot_lock.release()
                    rampa_tile2 = rampa_tile_t
                    rampa_lock.release()
                muri_lock.release()
                grid_lock.release()
        else:
            t.stop()

def torna_inizio():
    g = grafo_cartesiano.GrafoCartesiano()
    robot_lock.acquire()
    grid_lock.acquire()
    muri_lock.acquire()
    route = g.risolvi(muri, (robot[0], robot[1]), (200,200), MAX_MAP, MAX_MAP, grid)
    if grid is grid2:   #Siamo nel piano sbagliato
        rampa_lock.acquire()
        route = route + g.risolvi(muri, (robot[0], robot[1]), rampa_tile2, MAX_MAP, MAX_MAP, grid)
        rampa_lock.release()
    muri_lock.release()
    grid_lock.release()
    robot_lock.release()
    followRoute(route)

def pianifica(centers1, centers2):
    #start - cluster1 - rampa_tile1 - rampa_tile2 - cluster2 - inizio
    g = grafo_cartesiano.GrafoCartesiano()
    piano = centers1
    piano += rampa_tile1
    piano += rampa_tile2
    piano += clusters2
    piano += [(200,200)]
    route = []
    for obb in piano:
        muri_lock.acquire()
        route += g.risolvi(muri, (200, 200), obb, MAX_MAP, MAX_MAP, grid)
        muri_lock.release()
    followRoute(route)


def followRoute(route):
    for nodo in route:
        vai_a_nodo(nodo)

def vai_a_nodo(nodo):
    robot_lock.acquire()
    dx = nodo[0] - robot[0]
    dy = nodo[1] - robot[1]
    if theta > -0.1 and theta < 0.1:
        while math.fabs(nodo[0] - robot[0]) < 0.5:
            if dx > 0:
                mov.goForward()
            else:
                mov.goBack()
        if dy > 0:
            mov.goLeft()
        else:
            mov.goRight()
    if theta > maht.pi-0.1 and theta < math.pi+0.1:
        while math.fabs(nodo[0] - robot[0]) < 0.5:
            if dx > 0:
                mov.goBack()
            else:
                mov.goForward()
        if dy > 0:
            mov.goRight()
        else:
            mov.goLeft()

    while math.sqrt((nodo[0]-robot[0])**2+(nodo[1]-robot[1])**2) > 1:
        robot_lock.release()
        mov.goForward()
        robot_lock.acquire()
    robot_lock.release()

def find_next_token():
    murin_passato = muri1_passato if muri is muri1 else muri2_passato
    return cluster_muri.trova_muro_vicino((robot[0], robot[1]), muri, murin_passato)

def routine_movimento():
    muovi = True
    sensori_lock.acquire()
    dist_a, val = sensori_distanza[0].lettura
    dist_d, val_d = sensori_distanza[1].lettura
    if val_d:
        if dist_d > 1: #Manca il muro a destra
            mov.goRight()
            muovi = False
        elif val:
            if dist_a < 3/30.0: #Se c'e' un muro piu' vicino di 3 cm
                mov.goLeft()
                muovi = False
    if muovi:
        mov.goForward()
    sensori_lock.release()

def move_to(target):
    g = grafo_cartesiano.GrafoCartesiano()
    followRoute(g.risolvi(muri, (robot[0], robot[1]), target, MAX_MAP, MAX_MAP, grid))

def loop_routine_movimento(nothing, nothing1):
	start = (200, 200)
	mov.goForward()
	for i in range(2):
		while True:
			robot_lock.acquire()
			grid_lock.acquire()
			while not ((math.floor(robot[0]) == start[0] and math.floor(robot[1]) == start[1]) or (math.ceil(robot[0]) == start[0] and math.ceil(robot[1]) == start[1]) and grid is grid1):
				grid_lock.release()
				robot_lock.release()
				routine_movimento()
				if rileva_vittima():
					sgancia()
				robot_lock.acquire()
				grid_lock.acquire()
			robot_lock.release()
			grid_lock.release()
			start = find_next_token()
			if start == None:
				break
			move_to(start)
		#Vai al secondo piano
		move_to(rampa_tile1)
		move_to(rampa_tile2)
		#Rifai la stessa cosa del primo nel secondo
		start = find_next_token()
	#Torna all'inizio
	move_to(rampa_tile2)
	move_to(rampa_tile1)
	move_to((200,200))

def rileva_vittima():
    temp, val = sensore_temperatura.leggi()
    dist, val1 = sensori[0].lettura, sensori[0].valido
    dist2, val2 = sensori[1].lettura, sensori[1].valido
    dist3, val3 = sensori[3].lettura, sensori[3].valido
    if val and val1 and val2 and val3 and temp >= 28 and (dist < 15.0 or dist2 < 15.0 or dist3 < 15.0):
        return True
    return False

def sgancia():
    sensori_lock.acquire()
    mov.goBackGrad()
    sensori_lock.release()
    mov.leaveRescuePack()
    mov.goBackGrad()

#moves = movimenti.Robo_moves()

'''
0 - casella nera
1 - vuoto
2 - non esplorato

grid1 e 2 vengono inizializzate come non esplorato
grid e' la griglia corrente
Una cella di grid e' di 30 cm
'''
grid_lock = thread.allocate_lock()
grid1 = [[int(2) for x in xrange(MAX_MAP+1)] for y in xrange(MAX_MAP+1)]
grid2 = [[int(2) for x in xrange(MAX_MAP+1)] for y in xrange(MAX_MAP+1)]
grid = grid1

'''
rampa_tile1 e' il tile in cui c'e' la rampa nel grid1
rampa_tile2 e' il tile in cui c'e' la rampa nel grid2
'''
rampa_lock = thread.allocate_lock()
rampa_tile1 = (None, None)
rampa_tile2 = (None, None)
rampa_tile_t = (None, None)
routine = True

'''
[((1,1),(1,2)),((3,2),(2,2))]
    ^     ^
    |     |
    -------

murin_passato indica se si e' gia' passati a sinistra di un determinato muro
'''
muri_lock = thread.allocate_lock()
muri1 = []
muri2 = []
muri1_passato = []
muri2_passato = []
muri = muri1

theta_lock = thread.allocate_lock()
ret,chk = sensore_angolo.leggi()
theta = ret*math.pi/180;

distanza_precedente = sensore_distanza_p.leggi();
loop_movimento_t = thread.start_new_thread(loop_routine_movimento, (None, None))

while True:
    for s in sensori_distanza:
        elabora_sensore(theta, s)
    sensori_lock.acquire()
    elabora_sensore_colore()
    elabora_posizione()
    theta = sensore_angolo.leggi()*math.pi/180
    theta %= 2*math.pi
    distanza_corrente = sensore_distanza_p.leggi()
    sensori_lock.release()
    elabora_giroscopio()
    elabora_velocita(theta, distanza_precedente, distanza_corrente, sensore_velocita)
    distanza_precedente = distanza_corrente
    robot_lock.acquire()
    grid_lock.acquire()
    robot_lock.release()
    grid_lock.release()
