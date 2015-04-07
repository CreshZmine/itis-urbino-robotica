class Sensore():
    def __init__(self, id, mov):
        self.id = id
        self.mov = mov #RoboSerial
        self.lettura = 0
        self.valido = False

    def leggi(self):
        self.lettura, self.valido = self.mov.requestSensor(self.id)
        return self.lettura, self.valido
