class Sensore():
    def __init__(self, id, mov):
        self.id = id
        self.mov = mov #RoboSerial

    def leggi(self):
        return self.mov.requestSensor(self.id)
