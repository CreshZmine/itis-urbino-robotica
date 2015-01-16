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
