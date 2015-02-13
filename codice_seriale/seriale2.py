# Raspberry - Seriale | Corso robotica - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

import serial

####### CONNECTION PARAMETERS #######
port = "COM3" # Specify serial post
baud = 9600 # Set baudrate to 9600bps
#####################################

ser = serial.Serial(port, baud)  #Opening serial port

if ser.isOpen():	#Check if connection is open
	com_num = ser.portstr
	print ("Porta " + com_num + " aperta")
	### Send command to serial ###
	buffer = "Hi! I'm a test from client 1"
	ser.write(buffer)      
	### Wait for data ###
	num = 0
	while num == 0:
		num = ser.inWaiting()
	### Get Serial Buffer ###
	buffer = ser.read(num)
	print ("Dati ricevuti dalla seriale: ")
	print buffer
	ser.close()		#Close connection
else:
	print ("Porta seriale gia' in uso o inesistente") 
	s = raw_input("Digita INVIA per uscire")