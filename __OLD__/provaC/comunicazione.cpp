#ifndef COMUNICAZIONE_H

#define COMUNICAZIONE_H

#include <iostream>

using namespace std;

void Send(int sd, const char *msg)
{
    int len;
    ssize_t bytes_sent;
    len = strlen(msg);
    bytes_sent = send(sd, msg, len, 0);
    
}

void send_l (int sd, const char *msg, ssize_t len)
{
	send(sd, msg, len, 0);
}

int Receive(int sd, char *msg)
{
    int bytes = recv(sd, msg, 1000, 0);
    // If no data arrives, the program will just wait here until some data arrives.
    if (bytes == 0) cout << "host shut down." << endl ;
    if (bytes == -1) cout << "recieve error!" << endl ;
    //cout << bytes_recieved << " bytes recieved :" << endl ;
    msg[bytes] = '\0';
    
    return bytes;
}
 
/*botta e risposta*/
int Chiedo(int sd, char *msg)
{
    Send(sd,msg);
    return Receive(sd,msg);
}
#endif /* end of include guard: COMUNICAZIONE_H */
