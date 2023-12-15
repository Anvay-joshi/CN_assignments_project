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

    seq_num = 0

    while True:
        print("\n")
        message = input("Enter a message to send: ")

        checksum = calculate_checksum(message.encode())

        message_corrupted = corrupt_message(message.encode())

        packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()
        sender_socket.sendto(packet, receiver_addr)

        ack, _ = sender_socket.recvfrom(1024)

        while True:
            ack = ack.decode()
            if ack == "ACK":
                print(f"Message {seq_num} sent successfully.")
                seq_num = 1 - seq_num
                break
            elif ack == "NAK":
                print(f"Message {seq_num} corrupted. Resending...")
            else:
                print("Unknown acknowledgment. Resending...")

            message_corrupted = corrupt_message(message.encode())
            packet = str(seq_num).encode() + b"|" + message_corrupted + b"|" + str(checksum).encode()
            sender_socket.sendto(packet, receiver_addr)
            ack, _ = sender_socket.recvfrom(1024)

        if message.lower() == 'exit':
            print("Tearing down the connection\n")
            break

    sender_socket.close()

if __name__ == "__main__":
    main()

