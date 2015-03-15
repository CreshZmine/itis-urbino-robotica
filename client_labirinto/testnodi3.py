#!/usr/bin/python
import nodi2

grafo = nodi2.Grafo()

grafo.graph['a'] = {}
grafo.graph['a']['b'] = 5
grafo.graph['a']['d'] = 8

grafo.graph['b'] = {}
grafo.graph['b']['a'] = 5
grafo.graph['b']['c'] = 2
grafo.graph['b']['d'] = 10

grafo.graph['c'] = {}
grafo.graph['c']['b'] = 10
grafo.graph['c']['d'] = 1

grafo.graph['d'] = {}
grafo.graph['d']['a'] = 8
grafo.graph['d']['b'] = 2
grafo.graph['d']['c'] = 1
grafo.graph['d']['e'] = 6
grafo.graph['d']['f'] = 7

grafo.graph['e'] = {'d': 6}

grafo.graph['f'] = {'d': 7}

print grafo.risolvi('a', 'f')
