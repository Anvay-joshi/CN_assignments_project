#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <netdb.h>
#include <unistd.h>
#include <stdlib.h>

//#define SERVER_IP "10.100.109.249" // Change this to the server's IP address
//#define SERVER_PORT 2000

int main(int argc, char** argv) {
    if(argc != 3){
        printf("Usage: ./client [SERVER_IP] [SERVER_PORT]");
        return 0;
    }
    /* Configure the server address */
    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    //server_addr.sin_addr.s_addr = inet_addr(SERVER_IP);
    //server_addr.sin_port = htons(SERVER_PORT);
    server_addr.sin_addr.s_addr = inet_addr(argv[1]);
    server_addr.sin_port = htons( atoi(argv[2]) );

    /* Create client-side socket */
    int sockfd;
    sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    /* Connect to the server */
    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Connection failed");
        return 1;
    }

    char message[1024];

    while (1) {
        // Get user input
        printf("Enter your message: ");
        fgets(message, sizeof(message), stdin);

        // Send the message to the server
        send(sockfd, message, strlen(message), 0);

        // Receive the server's reply
        int bytes_received = recv(sockfd, message, sizeof(message), 0);
        if (bytes_received <= 0) {
            perror("Server disconnected");
            break;
        }

        // Null-terminate the received message
        message[bytes_received] = '\0';

        // Print the server's reply
        printf("Received from server: %s", message);
    }

    close(sockfd);

    return 0;
}

