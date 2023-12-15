import socket
import hashlib
import random

# Function to corrupt the message with a 30% probability
def corrupt_message(message):
    if random.random() < 0.3:  # 30% probability of corruption
        # Select a random position to corrupt
        index = random.randint(0, len(message) - 1)
        
        # Flip one bit (XOR with 1)
        message = message[:index] + bytes([message[index] ^ 1]) + message[index + 1:]
    
    return message

def calculate_checksum(data):
    #checksum = hashlib.md5(data).hexdigest()
    checksum = 0

    for byte in data:
        checksum ^= byte

    return checksum

def main():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(("localhost", 2000))

    while True:
        message = input("Enter a message to send: ")

        checksum = calculate_checksum(message.encode())

        message_corrupted = corrupt_message(message.encode())

        packet = message_corrupted + b"|" + str(checksum).encode()
        sender_socket.send(packet)

        ack = sender_socket.recv(1024).decode()

        while (ack != "ACK"):
            print("Message corrupted. Resending the packet")

            message_corrupted = corrupt_message(message.encode())

            packet = message_corrupted + b"|" + str(checksum).encode()

            sender_socket.send(packet)
            ack = sender_socket.recv(1024).decode()

#            i += 1
#            if(i == 5):
#                break

        if ack == "ACK":
            print("Message sent successfully.")

        if(message.lower() == 'exit'):
            print("Tearing down the connection\n")
            break

    sender_socket.close()

if __name__ == "__main__":
    main()

