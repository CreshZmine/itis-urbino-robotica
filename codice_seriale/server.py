# Raspberry - Server Seriale | Corso robotica - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

import serial, sys

####### CONNECTION PARAMETERS #######
port = "/dev/ttyAMA0" # Specify serial post
altport = "COM2" # Specify alternative serial post
baud = 9600 # Set baudrate to 9600bps
charTerminator = "*" # Character that determines the end of the communication
closeCommand = "exit" # Command that determines the end of the program
#####################################

try:
	open=True;
	ser = serial.Serial(port, baud)  #Opening serial port
	com_num = ser.portstr
except:
	# In case of connection error
	print ("[Warning] Unable to open port " + port + ". Trying alternarive port.")
	open=False;
	try:
		open=True;
		ser = serial.Serial(altport, baud)  #Opening serial port
		com_num = ser.portstr
	except:
		print ("[Warning] Unable to open alternative port " + altport + "The program will be terminated.")
		open=False;

if open: #Check if connection is open
	### Printing connection information ###
	print ("[Info] Serial connection open on port " + com_num)
	print ("[Info] Baudrate set to " + str(baud))
	print ("[Info] Character terminator set to (" + charTerminator + ")")
	print ("[Info] Enter " + closeCommand + " to close the program")
	### Send command to serial ###
	while True:
		buffer=""
		num = 0
		lenRead = 0
		buffer = raw_input("[Msg] --> ")
		if (buffer == closeCommand):
			break
		buffer+=" "+charTerminator
		ser.write(buffer)
	print ("\n[Info] Detected close command. The program will be terminated.")
	ser.close()		#Close connection
	print ("[Info] Serial connection closed.")