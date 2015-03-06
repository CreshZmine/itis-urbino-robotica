# coding=utf-8
# Raspberry - Server Seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.OpenConnection()

closeCommand = "exit"

### Printing connection information ###
print ("[Info] Serial connection open on port " + str(com.GetPort()))
print ("[Info] Baudrate set to " + str(com.GetBaudrate()))
print ("[Info] Character starter set to (" + com.GetCharStarter() + ")")
print ("[Info] Character terminator set to (" + com.GetCharTerminator() + ")")
print ("[Info] Enter " + closeCommand + " to close the program")

### Send command to serial ###
while True:
	buffer=""
	num = 0
	lenRead = 0
	buffer = raw_input("[Msg] --> ")
	if (buffer == closeCommand):
		break
	com.Send(buffer)
	com.SendCommand("F","0")
	if(com.IsConnceted()):
		print("Connected")
print ("\n[Info] Detected close command. The program will be terminated.")
com.CloseConnection() #Close connection
print ("[Info] Serial connection closed.")