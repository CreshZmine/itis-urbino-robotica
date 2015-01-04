#SERVER TCP IP
from socket import *
import thread
import time
import math

import pyglet
from pyglet.gl import *

#lista=[(10,10),(100,100),(20,80),(10,30),(300,100),(20,180)] 
lista=[]
listaraggi = [] 

a=10
b=400
s=12
 
def tp(x,y):
    return math.sqrt(x*x+y*y)
    
def linea(x0,y0,x1,y1):
    dx =x1-x0
    dy =y1-y0
    d = tp(dx,dy)
    i = 5.0
    lista.append((x0,y0))
    while i < d:
        lista.append((x0+dx*i/d,y0+dy*i/d))
        i=i+10
    lista.append((x1,y1))
        
def dist((x0,y0),(x1,y1)):
    dx =x1-x0
    dy =y1-y0
    return tp(dx,dy)

def sensore(tx, ty, dx, dy):
    print "sensore"
    startx=tx
    starty=ty
    mindist = 200
    minpoint = (0,0)
    while abs(tx-startx)<100 and abs(ty-starty)<100 :
        for p in lista :
            if distanza(p,(tx,ty))<20 :
                if mindist > distanza(p,(robo.x,robo.y)) :
                    mindist = distanza(p,(robo.x,robo.y))
                    minpoint = p
        tx += dx
        ty += dy
    listaraggi = [ minpoint ]
    return str(mindist)


linea(a ,a ,a ,b)
linea(a ,b ,b ,b)
linea(b ,a ,b ,b)
linea(b ,a , 120 ,a)
linea(a ,a , 80 ,a)

linea(5*a,7*a,b/2,b/3)
linea(b/2,7*a,b/2,b/3)
linea(5*a,b/2,3*b/4,b/2)
linea(b/4,3*b/4,3*b/4,3*b/4)


    
def f(x):
    r = 1
    while x >0:
        r = r * x
        x= x-1
    return r
 
class obj:
    cli=''
    addr=''
    x = 100.0
    y = 0.0
    dx = 0.0
    dy = 1.0
    
    connessione = 0
    def avanti(self,dl):
        print "avanti: " ,self.x,self.y
        self.x = self.x+self.dx*dl
        self.y = self.y+self.dy*dl
        print "avanti: " ,self.x,self.y
        
    def ruota(self,da):
        self.dx,self.dy = self.dx*math.cos(da)-self.dy*math.sin(da),self.dx*math.sin(da)+self.dy*math.cos(da)
         
    def sensore(self,n):
        return 0

    def disegna(self):
        d = 6.0
        glBegin(GL_LINE_STRIP)
        glVertex2f(self.x-self.dy*d, self.y-self.dx*d)  
        glVertex2f(self.x+self.dy*d, self.y+self.dx*d)  
        glVertex2f(self.x+self.dx*2*d, self.y+self.dy*2*d)  
        glVertex2f(self.x-self.dy*d, self.y-self.dx*d)  
        glEnd()
        if self.connessione <= 1:
            if self.connessione == 1: 
                connetti()
            self.connessione += 1
            #handler(self.cli,self.addr)
    
robo = obj()
     
BUFF = 1024

#INDIRIZZO E PORTA DEL SERVER
#HOST = '192.168.1.7'# must be input parameter @TODO
HOST = '127.0.0.1'# must be input parameter @TODO
PORT = 5436 # must be input parameter @TODO

localtime = time.asctime( time.localtime(time.time()) )

print "Server on. Local Time "+localtime

def gen_response():
    return 'ok-bene\n' 
 
def handler2(clientsock,addr):
    while 1:
        
        data = clientsock.recv(BUFF)
        print 'data:' + repr(data)
        if not data : 
            break
        #   if data == '': break
        a = f(1000) #solo per rallentare
        risposta="che?"
        if data[0] == 'a' : 
            print "avanti"
            robo.avanti(4)
            risposta = "ok"
        else:
            if data[0] == 'r' :
                robo.ruota(-1.57)
                risposta = "ok"
            else:
                if data[0] == 'l' :
                    robo.ruota(1.57)
                    risposta = "ok"
                else:
                    if data[0] == 's':
                        if data[1] == 0:
                            #sensore 0 : distanza avanti
                            risposta = sensore(robo.x, robo.y, robo.dx, robo.dy)
                        if data[1] == 1:
                            #sensore 1 : distanza sinistra
                            risposta = sensore(robo.x, robo.y, -robo.dy, robo.dx)
                        if data[1] == 2:
                            #sensore 1 : distanza destra
                            risposta = sensore(robo.x, robo.y, robo.dy, -robo.dx)
                        if data[1] == 3:
                            #sensore 3 : distanza dietro
                            risposta = sensore(robo.x, robo.y, -robo.dx, -robo.dy)

        clientsock.send(risposta)
        time.sleep(0.6)
        print 'sent:' + repr(gen_response())
    clientsock.close()
    print "=== chiuso ===" 


def handler(clientsock,addr):
    
    data = clientsock.recv(BUFF)
    print 'data:' + repr(data)
    if not data : 
        return
    #   if data == '': break
    a = f(1000) #solo per rallentare
    if data[0] == 'a' : 
        print "avanti"
        robo.avanti(4)
    else:
        if data[0] == 'r' :
            robo.ruota(-1.57)
        else:
            if data[0] == 'l' :
                robo.ruota(0.7)
                 
    clientsock.send(gen_response())
    print 'sent:' + repr(gen_response())


def connetti():    
    if __name__=='__main__':
        ADDR = (HOST, PORT) #QUESTO SERVER
        serversock = socket(AF_INET, SOCK_STREAM)
        serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serversock.bind(ADDR)
        serversock.listen(2)
        #while 1:
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler2, (clientsock, addr))
        robo.cli = clientsock
        robo.addr= addr

def quadro():
    d = 4.0
    for (x,y) in lista:
        glBegin(GL_LINE_STRIP)
        glVertex2f(x-d, y-d)  
        glVertex2f(x-d, y+d)
        glVertex2f(x+d, y+d)
        glVertex2f(x+d, y-d)
        glVertex2f(x-d, y-d)
        glEnd()


def disegna():
    quadro()
    robo.disegna()
    
    for (tx,ty) in listaraggi:
        glBegin(GL_LINE_STRIP)
        glVertex2f(robo.x,robo.y)  
        glVertex2f(tx, ty)
        glEnd()


win = pyglet.window.Window()

@win.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    disegna()
            
pyglet.app.run()
