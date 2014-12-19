all : ser cli

cli : cli.cpp
	g++ cli.cpp -o cli
	
ser : ser.cpp
	g++ ser.cpp -o ser
