import socket
import hashlib
import random

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
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_addr = ("localhost", 2000)

    seq_num = 0  # Initialize the sequence number

    while True:
        print("\n")
        message = input("Enter a message to send: ")
        if message.lower() == 'exit':
            message_corrupted = message.encode()
        else:
            # Calculate the checksum
            checksum = calculate_checksum(message.encode())

            message_corrupted = corrupt_message(message.encode())

        # Prepare the packet with sequence number
        packet = f"{seq_num}|{message_corrupted.decode()}|{checksum}".encode()
        sender_socket.sendto(packet, receiver_addr)
        print(f"Packet sent with seq no {seq_num}")

        if message.lower() == 'exit':
            print("Tearing down the connection\n")
            break

        ack, _ = sender_socket.recvfrom(1024)

        while True:
            ack = ack.decode()
            if ack == f"ACK{seq_num}":
                print(f"Message {seq_num} sent successfully.")
                seq_num = 1 - seq_num  # Toggle the sequence number (0 or 1)
                break
            elif ack == f"ACK{1 - seq_num}":
                print(f"Received {ack}... Message {seq_num} corrupted. Resending...")
            else:
                print("Unknown acknowledgment. Resending...")

            # Resend the packet with the same sequence number
            message_corrupted = corrupt_message(message.encode())

            # Prepare the packet with the sequence number
            packet = f"{seq_num}|{message_corrupted.decode()}|{checksum}".encode()
            sender_socket.sendto(packet, receiver_addr)
            ack, _ = sender_socket.recvfrom(1024)

    sender_socket.close()

if __name__ == "__main__":
    main()

