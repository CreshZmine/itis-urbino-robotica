# Emulatore Python per comunicazione con microcontrollore Tiva | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial
import time

com=RoboSerial()
com.openConnection()

try:
	### Stampa a schermo le informazioni della connessione ###
	print ("########################")
	print ("# Avvio emulatore Tiva #")
	print ("########################\n")
	print ("[Info] Serial connection open on port " +  com.port )
	print ("[Info] Baudrate set to " + str(com.baud) )
	print ("[Info] Character starter set to (" + com.charStarter + ")")
	print ("[Info] Character terminator set to (" + com.charTerminator + ")")
	print ("[Info] Press CTRL+C to close the program")

	### Riceve i data dalla seriale ###
	if(com.isConnceted()):
		while True:
			if(com.receive()):
				print ("[Serial] Received (good): "+ com.lastReceive)
			else:
				print ("[Serial] Received (bad): "+ com.lastReceive)
			
			chr = com.lastReceive[0]
			
			if (chr == "F" or chr == "B" or chr == "I" or chr == "S" or chr == "R" or chr == "L" or chr == "G"):
				com.sendCommand16(chr,"0","1")
			else:
				com.sendCommand16("E","0","0")
			
			## Inizio istruzioni debug ##
			print ("[Debug] Buffer: " + com.receiveBuffer) # Stampa il buffer di messaggi ricevuti
			## Fine istruzioni debug ##
	else:
		print ("\n[Info] Unable to connect to serial.")
except (KeyboardInterrupt, SystemExit):
	print ("\n[Info] Keyboard interrupt detected. The program will be terminated.")
	com.closeConnection() #Close connection
	print ("[Info] Serial connection closed.")
