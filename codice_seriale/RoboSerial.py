# Raspberry | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

import serial

class RoboSerial: 
	def __init__(self): 
		self.port = "/dev/ttyAMA0" # Specify serial post
		self.altport = "COM2" # Specify alternative serial post
		self.baud = 9600 # Set baudrate to 9600bps
		self.charTerminator="*" # Character that determines the end of the communication
		self.ser=None
	
	def OpenConnection(self):
		# !NOTE!
		# If there are any connection error "ser" will be return as a null object
		try:
			self.ser = serial.Serial(self.port, self.baud)  #Opening serial port
		except:
			# In case of connection error to first port
			# print ("[Warning] Unable to open port " + self.port + ". Trying alternarive port.")
			try:
				# Connection with alternative port
				self.ser = serial.Serial(self.altport, self.baud)  #Opening serial port
			except:
				# print ("[Warning] Unable to open alternative port " + self.altport)
				slef.ser=None

	def CloseConnection(self):
		if (self.ser != None):
			# Check if connection is opened
			self.ser.close() #Close connection
			#print ("[Info] Serial connection closed.")
			
	def Recive(self):
		if (self.ser != None):
			# Check if connection is opened
			read=""
			num = 0
			lenRead = 0
			while True:
				num = self.ser.inWaiting()
				lenRead = len(read)
				lenRead=lenRead-1
				if (lenRead > 0 and read[lenRead] == self.charTerminator): # Detecting end of communication character
					break
				elif (num!=0):
					read+=self.ser.read(num)
			return read
		else:
			return ""
	
	def Send(self, msg):
		if (self.ser != None):
			# Check if connection is opened
			msg+=" "+self.charTerminator
			self.ser.write(msg)
