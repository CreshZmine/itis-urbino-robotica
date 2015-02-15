# Raspberry - Seriale | Corso robotica - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

import serial

####### CONNECTION PARAMETERS #######
port = "COM2" # Specify serial post
altport = "COM3" # Specify alternative serial post
baud = 9600 # Set baudrate to 9600bps
#####################################

try:
	open=True;
	ser = serial.Serial(port, baud)  #Opening serial port
	useport=port
except:
	print ("Unable to open port " + port + ". Trying alternarive port.")
	open=False;
	try:
		open=True;
		ser = serial.Serial(altport, baud)  #Opening serial port
		useport=altport
	except:
		print ("Unable to open alternative port " + altport)
		open=False;

if open:	#Check if connection is open
	com_num = ser.portstr
	print ("Porta " + com_num + " aperta")
	### Send command to serial ###
	buffer = "Comunication test from " + useport
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