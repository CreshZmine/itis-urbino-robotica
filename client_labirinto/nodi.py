import math

INFINITE=999

class Nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.peso = INFINITE
        self.precedente = None

    def calcola_distanza(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        dx *= dx
        dy *= dy
        return math.sqrt(dx+dy)

class Grafo:
    def __init__(self):
        self.nodi = []

    def calcola_strada_corta(self, inizio, fine):
        self.reset_nodi()
        scanning = []
        scanned = [inizio]
        for vicino in inizio.vicini:
            vicino.precedente = inizio
            vicino.peso = inizio.calcola_distanza(vicino)
            scanning.append(vicino)

        while scanning:
            min = scanning[0]
            for i in range(len(scanning)):
                if scanning[i].peso < min.peso:
                    min = scanning[i]

            #calcolo i pesi dei vicini di min
            for vicino in min.vicini:
                if not vicino in scanned:
                    peso_compl = min.calcola_distanza(vicino)+min.peso
                    if peso_compl < vicino.peso:
                        vicino.peso = peso_compl
                        vicino.precedente = min
                    if not vicino in scanning:
                        scanning.append(vicino)

            #rimuovo min da scanning
            scanning.remove(min)
            scanned.append(min)

        strada = []
        if not fine.precedente is None:
            strada.append(fine)
            curr = fine
            while not curr is inizio:
                strada.insert(0, curr.precedente)
                curr = curr.precedente

        return strada

    def reset_nodi(self):
        #Resetto gli i pesi e i puntatori ai nodi precedenti
        for n in self.nodi:
            n.peso = INFINITE
            n.precedente = None

