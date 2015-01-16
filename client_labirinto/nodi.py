import math

class nodo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calcola_distanza(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        dx *= dx
        dy *= dy
        return math.sqrt(dx+dy)

def calcola_strada_corta(inizio, fine):
    scanning = []
    scanned = [inizio]
    for vicino in inizio.vicini:
        vicino.precendente = inizio
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
                if not(hasattr(vicino, "peso")) or peso_compl < vicino.peso:
                    vicino.peso = peso_compl
                    vicino.precendente = min
                if not vicino in scanning:
                    scanning.append(vicino)

        #rimuovo min da scanning
        scanning.remove(min)
        scanned.append(min)

    strada = []
    if hasattr(fine, "precendente"):
        strada.append(fine)
        curr = fine
        while not curr is inizio:
            strada.insert(0, curr.precendente)
            curr = curr.precendente

    return strada
