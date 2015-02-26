from RoboSerial import RoboSerial

Prova = RoboSerial()
Prova.OpenConnection()
#msg = Prova.Recive()
#print msg
Prova.Send("Hello")
Prova.CloseConnection()
