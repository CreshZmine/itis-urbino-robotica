HOST = '127.0.0.1'
PORT = 5436

s=None

def initialize():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

def turn_right():
    s.sendall('r')

def turn_left():
    s.sendall('l')

def forward():
    s.sendall('a')

def sensore(numero_sensore):
    s.sendall('s'+chr(numero_sensore))
