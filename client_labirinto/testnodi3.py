#!/usr/bin/python
import nodi2

grafo = nodi2.Grafo()

grafo.inserisci('a', 'b', 5)
grafo.inserisci('a', 'd', 8)

grafo.inserisci('b', 'a', 5)
grafo.inserisci('b', 'c', 2)
grafo.inserisci('b', 'd', 10)

grafo.inserisci('c', 'b', 10)
grafo.inserisci('c', 'd', 1)

grafo.inserisci('d', 'a', 8)
grafo.inserisci('d', 'b', 2)
grafo.inserisci('d', 'c', 1)
grafo.inserisci('d', 'e', 6)
grafo.inserisci('d', 'f', 7)

grafo.inserisci('e', 'd', 6)

grafo.inserisci('f', 'd', 7)

print grafo.risolvi('a', 'f')
