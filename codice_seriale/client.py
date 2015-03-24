# Raspberry - Client Seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.openConnection()

closeCommand = "exit"

### Stampa a schermo le informazioni della connessione ###
print ("[Info] Serial connection open on port " +  com.port )
print ("[Info] Baudrate set to " + str(com.baud) )
print ("[Info] Character starter set to (" + com.charStarter + ")")
print ("[Info] Character terminator set to (" + com.charTerminator + ")")
print ("[Info] Enter " + closeCommand + " to close the program")

### Invia messaggio via seriale ###
if(com.isConnceted()):
	while True:
		buffer=""
		num = 0
		lenRead = 0
		buffer = raw_input("[Msg] --> ")
		if (buffer == closeCommand):
			break
		#com.Send(buffer)
		
		## Inizio istruzioni debug ##
		print(com.goForward())
		#print(com.goBack())
		#print(com.goBackGrad()
		#print(com.goRight())
		#print(com.goLeft())
		#print(com.goStop())
		#print(com.goGrad(3))
		#print(com.requestSensor(6))
		print ("[Debug] Buffer: " + com.sendBuffer) # Stampa il buffer di messaggi inviati
		## Fine istruzioni debug ##
		
	print ("\n[Info] Detected close command. The program will be terminated.")
	com.closeConnection() # Chiusura della connessione
	print ("[Info] Serial connection closed.")
else:
		print ("\n[Info] Unable to connect to serial.")
