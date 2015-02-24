from classSerial import RoboSerial

Prova = RoboSerial()
ser = Prova.OpenConnection()
#msg = Prova.Recive(ser)
#print msg
Prova.Send(ser, "Hello")
Prova.CloseConnection(ser)