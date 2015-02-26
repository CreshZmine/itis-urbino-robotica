# Raspberry - Client seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.OpenConnection()

try:
	### Printing connection information ###
	#print ("[Info] Serial connection open on port " + com_num)
	#print ("[Info] Baudrate set to " + str(baud))
	#print ("[Info] Character terminator set to (" + charTerminator + ")")
	print ("[Info] Press CTRL+C to close the program")

	### Read data from serial ###
	while True:
		read=com.Recive()
		print ("[Serial] Recived: " + read) # Print serial buffer
except:
	print ("\n[Info] Keyboard interrupt detected. The program will be terminated.")
	com.CloseConnection() #Close connection
	print ("[Info] Serial connection closed.")
