# Raspberry - RoboSerial | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Scritto per Python 2.7
# Per installare PySerial -> python -m pip install pyserial

import serial

class RoboSerial: 
	def __init__(self): 
		# Impostazioni di connessione
		self.port = "/dev/ttyAMA0" # Porta seriale principale
		self.altPort = "COM2" # Porta seriale alternativa (attualmente usate per la simulazione su Windows)
		self.baud = 115200 # Baudrate per la comunicazione seriale
		
		# Impostazioni di comunicazione
		self.charStarter="#" # Carattere che determina l'inizio della comunicazione
		self.charTerminator="*" # Carattere che determina la fine della comunicazione
		
		# Variabili aggiuntive
		self.ser = None # Oggetto per comunicazione seriale
		
		# Buffer di comunicazione
		self.reciveBuffer = ""
		self.sendBuffer = ""
	
	def __del__(self):
		# Chiusura connessione seriale
		self.ser.close()

	#######################################
	# Funzioni per la connessione seriale #
	#######################################
	
	def OpenConnection(self):
		# NOTA -> Se non e' stato possibile aprire la comunicazione seriale ser verra' settato a null
		try:
			self.ser = serial.Serial(self.port, self.baud)  # Tentativo di connessione con la porta principale
			self.ser.flushInput() # Scarta tutte le informazioni presenti nel buffer di input
			self.ser.flushOutput() # Scarta tutte le informazioni presenti nel buffer di input

		except:
			# In caso di errore con la porta principale
			try:
				self.ser = serial.Serial(self.altPort, self.baud)  # Tentativo di connessione con la porta alternativa
				self.ser.flushInput() # Scarta tutte le informazioni presenti nel buffer di input
				self.ser.flushOutput() # Scarta tutte le informazioni presenti nel buffer di input
			except:
				# In caso di errore con la porta alternativa
				self.ser=None # Imposta "ser" a null per mancata connessione
				
	def OpenConnectionPort(self, portCon):
		# NOTA -> Se non e' stato possibile aprire la comunicazione seriale ser verra' settato a null
		try:
			self.ser = serial.Serial(portCon, self.baud)  # Tentativo di connessione
			self.ser.flushInput() # Scarta tutte le informazioni presenti nel buffer di input
			self.ser.flushOutput() # Scarta tutte le informazioni presenti nel buffer di input
		except:
			# In caso di errore
			self.ser=None # Imposta "ser" a null per mancata connessione

	def CloseConnection(self):
		if(self.IsConnected()):
			self.ser.close() # Chiude la connessione
			self.usedPort="" # Modifica la stringa per la porta in uso
		
	def IsConnceted(self):
		# Verifica se la comunicazione e' apera | True se e' apera | False se e' chiusa
		if(self.IsConnected()):
			return True
		else:
			return False
			
	#####################
	# Funzioni pset/get #
	#####################
	
	def SetBaudrate(self, baudrate):
		# Modifica il baudrate della connessione
		self.CloseConnection()
		self.baud=baudrate
		self.OpenConnection()
		
	def GetBaudrate(self):
		return self.baud
	
	def GetPort(self):
		return self.ser.name
	
	def GetCharStarter(self):
		return self.charStarter
		
	def GetCharTerminator(self):
		return self.charTerminator
		
	def GetReciveBuffer(self):
		return self.reciveBuffer
		
	def GetSendBuffer(self):
		return self.sendBuffer
	
	#######################################
	# Funzioni per l'invio e la ricezione #
	#######################################
	
	def Recive(self):
		if(self.IsConnected()):
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
			self.reciveBuffer+=read
			
			# Rimuove il carattere terminatore della comunicazione
			read=read.replace(self.charTerminator," ")
			
			# Restituisce la stringa ricevuta
			return read
		else:
			# Restituisce una stringa vuota perche' la cominicazione non e' disponibile
			return ""

	def Send(self, msg):
		if(self.IsConnected()):
			msg+=self.charTerminator
			self.sendBuffer+=msg
			self.ser.write(msg)
	
	def SendCommand(self, cmd, dato):
		# Schema messaggio generato <comando(char)><dato(8bit)><checksum(8bit)>
		if(self.IsConnected()):
			msg=cmd+dato # Compone il messaggio
			msg+=chr(self.GenChecksum(cmd,dato)) # Genera il checksum
			msg+=self.charTerminator # Aggiunge il carattere terminatore
			self.sendBuffer+=msg
			self.ser.write(msg)
			
	def GenChecksum(self, cmd, dato):
		# Calcola il checksum partendo dal comando e dal dato passato
		cmdA=ord(cmd)
		datoA=ord(dato)
		chsm=cmdA ^ datoA ^ 0xA9
		
		return chsm
		
	################################
	# Inoltro comandi preimpostati #
	################################

	def GoForward(self):
		# Invia un comando di spostamento in avanti
		if(self.IsConnected()):
			self.SendCommand("F","0")
			
	def GoBack(self):
		# Invia un comando di spostamento indietro
		if(self.IsConnected()):
			self.SendCommand("B","0")
			
	def GoBackGrad(self):
		# Invia un comando di rotazione di 180 gradi
		if(self.IsConnected()):
			self.SendCommand("I","0")
			
	def GoRight(self):
		# Invia un comando di spostamento a destra
		if(self.IsConnected()):
			self.SendCommand("R","0")
			
	def GoLeft(self):
		# Invia un comando di spostamento a sinistra
		if(self.IsConnected()):
			self.SendCommand("L","0")
			
	def GoStop(self):
		# Invia un comando di stop
		if(self.IsConnected()):
			self.SendCommand("S","0")
			
	def GoGrad(self,grad):
		# Invia un comando di rotazione in gradi
		if(self.IsConnected()):
			self.SendCommand("G",str(grad))

	def RequestSensor(self, idSens):
		# Richiede lo stato di un sensore
		if(self.IsConnected()):
			self.SendCommand("D",str(idSens))
