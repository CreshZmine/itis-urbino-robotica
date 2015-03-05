#!/usr/bin/python

import nodi
import math

def distanza(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dx = dx**2
    dy = dy**2
    return math.sqrt(dx+dy)

grafo = nodi.Grafo()

a = nodi.Nodo()
b = nodi.Nodo()
c = nodi.Nodo()
d = nodi.Nodo()
e = nodi.Nodo()
f = nodi.Nodo()

a.aggiungi_vicino(b, 5)
a.aggiungi_vicino(d, 8)

b.aggiungi_vicino(a, 5)
b.aggiungi_vicino(c, 2)
b.aggiungi_vicino(d, 10)

c.aggiungi_vicino(b, 10)
c.aggiungi_vicino(d, 1)

d.aggiungi_vicino(a, 8)
d.aggiungi_vicino(b, 2)
d.aggiungi_vicino(c, 1)
d.aggiungi_vicino(e, 6)
d.aggiungi_vicino(f, 7)

e.aggiungi_vicino(d, 6)

f.aggiungi_vicino(d, 7)
#http://altenwald.org/2011/10/02/grafos-fundamentos-basicos/
