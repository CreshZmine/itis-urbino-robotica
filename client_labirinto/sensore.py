class Sensore():
    def __init__(self, id, mov):
        self.id = id
        self.mov = mov #RoboSerial
        self.lettura = 0

    def leggi(self):
        self.lettura = self.mov.requestSensor(self.id)
        return self.lettura
