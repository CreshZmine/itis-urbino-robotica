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
	try:
		### Printing connection information ###
		print ("[Info] Serial connection open on port " + com_num)
		print ("[Info] Baudrate set to " + str(baud))
		print ("[Info] Character terminator set to (" + charTerminator + ")")
		print ("[Info] Press CTRL+C to close the program")
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
			print ("[Serial] Recived: " + read[0:lenRead-1]) # Print serial buffer
	except:
		print ("\n[Info] Keyboard interrupt detected. The program will be terminated.")
		ser.close()	 #Close connection
		print ("[Info] Serial connection closed.")
