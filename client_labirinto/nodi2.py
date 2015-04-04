import heapq

class Grafo:
    def __init__(self):
        self.graph = {}

    def inserisci(self, nodo, vicino, costo):
        if not nodo in self.graph:
            self.graph[nodo] = {}
        self.graph[nodo][vicino] = costo

    def risolvi(self, inizio, fine):
        #costo, nodo corrente, percorso
        coda = [(0, inizio, [])]

        visitati = set()

        while True:
            (costo, v, percorso) = heapq.heappop(coda)
            if not v in visitati:
                percorso = percorso + [v]
                visitati.add(v)
                if v == fine:
                    return percorso, costo
                for (prossimo, c) in self.graph[v].iteritems():
                    heapq.heappush(coda, (costo+c, prossimo, percorso))
