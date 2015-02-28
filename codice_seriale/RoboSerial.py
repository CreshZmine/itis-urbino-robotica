# coding=utf-8

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
		self.usedPort = "" # Porta seriale attualmente attiva
		self.charStarter="#" # Carattere che determina l'inizio della comunicazione
		
		# Variabili aggiuntive
		self.charTerminator="*" # Carattere che determina la fine della comunicazione
		self.ser=None # Oggetto per comunicazione seriale
	
	def OpenConnection(self):
		# !NOTA! Se non è stato possibile aprire la comunicazione seriale ser verrà settato a null
		try:
			self.ser = serial.Serial(self.port, self.baud)  # Tentativo di connessione con la porta principale
			self.usedPort=self.port
		except:
			# In caso di errore con la porta principale
			try:
				self.ser = serial.Serial(self.altPort, self.baud)  # Tentativo di connessione con la porta alternativa
				self.usedPort=self.altPort
			except:
				# In caso di errore con la porta alternativa
				self.ser=None # Imposta "ser" a null per mancata connessione

	def CloseConnection(self):
		if (self.ser != None):
			self.ser.close() # Chiude la connessione
			self.usedPort="" # Modifica la stringa per la porta in uso
			
	def Recive(self):
		if (self.ser != None):
			read=""
			num = 0
			lenRead = 0
			while True:
				# Verifica quanti dati stanno per esserre ricevuti
				num = self.ser.inWaiting()
				lenRead = len(read)-1
				if (lenRead > 0 and read[lenRead] == self.charTerminator): # Rileva il carattere di fine comunicazione
					break
				elif (num!=0):
					# Legge dalla seriale
					read+=self.ser.read(num)
					
			# Rimuove il carattere terminatore della comunicazione
			read=read.replace(self.charTerminator," ")
			
			# Restituisce la stringa ricevuta
			return read
		else:
			# Restituisce una stringa vuota perchè la cominicazione non è disponibile
			return ""
	
	def IsConnceted(self):
		# Verifica se la comunicazione è apera | True se è apera | False se è chiusa
		if (self.ser != None):
			return True
		else:
			return False
			
	def SetBaudrate(self, baudrate):
		# Modifica il baudrate della connessione
		self.CloseConnection()
		self.baud=baudrate
		self.OpenConnection()
		
	def GetBaudrate(self):
		return self.baud
	
	def GetPort(self):
		return self.usedPort
	
	def GetCharStarter(self):
		return self.charStarter
		
	def GetCharTerminator(self):
		return self.charTerminator

	def Send(self, msg):
		if (self.ser != None):
			msg+=self.charTerminator
			self.ser.write(msg)

	def GoForward(self):
		# Invia un comando di spostamento in avanti
		if(self.ser!=None):
			msg="f"
			self.Send(msg)
	def GoBack(self):
		# Invia un comando di spostamento indietro
		if(self.ser!=None):
			msg="b"
			self.Send(msg)

	def RequestSensor(self, idSens):
		# Richiede lo stato di un sensore
		if(self.ser!=None):
			msg="s"+chr(idSens)
			self.Send(msg)
