import sys
import getopt
import math

def tp(x,y):
    return math.sqrt(x*x+y*y)

def parseMapFile(map_path):
    map = []
    with open(map_path, "r") as map_file:
        for line in map_file:
            line = line.split()
            if len(line) == 0:
                continue
            if line[0][0] == '#':
                continue
            if line[0] == 'l': #Disegna una linea
                dx =float(line[3])-float(line[1])
                dy =float(line[4])-float(line[2])
                d = tp(dx,dy)
                i = 5.0
                map.append((float(line[1]),float(line[2])))
                while i < d:
                    map.append((float(line[1])+dx*i/d,float(line[2])+dy*i/d))
                    i=i+10
                map.append((float(line[3]),float(line[4])))
            if line[0] == 'r': #Posizione del robot
            else:
                map.append((float(line[0]), float(line[1])))
