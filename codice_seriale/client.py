# Raspberry - Client seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.OpenConnection()

try:
	### Printing connection information ###
	print ("[Info] Serial connection open on port " + str(com.GetPort()))
	print ("[Info] Baudrate set to " + str(com.GetBaudrate()))
	print ("[Info] Character starter set to (" + com.GetCharStarter() + ")")
	print ("[Info] Character terminator set to (" + com.GetCharTerminator() + ")")
	print ("[Info] Press CTRL+C to close the program")

	### Read data from serial ###
	if(com.IsConnceted()):
		while True:
			read=com.Recive()
			print ("[Serial] Recived: " + read) # Print serial buffer
	else:
		print ("\n[Info] Unable to connect to serial.")
except (KeyboardInterrupt, SystemExit):
	print ("\n[Info] Keyboard interrupt detected. The program will be terminated.")
	com.CloseConnection() #Close connection
	print ("[Info] Serial connection closed.")
