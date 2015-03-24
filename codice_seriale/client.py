# Raspberry - Client Seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.openConnection()

closeCommand = "exit"

### Stampa a schermo le informazioni della connessione ###
print ("#######################################")
print ("# Avvio test di comunicazione seriale #")
print ("#######################################\n")
print ("[Info] Connessione seriale aperta sulla porta " +  com.port )
print ("[Info] Baudrate impostato a " + str(com.baud) )
print ("[Info] Carattere terminatore impostato come (" + com.charTerminator + ")")
print ("[Info] Premere CTRL+C per chiudere il programma")

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
		print(com.goBack())
		print(com.goBackGrad())
		print(com.goRight())
		print(com.goLeft())
		print(com.goStop())
		print(com.goGrad(3))
		print(com.requestSensor(6))
		#print ("[Debug] Buffer: " + com.sendBuffer) # Stampa il buffer di messaggi inviati
		#print ("[Debug] Buffer: " + com.receiveBuffer) # Stampa il buffer di messaggi ricevuti
		## Fine istruzioni debug ##
		
	print ("\n[Info] Rilevata interruzione da tastiera. Il programma verra' terminato.")
	com.closeConnection() #Close connection
	print ("[Info] Connessione seriale chiusa.")
else:
	print ("\n[Info] Impossibile collegarsi alla porta seriale.")