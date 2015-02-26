# Raspberry - Server Seriale | Corso robotica 2014/15 - ITIS E. Mattei Urbino
# Write using Python 2.7
# To install PySerial -> python -m pip install pyserial

from RoboSerial import RoboSerial

com=RoboSerial()
com.OpenConnection()

closeCommand= "exit"

### Printing connection information ###
#print ("[Info] Serial connection open on port " + com_num)
#print ("[Info] Baudrate set to " + str(baud))
#print ("[Info] Character terminator set to (" + charTerminator + ")")
print ("[Info] Enter " + closeCommand + " to close the program")

### Send command to serial ###
	while True:
		buffer=""
		num = 0
		lenRead = 0
		buffer = raw_input("[Msg] --> ")
		if (buffer == closeCommand):
			break
		com.Send(buffer) 
	print ("\n[Info] Detected close command. The program will be terminated.")
	com.close() #Close connection
	print ("[Info] Serial connection closed.")
