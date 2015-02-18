# Raspberry - Client seriale | Corso robotica - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

import serial

####### CONNECTION PARAMETERS #######
port = "/dev/ttyAMA0" # Specify serial post
altport = "COM2" # Specify alternative serial post
baud = 9600 # Set baudrate to 9600bps
charTerminator="*" # Character that determines the end of the communication
#####################################

try:
	open=True;
	ser = serial.Serial(port, baud)  #Opening serial port
	com_num = ser.portstr
except:
	# In case of connection error
	print ("[Sys] Unable to open port " + port + ". Trying alternarive port.")
	open=False;
	try:
		open=True;
		ser = serial.Serial(altport, baud)  #Opening serial port
		com_num = ser.portstr
	except:
		print ("[Sys] Unable to open alternative port " + altport + "The program will be terminated.")
		open=False;

if open: #Check if connection is open
	try:
		### Printing connection information ###
		print ("[Sys] Serial connection open on port " + com_num)
		print ("[Sys] Baudrate set to " + str(baud))
		print ("[Sys] Character terminator set to (" + charTerminator + ")")
		### Read data from serial ###
		while True:
			read=""
			num = 0
			lenRead = 0
			while True:
				num = ser.inWaiting()
				lenRead = len(read)
				#print ("["+str(lenRead)+"] ["+read+"]") #Only for debugging
				lenRead=lenRead-1
				if (lenRead > 0 and read[lenRead] == charTerminator): # Detecting end of communication character
					break
				elif (num!=0):
					read+=ser.read(num)
			print ("[Ser] Recived: " + read[0:lenRead-1]) # Print serial buffer
	except:
		print ("\n[Sys] Keyboard interrupt detected. The program will be terminated.")
		ser.close()	 #Close connection
		print ("[Sys] Serial connection closed.")
