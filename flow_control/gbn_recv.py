import socket
import random

def send_packet_unreliable(receiver_socket, sender_addr, ack):
    if random.random() < 0.9:  # 10% probability of corruption
        receiver_socket.sendto(str(ack).encode(), sender_addr)

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(("localhost", 2000))  # Replace with the actual receiver IP and port

    print("Receiver is ready to receive messages...")

    expected_seq_num = 0  # Initialize the expected sequence number
    ack = 0  # Initialize the expected ACK number

    while True:
        message, sender_addr = receiver_socket.recvfrom(1024)
        seq_num = int(message.decode().split()[1])

        if(seq_num == -1):
            break

        if seq_num == expected_seq_num:
            print(f"Received and delivered message {seq_num}: {message}")
            print(f"sending ACK{seq_num}")
            expected_seq_num += 1
            ack = expected_seq_num - 1
            #receiver_socket.sendto(str(ack).encode(), sender_addr)
            send_packet_unreliable(receiver_socket, sender_addr, ack)

        else:
            print(f"Out of sequence packet\n expected {expected_seq_num}, recieved {seq_num}")
            print(f"sending ACK{seq_num}")
            ack = seq_num
            #receiver_socket.sendto(str(ack).encode(), sender_addr)
            send_packet_unreliable(receiver_socket, sender_addr, ack)


if __name__ == "__main__":
    main()

