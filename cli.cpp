#include <iostream>
#include <cstring>      // Needed for memset
#include <sys/socket.h> // Needed for the socket functions
#include <netdb.h>      // Needed for the socket functions

#include <unistd.h>
#include "comunicazione.cpp"
#include "movimenti.cpp"

using namespace std;

//sequenza prefissata per prova..
char seq[]={'a','a','a','a','a','a','r','a','a','a','l','a','a','a','r'};

int main()
{
    int status;
    struct addrinfo host_info;       // The struct that getaddrinfo() fills up with data.
    struct addrinfo *host_info_list; // Pointer to the to the linked list of host_info's.

    // The MAN page of getaddrinfo() states "All  the other fields in the structure pointed
    // to by hints must contain either 0 or a null pointer, as appropriate." When a struct
    // is created in c++, it will be given a block of memory. This memory is not nessesary
    // empty. Therefor we use the memset function to make sure all fields are NULL.
    memset(&host_info, 0, sizeof host_info);

    cout << "Setting up the structs..."  << endl;

    host_info.ai_family = AF_UNSPEC;     // IP version not specified. Can be both.
    host_info.ai_socktype = SOCK_STREAM; // Use SOCK_STREAM for TCP or SOCK_DGRAM for UDP.

    // Now fill up the linked list of host_info structs with google's address information.
    //status = getaddrinfo("www.google.com", "80", &host_info, &host_info_list);
    status = getaddrinfo("127.0.0.1", "5556", &host_info, &host_info_list);
    
    // getaddrinfo returns 0 on succes, or some other value when an error occured.
    // (translated into human readable text by the gai_gai_strerror function).
    if (status != 0)  cout << "getaddrinfo error" << gai_strerror(status) ;


    cout << "Creating a socket..."  << endl;
    int socketfd ; // The socket descripter
    socketfd = socket(host_info_list->ai_family, host_info_list->ai_socktype,
                      host_info_list->ai_protocol);
    if (socketfd == -1)  cout << "socket error " ;


    cout << "Connecting..."  << endl;
    status = connect(socketfd, host_info_list->ai_addr, host_info_list->ai_addrlen);
    if (status == -1)  std::cout << "connect error" ;


    
    char buffer[1000];
    int count = 0;
    int i = 0;
    
    buffer[0]='s';
    buffer[1]='0';
    buffer[2]='\0';
        
        
    Chiedo(socketfd,buffer);
    cout << buffer << endl;

    cout << sensore(socketfd, 0) << endl;
  
    while ( buffer[0] != '*' && count++ < 14 ) {
        
        //strcpy(buffer,"a");
        buffer[0]=seq[i];
        buffer[1]='\0';
        i++;
     
        Chiedo(socketfd,buffer);
        cout << buffer << endl;
    }
    
    
    cout << "Receiving complete. Closing socket..." << endl;
    freeaddrinfo(host_info_list);
    close(socketfd);

}
