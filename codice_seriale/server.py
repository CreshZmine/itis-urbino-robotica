# Raspberry - Server Seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.OpenConnection()

closeCommand = "exit"

### Stampa a schermo le informazioni della connessione ###
print ("[Info] Serial connection open on port " + str(com.GetPort()))
print ("[Info] Baudrate set to " + str(com.GetBaudrate()))
print ("[Info] Character starter set to (" + com.GetCharStarter() + ")")
print ("[Info] Character terminator set to (" + com.GetCharTerminator() + ")")
print ("[Info] Enter " + closeCommand + " to close the program")

### Invia messaggio via seriale ###
if(com.IsConnceted()):
	while True:
		buffer=""
		num = 0
		lenRead = 0
		buffer = raw_input("[Msg] --> ")
		if (buffer == closeCommand):
			break
		com.Send(buffer)
		
		## Inizio istruzioni debug ##
		#com.GoForward()
		#com.GoBack()
		#com.GoRight()
		#com.GoLeft()
		#com.RequestSensor(6)
		print ("[Debug] Buffer: " + com.GetSendBuffer()) # Stampa il buffer di messaggi inviati
		## Fine istruzioni debug ##
		
	print ("\n[Info] Detected close command. The program will be terminated.")
	com.CloseConnection() # Chiusura della connessione
	print ("[Info] Serial connection closed.")
else:
		print ("\n[Info] Unable to connect to serial.")