# Raspberry - Server seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.OpenConnection()

try:
	### Stampa a schermo le informazioni della connessione ###
	print ("[Info] Serial connection open on port " +  com.port )
	print ("[Info] Baudrate set to " + str(com.baud) )
	print ("[Info] Character starter set to (" + com.charStarter + ")")
	print ("[Info] Character terminator set to (" + com.charTerminator + ")")
	print ("[Info] Press CTRL+C to close the program")

	### Riceve i data dalla seriale ###
	if(com.IsConnceted()):
		while True:
			if(com.Recive()):
				print ("[Serial] Recived (good): "+ com.lastRecive)
			else:
				print ("[Serial] Recived (bad): "+ com.lastRecive)
			
			## Inizio istruzioni debug ##
			print ("[Debug] Buffer: " + com.reciveBuffer) # Stampa il buffer di messaggi ricevuti
			## Fine istruzioni debug ##
	else:
		print ("\n[Info] Unable to connect to serial.")
except (KeyboardInterrupt, SystemExit):
	print ("\n[Info] Keyboard interrupt detected. The program will be terminated.")
	com.CloseConnection() #Close connection
	print ("[Info] Serial connection closed.")
