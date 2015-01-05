#include "comunicazione.cpp"

void giraDestra(int sd)
{
	Send(sd, "r");
}

void giraSinistra(int sd)
{
	Send(sd, "l");
}

void avanti(int sd)
{
	Send(sd, "a");
}

int sensore(int sd, char sens_id)
{
	char sens[3] = "s";
	sens[1] = sens_id;
	sens[2] = 0;
	return Chiedo(sd, sens);
}
