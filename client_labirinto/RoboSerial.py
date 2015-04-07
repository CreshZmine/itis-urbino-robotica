# Raspberry - RoboSerial | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Scritto per Python 2.7
# Per installare PySerial -> python -m pip install pyserial

import serial

class RoboSerial:
	def __init__(self):
		# Impostazioni di connessione
		self.port = "" # Porta seriale in uso
		self.defPort = "/dev/ttyAMA0" # Porta seriale principale
		self.altPort = "COM2" # Porta seriale alternativa (attualmente usate per la simulazione su Windows)
		self.baud = 115200 # Baudrate per la comunicazione seriale

		# Impostazioni di comunicazione
		self.charStarter="#" # Carattere che determina l'inizio della comunicazione
		self.charTerminator="*" # Carattere che determina la fine della comunicazione

		# Variabili aggiuntive
		self.ser = None # Oggetto per comunicazione seriale

		# Ultimi messaggi inviati/ricevuti
		self.lastReceive = ""
		self.lastSend = ""

		# Buffer di comunicazione
		self.receiveBuffer = ""
		self.sendBuffer = ""

	def __del__(self):
		# Chiusura connessione seriale
		if(self.ser != None):
			self.ser.close()

	#######################################
	# Funzioni per la connessione seriale #
	#######################################

	def openConnection(self):
		# NOTA -> Se non e' stato possibile aprire la comunicazione seriale ser verra' settato a null
		# !ATTENZIONE! -> Il Raspberry PI quando la porta seriale UART0 viene inizializzata invia un impulso negativo di 32us sul TX
		try:
			self.ser = serial.Serial(self.defPort, self.baud)  # Tentativo di connessione con la porta principale
			self.port=self.defPort
			return True
		except:
			# In caso di errore con la porta principale
			try:
				self.ser = serial.Serial(self.altPort, self.baud)  # Tentativo di connessione con la porta alternativa
				self.port=self.altPort
				return True
			except:
				# In caso di errore con la porta alternativa
				self.ser=None # Imposta "ser" a null per mancata connessione
				return False

	def openConnectionPort(self, portCon):
		# NOTA -> Se non e' stato possibile aprire la comunicazione seriale ser verra' settato a null
		# !ATTENZIONE! -> Su Raspberry PI quando la porta seriale UART0 viene inizializzata viene inviato un impulso negativo di 32us sul TX
		try:
			self.ser = serial.Serial(portCon, self.baud)  # Tentativo di connessione
			self.port=portCon
		except:
			# In caso di errore
			self.ser=None # Imposta "ser" a null per mancata connessione

	def closeConnection(self):
		if(self.ser != None):
			self.ser.close() 	# Chiude la connessione
			self.port="" 		# Modifica la stringa per la porta in uso

	def isConnected(self):
		# Verifica se la comunicazione e' aperta
		# Valori di ritorno:
		# 	-> True se e' apera
		# 	-> False se e' chiusa

		if(self.ser != None):
			return True
		else:
			return False

	#######################################
	# Funzioni per l'invio e la ricezione #
	#######################################

	def receive(self):
		if(self.isConnected()):
			read=""
			num = 0
			lenRead = 0
			while True:
				num = self.ser.inWaiting() # Verifica quanti dati stanno per esserre ricevuti
				lenRead = len(read)-1
				if (lenRead > 0 and read[lenRead] == self.charTerminator): # Rileva il carattere di fine comunicazione
					break
				elif (num!=0):
					read+=self.ser.read(num) # Legge dalla seriale

			# Manipolazione e verifica del messaggio ricevuto
			self.receiveBuffer+=read														# Salva il messaggio ricevuto nel buffer
			read=read.replace(self.charTerminator," ") 										# Rimuove il carattere terminatore della comunicazione
			self.lastReceive = read 														# La salvo come ultima stringa ricevuta
			cksum = self.genChecksum16(read[-5], read[-4], read[-3])						# Genero il checksum per la verifica dell'integrita' del messaggio

			# Verifico se il checksum generato corrisponde con quello ricevuto
			if (cksum == ord(read[-2])):
				return True
			else:
				return False
		else:
		  	# Da sempre esito negativo alla verifica del checksum quando la connessione seriale non e' disposibile
			return False

	def send(self, msg):
		if(self.isConnected()):
			msg+=self.charTerminator
			self.sendBuffer+=msg
			self.lastSend = msg
			self.ser.write(msg)

	def sendCommand(self, cmd, dato):
		# Schema messaggio generato <comando(1byte)><dato(1byte)><checksum(1byte)><carattere_terminatore(1byte)>
		# Secondo lo standard di comunicazione questo e' un messaggio tipico del Raspberry

		if(self.isConnected()):
			msg=cmd+dato 							# Compone il messaggio
			msg+=chr(self.genChecksum(cmd,dato)) 	# Genera il checksum
			msg+=self.charTerminator 				# Aggiunge il carattere terminatore
			self.sendBuffer+=msg 					# Salva il messaggio nel buffer dei messaggi inviati
			self.ser.write(msg) 					# Invia il messaggio

	def sendCommand16(self, cmd, dato1, dato0):
		# Schema messaggio generato <comando(1byte)><dato(2byte)><checksum(1byte)><carattere_terminatore(1byte)>
		# Secondo lo standard di comunicazione questo e' un messaggio tipico del Tiva

		if(self.isConnected()):
			msg=cmd+dato1+dato0 							# Compone il messaggio
			msg+=chr(self.genChecksum16(cmd,dato1,dato0)) 	# Genera il checksum
			msg+=self.charTerminator 						# Aggiunge il carattere terminatore
			self.sendBuffer+=msg 							# Salva il messaggio nel buffer dei messaggi inviati
			self.ser.write(msg) 							# Invia il messaggio

	def genChecksum(self, cmd, dato):
		# Calcola il checksum partendo dal comando e dal dato a 8 bit passato

		# Viene prelevato il valore ASCII del carattere
		cmdA=ord(cmd)
		datoA=ord(dato)

		# Viene fatto lo XOR con tutti i caratteri e il valore 0xA9
		chsm=cmdA ^ datoA ^ 0xA9

		# Viene restituito il risultato
		return chsm

	def genChecksum16(self, cmd, dato1, dato0):
		# Calcola il checksum partendo dal comando e dal dato a 16 bit passato
		cmdA=ord(cmd)

		# Viene prelevato il valore ASCII del carattere
		datoA=ord(dato1)
		datoB=ord(dato0)

		# Viene fatto lo XOR con tutti i caratteri e il valore 0xA9
		chsm=cmdA ^ datoA ^ datoB ^ 0xA9

		# Viene restituito il risultato
		return chsm

	################################
	# Inoltro comandi preimpostati #
	################################

	def goForward(self):
		# Invia un comando di spostamento in avanti
		if(self.isConnected()):
			self.sendCommand("F","0")

			if(self.receive()):
				if(self.lastReceive[2] == "1"):
					return True,True
				else:
					return False,True
			else:
				if(self.lastReceive[2] == "1"):
					return True,False
				else:
					return False,False

	def goBack(self):
		# Invia un comando di spostamento indietro
		if(self.isConnected()):
			self.sendCommand("B","0")

			if(self.receive()):
				if(self.lastReceive[2] == "1"):
					return True,True
				else:
					return False,True
			else:
				if(self.lastReceive[2] == "1"):
					return True,False
				else:
					return False,False

	def goBackGrad(self):
		# Invia un comando di rotazione di 180 gradi
		if(self.isConnected()):
			self.sendCommand("I","0")

			if(self.receive()):
				if(self.lastReceive[2] == "1"):
					return True,True
				else:
					return False,True
			else:
				if(self.lastReceive[2] == "1"):
					return True,False
				else:
					return False,False

	def goRight(self):
		# Invia un comando di spostamento a destra
		if(self.isConnected()):
			self.sendCommand("R","0")

			if(self.receive()):
				if(self.lastReceive[2] == "1"):
					return True,True
				else:
					return False,True
			else:
				if(self.lastReceive[2] == "1"):
					return True,False
				else:
					return False,False

	def goLeft(self):
		# Invia un comando di spostamento a sinistra
		if(self.isConnected()):
			self.sendCommand("L","0")

			if(self.receive()):
				if(self.lastReceive[2] == "1"):
					return True,True
				else:
					return False,True
			else:
				if(self.lastReceive[2] == "1"):
					return True,False
				else:
					return False,False

	def goStop(self):
		# Invia un comando di stop
		if(self.isConnected()):
			self.sendCommand("S","0")

			if(self.receive()):
				if(self.lastReceive[2] == "1"):
					return True,True
				else:
					return False,True
			else:
				if(self.lastReceive[2] == "1"):
					return True,False
				else:
					return False,False

	def goGrad(self,grad):
		# Invia un comando di rotazione in gradi
		if(self.isConnected()):
			self.sendCommand("G",str(grad))

			if(self.receive()):
				if(self.lastReceive[2] == "1"):
					return True,True
				else:
					return False,True
			else:
				if(self.lastReceive[2] == "1"):
					return True,False
				else:
					return False,False

	def requestSensor(self, idSens):
		# Richiede lo stato di un sensore
		status = False	# Risultato verifica checksum sulla risposta del Tiva alla richiesta

		if(self.isConnected()):
			self.sendCommand("D",chr(idSens))

			if(self.receive()):
				ret=(ord(self.lastReceive[1])*(2**8))+(ord(self.lastReceive[2]))
				return ret,True
			else:
				ret=(ord(self.lastReceive[1])*(2**8))+(ord(self.lastReceive[2]))
				return ret,False
