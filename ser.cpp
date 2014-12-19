#include <iostream>
#include <cstring>      // Needed for memset
#include <sys/socket.h> // Needed for the socket functions
#include <netdb.h>      // Needed for the socket functions

#include <unistd.h>

using namespace std;



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
    
void Send(int sd, const char *msg)
{
    // cout << "send()ing back a message..."  << endl;
    //char *msg = "thank you.";
    int len;
    ssize_t bytes_sent;
    len = strlen(msg);
    bytes_sent = send(sd, msg, len, 0);
	
}

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
    host_info.ai_flags = AI_PASSIVE;     // IP Wildcard

    // Now fill up the linked list of host_info structs with google's address information.
    status = getaddrinfo(NULL, "5556", &host_info, &host_info_list);
    // getaddrinfo returns 0 on succes, or some other value when an error occured.
    // (translated into human readable text by the gai_gai_strerror function).
    if (status != 0)  std::cout << "getaddrinfo error" << gai_strerror(status) ;
	
    std::cout << "Creating a socket..."  << std::endl;
    int socketfd = socket(host_info_list->ai_family, host_info_list->ai_socktype,
                      host_info_list->ai_protocol);
    if (socketfd == -1)  std::cout << "socket error " ;

    cout << "Binding socket..."  << endl;
    // we use to make the setsockopt() function to make sure the port is not in use
    // by a previous execution of our code. (see man page for more information)
    int yes = 1;
    status = setsockopt(socketfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));
    status = bind(socketfd, host_info_list->ai_addr, host_info_list->ai_addrlen);
    if (status == -1)  std::cout << "bind error" << std::endl ;
	
	int new_sd;
	while( true ) {

		std::cout << "Listen()ing for connections..."  << std::endl;
		status =  listen(socketfd, 5);
		if (status == -1)  std::cout << "listen error" << std::endl ;


		
		struct sockaddr_storage their_addr;
		socklen_t addr_size = sizeof(their_addr);
		new_sd = accept(socketfd, (struct sockaddr *)&their_addr, &addr_size);
		if (new_sd == -1)
		{
			std::cout << "listen error" << std::endl ;
		}
		else
		{
			std::cout << "Connection accepted. Using new socketfd : "  <<  new_sd << std::endl;
		}


		std::cout << "Waiting to recieve data..."  << std::endl;
		ssize_t bytes_recieved;
		
		char buffer[1000];
		int b;
		while( true ) {
			b=Receive(new_sd,buffer);
			if (b<=0) break;
			cout << buffer << endl;
			Send(new_sd,"Grazie 1!");

		}

		std::cout << "Stopping server...." << std::endl;
		
		
	}
	freeaddrinfo(host_info_list);
	close(new_sd);
    close(socketfd);

return 0 ;
}
