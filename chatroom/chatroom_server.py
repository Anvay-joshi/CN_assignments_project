'''
A chat room application in which each user first enters by giving his/her name and start sharing textual messages with all other users available in the chat room.

The user can see all the messages with the sender names (given at the start of entering into the chat room) with a current receiving time of the message.

When anybody leaves the chat room a message to all current chat applicants available in the chat room is able to see that the corresponding user left.

Every message from the user contains its receiving time as well.

Here the application is to be implemented like a multithreaded two-way communication program with necessary synchronization among the threads
'''


' Server side '

import threading
import socket

# Get host and connection port
host = 'localhost'
#host = '10.100.106.188'
port = 59000

# Connect server via TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []

# broadcast: handles client broadcasts
def broadcast(message):
    for client in clients:
        client.send(message)

# handle_client: handles client requests
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room'.encode('utf-8'))
            aliases.remove(alias)
            break

# Main function to receive the clients connection
def receive():
    while True:
        print('Server is ready')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(100)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias}: connected to the chat room'.encode('utf-8'))
        client.send('\nUser connected!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Main code
if __name__ == "__main__":
    receive()
