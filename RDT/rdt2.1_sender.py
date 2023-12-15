import socket
import hashlib
import random

# Function to corrupt the message with a 30% probability
def corrupt_message(message):
    if random.random() < 0.3:  # 30% probability of corruption
        index = random.randint(0, len(message) - 1)
        message = message[:index] + bytes([message[index] ^ 1]) + message[index + 1:]
    return message

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(("localhost", 2000))  # Replace with actual receiver IP and port

    seq_num = 0  # Initialize the sequence number

    while True:
        print("\n")
        message = input("Enter a message to send: ")

        # Calculate the checksum
        checksum = calculate_checksum(message.encode())

        message_corrupted = corrupt_message(message.encode())

        # Prepare the packet with sequence number
        packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()
        sender_socket.send(packet)

        ack = sender_socket.recv(1024).decode()

        while True:
            if ack == "ACK":
                print(f"Message {seq_num} sent successfully.")
                seq_num = 1 - seq_num  # Toggle the sequence number (0 or 1)
                break
            elif ack == "NAK":
                print(f"Message {seq_num} corrupted. Resending...")
            else:
                print("Unknown acknowledgment. Resending...")
            
            # Resend the packet with the same sequence number
            message_corrupted = corrupt_message(message.encode())

            # Prepare the packet with sequence number
            packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()
            sender_socket.send(packet)
            ack = sender_socket.recv(1024).decode()

        if message.lower() == 'exit':
            print("Tearing down the connection\n")
            break

    sender_socket.close()

if __name__ == "__main__":
    main()

