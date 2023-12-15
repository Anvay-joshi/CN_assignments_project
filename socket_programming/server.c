#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <unistd.h>

#define MAX_CONNECTIONS 4

int main() {
    int sockfd;

    // Create server-side socket
    sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    struct sockaddr_in my_addr;
    my_addr.sin_family = AF_INET; // IPv4
    my_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    my_addr.sin_port = htons(2000); // Use the desired port number

    bind(sockfd, (struct sockaddr *)&my_addr, sizeof(my_addr));
    listen(sockfd, MAX_CONNECTIONS);

    while (1) {
        struct sockaddr_in client_addr;
        int client_len = sizeof(client_addr);
        int client_fd = accept(sockfd, (struct sockaddr *)&client_addr, &client_len);

        char message[1024];
        while (1) {
            // Receive a message from the client
            int bytes_received = recv(client_fd, message, sizeof(message), 0);

            // Check if the client disconnected
            if (bytes_received <= 0) {
                close(client_fd);
                break;
            }

            // Print the received message
            message[bytes_received] = '\0'; // Null-terminate the string
            printf("Received from client: %s\n", message);

            // Send a reply to the client
            printf("Enter your reply: ");
            fgets(message, sizeof(message), stdin); // Get user input
            send(client_fd, message, strlen(message), 0);
        }
    }

    return 0;
}

