import socket

HOST = '127.0.0.1'
PORT = 5436

class Robo_moves():

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def turn_right(self):
        self.s.sendall('r')

    def turn_left(self):
        self.s.sendall('l')

    def forward(self):
        self.s.sendall('a')

    def sense(self, numero_sensore):
        self.s.sendall('s'+chr(numero_sensore))
        return self.s.recv(4096)
