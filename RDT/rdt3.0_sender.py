import socket
import hashlib
import random
import time

def corrupt_message(message):
    if random.random() < 0.1:  # 10% probability of corruption
        index = random.randint(0, len(message) - 1)
        message = message[:index] + bytes([message[index] ^ 1]) + message[index + 1:]
    return message

def send_packet_unreliable(sender_socket, packet):
    if random.random() < 0.9:  # 10% probability of corruption
        sender_socket.send(packet)
    else:
        print("\t\tPacket lost artificially from from sender side")


def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(("localhost", 2000))  # Replace with the actual receiver IP and port

    seq_num = 0  # Initialize the sequence number

    while True:
        print("\n")
        message = input("Enter a message to send: ")

        # Calculate the checksum
        checksum = calculate_checksum(message.encode())

        message_corrupted = corrupt_message(message.encode())

        # Prepare the packet with sequence number
        packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()

        #sender_socket.send(packet)
        send_packet_unreliable(sender_socket, packet)

        ack_received = False
        start_time = time.time()

        while not ack_received:
            sender_socket.settimeout(5.0)  

            try:
                ack = sender_socket.recv(1024).decode()
                if ack == "ACK" + str(seq_num):
                    print(f"Message {seq_num} sent successfully.")
                    seq_num = 1 - seq_num  # Toggle the sequence number (0 or 1)
                    ack_received = True
                elif ack == "ACK" + str(1 - seq_num):
                    print(f"Out of order packet sent")
                else:
                    print("Unknown acknowledgment. Resending {seq_num}...")
            except socket.timeout:
                print(f"Timeout. Resending seq_no {seq_num}...")
                message_corrupted = corrupt_message(message.encode())
                packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()
                #sender_socket.send(packet)
                send_packet_unreliable(sender_socket, packet)

        if message.lower() == 'exit':
            print("Tearing down the connection\n")
            exit()

    sender_socket.close()

if __name__ == "__main__":
    main()

