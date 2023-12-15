import socket
import random

def corrupt_message(message):
    if random.random() < 0.3:  # 30% probability of corruption
        index = random.randint(0, len(message) - 1)
        message = message[:index] + bytes([message[index] ^ 1]) + message[index + 1:]
        print("\t\tACK corrupted artificially")
    return message

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(("localhost", 2000))

    print("Receiver is ready to receive messages...")
    
    expected_seq_num = 0  # Initialize the expected sequence number

    while True:
        print("\n")
        packet, sender_addr = receiver_socket.recvfrom(1024)
        packet = packet.decode()
        seq_num, message, received_checksum = packet.split('|')
        if message.lower() == 'exit':
            print("Tearing down the connection")
            receiver_socket.close()
            exit()
        seq_num = int(seq_num)
        received_checksum = int(received_checksum)

        # Calculate the checksum for the received message
        checksum = calculate_checksum(message.encode())

        i = 0

        while not (checksum == received_checksum):
            if i == 5:
                break

            ack_corrupted = corrupt_message(f"ACK{1 - expected_seq_num}".encode())
            receiver_socket.sendto(ack_corrupted, sender_addr)
            print(f"Message corrupted... sending ACK{1 - expected_seq_num}")

            packet, sender_addr = receiver_socket.recvfrom(1024)
            packet = packet.decode()
            seq_num, message, received_checksum = packet.split('|')
            seq_num = int(seq_num)
            received_checksum = int(received_checksum)

            # Calculate the checksum for the received message
            checksum = calculate_checksum(message.encode())

            i += 1

        ack_corrupted = corrupt_message(f"ACK{1 - expected_seq_num}".encode())
        receiver_socket.sendto(ack_corrupted, sender_addr)

        if seq_num != expected_seq_num:
            print(f"Expected seq_no {expected_seq_num}... Received seq {seq_num}... Discarding duplicate packet")
        else:
            print(f"Received and delivered: {message} seq_no {seq_num}\nSending ACK{seq_num}")
            expected_seq_num = 1 - expected_seq_num  # Toggle the expected sequence number
            print(f"Next expected packet = {expected_seq_num}")

    receiver_socket.close()

if __name__ == "__main__":
    main()

