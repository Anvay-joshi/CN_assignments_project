'''
A chat room application in which each user first enters by giving his/her name and start sharing textual messages with all other users available in the chat room.

The user can see all the messages with the sender names (given at the start of entering into the chat room) with a current receiving time of the message.

When anybody leaves the chat room a message to all current chat applicants available in the chat room is able to see that the corresponding user left.

Every message from the user contains its receiving time as well.

Here the application is to be implemented like a multithreaded two-way communication program with necessary synchronization among the threads
'''


' Client side '
import threading
import socket
alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 59000))
#client.connect(('10.100.106.188', 59000))

# client_receive: Handles messages received by client
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

# client_send: handles messages sent by client
def client_send():
    while True:
        message = (f'{alias} Enter: {input("")}')
        if (message == "Bye"):
            client.close()
        else:
            client.send(message.encode('utf-8'))

# Two threads are used for 1 client: one for sending, one for receiving
# Using the threading module
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
