import socket

HOST = '127.0.0.1'
PORT = 5436

res = 0.0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('s\x00')
print "sensore 0"
res = s.recv(4096)
print res

s.sendall('s\x01')
print "sensore 1"
res = s.recv(4096)
print res

s.sendall('s\x02')
print "sensore 2"
res = s.recv(4096)
print res

s.sendall('s\x03')
print "sensore 3"
res = s.recv(4096)
print res

s.close()
