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
	print ("[Info] Connessione seriale aperta sulla porta " +  com.port )
	print ("[Info] Baudrate impostato a " + str(com.baud) )
	print ("[Info] Carattere terminatore impostato come (" + com.charTerminator + ")")
	print ("[Info] Premere CTRL+C per chiudere il programma")

	### Riceve i data dalla seriale ###
	if(com.isConnceted()):
		while True:
			com.receive()
			chr = com.lastReceive[0]
			
			if (chr == "F" or chr == "B" or chr == "I" or chr == "S" or chr == "R" or chr == "L" or chr == "G"):	# Richiesta comando generico
				com.sendCommand16(chr,"0","1")
				print ("[Comando] Ricevuto comando "+chr)
			elif (chr == "D"):	# Richiesta informazioni dal sensore
				com.sendCommand16(com.lastReceive[1],"4","6")
				print ("[Richiesta] Ricevuta richiesta del sensore "+com.lastReceive[1])
			else:	# Qualsiasi altra richiesta
				com.sendCommand16("E","0","0")
			
			## Inizio istruzioni debug ##
			#print ("[Debug] Buffer: " + com.receiveBuffer) # Stampa il buffer di messaggi ricevuti
			## Fine istruzioni debug ##
	else:
		print ("\n[Info] Impossibile collegarsi alla porta seriale.")
except (KeyboardInterrupt, SystemExit):
	print ("\n[Info] Rilevata interruzione da tastiera. Il programma verra' terminato.")
	com.closeConnection() #Close connection
	print ("[Info] Connessione seriale chiusa.")
