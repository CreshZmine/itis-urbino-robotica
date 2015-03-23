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
		self.ReceiveBuffer = ""
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

		except:
			# In caso di errore con la porta principale
			try:
				self.ser = serial.Serial(self.altPort, self.baud)  # Tentativo di connessione con la porta alternativa
				self.port=self.altPort
			except:
				# In caso di errore con la porta alternativa
				self.ser=None # Imposta "ser" a null per mancata connessione
				
	def openConnectionPort(self, portCon):
		# NOTA -> Se non e' stato possibile aprire la comunicazione seriale ser verra' settato a null
		# !ATTENZIONE! -> Il Raspberry PI quando la porta seriale UART0 viene inizializzata invia un impulso negativo di 32us sul TX
		try:
			self.ser = serial.Serial(portCon, self.baud)  # Tentativo di connessione
			self.port=portCon
		except:
			# In caso di errore
			self.ser=None # Imposta "ser" a null per mancata connessione

	def closeConnection(self):
		if(self.ser != None):
			self.ser.close() # Chiude la connessione
			self.port="" # Modifica la stringa per la porta in uso
		
	def isConnceted(self):
		# Verifica se la comunicazione e' apera | True se e' apera | False se e' chiusa
		if(self.ser != None):
			return True
		else:
			return False
			
	#######################################
	# Funzioni per l'invio e la ricezione #
	#######################################
	
	def receive(self):
		if(self.ser != None):
			read=""
			num = 0
			lenRead = 0
			while True:
				num = self.ser.inWaiting() # Verifica quanti dati stanno per esserre ricevuti
				lenRead = len(read)-1
				if (lenRead > 0 and read[lenRead] == self.charTerminator): # Rileva il carattere di fine comunicazione
					break
				elif (num!=0):
					# Legge dalla seriale
					read+=self.ser.read(num)
			
			# Salva il messaggio ricevuto nel buffer
			self.ReceiveBuffer+=read
			
			# Rimuove il carattere terminatore della comunicazione
			read=read.replace(self.charTerminator," ")
			
			# La salvo come ultima stringa ricevuta
			self.lastReceive = read

			# Effettuo la verifica del checksun
			cksum = self.GenChecksum(read[lenRead-3], read[lenRead-2])
			
			if (cksum == ord(read[lenRead-1])):
				return True
			else:
				return False
		else:
		  	# Da sempre esito negativo alla verifica del checksum quando la connessione seriale non e' disposibile
			return False

	def send(self, msg):
		if(self.ser != None):
			msg+=self.charTerminator
			self.sendBuffer+=msg
			self.lastSend = msg
			self.ser.write(msg)
	
	def sendCommand(self, cmd, dato):
		# Schema messaggio generato <comando(char)><dato(8bit)><checksum(8bit)><carattere_terminatore(1byte)>
		if(self.ser != None):
			msg=cmd+dato # Compone il messaggio
			msg+=chr(self.GenChecksum(cmd,dato)) # Genera il checksum
			msg+=self.charTerminator # Aggiunge il carattere terminatore
			self.sendBuffer+=msg
			self.ser.write(msg)
			
	def genChecksum(self, cmd, dato):
		# Calcola il checksum partendo dal comando e dal dato passato
		cmdA=ord(cmd)
		datoA=ord(dato)
		chsm=cmdA ^ datoA ^ 0xA9
		
		return chsm
		
	################################
	# Inoltro comandi preimpostati #
	################################

	def goForward(self):
		# Invia un comando di spostamento in avanti
		if(self.ser != None):
			self.SendCommand("F","0")
			
	def goBack(self):
		# Invia un comando di spostamento indietro
		if(self.ser != None):
			self.SendCommand("B","0")
			
	def goBackGrad(self):
		# Invia un comando di rotazione di 180 gradi
		if(self.ser != None):
			self.SendCommand("I","0")
			
	def goRight(self):
		# Invia un comando di spostamento a destra
		if(self.ser != None):
			self.SendCommand("R","0")
			
	def goLeft(self):
		# Invia un comando di spostamento a sinistra
		if(self.ser != None):
			self.SendCommand("L","0")
			
	def goStop(self):
		# Invia un comando di stop
		if(self.ser != None):
			self.SendCommand("S","0")
			
	def goGrad(self,grad):
		# Invia un comando di rotazione in gradi
		if(self.ser != None):
			self.SendCommand("G",str(grad))

	def requestSensor(self, idSens):
		# Richiede lo stato di un sensore
		status = False	# Risultato verifica checksum sulla risposta del Tiva alla richiesta

		if(self.ser != None):
			self.SendCommand("D",str(idSens))
			status=self.Receive()

		return status
