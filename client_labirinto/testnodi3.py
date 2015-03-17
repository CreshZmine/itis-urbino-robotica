#!/usr/bin/python
import nodi2

grafo = nodi2.Grafo()

grafo.inserisci_nodo('a', 'b', 5)
grafo.inserisci_nodo('a', 'd', 8)

grafo.inserisci_nodo('b', 'a', 5)
grafo.inserisci_nodo('b', 'c', 2)
grafo.inserisci_nodo('b', 'd', 10)

grafo.inserisci_nodo('c', 'b', 10)
grafo.inserisci_nodo('c', 'd', 1)

grafo.inserisci_nodo('d', 'a', 8)
grafo.inserisci_nodo('d', 'b', 2)
grafo.inserisci_nodo('d', 'c', 1)
grafo.inserisci_nodo('d', 'e', 6)
grafo.inserisci_nodo('d', 'f', 7)

grafo.inserisci_nodo('e', 'd', 6)

grafo.inserisci_nodo('f', 'd', 7)

print grafo.risolvi('a', 'f')
