import socket

HOST = '127.0.0.1'
PORT = 5436

class Robo_moves():

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

    def turn_right(self):
        self.s.sendall('r')
        self.s.recv(4096)

    def turn_left(self):
        self.s.sendall('l')
        self.s.recv(4096)

    def forward(self):
        self.s.sendall('a')
        self.s.recv(4096)

    def sense(self, numero_sensore):
        self.s.sendall('s'+chr(numero_sensore))
        return self.s.recv(4096)

    def turn(self, theta):
        self.s.sendall('t'+str(theta))
        self.s.recv(4096)

    def termina(self):
        self.s.close()
