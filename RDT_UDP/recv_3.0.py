import socket
import random

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def send_packet_unreliable(conn, seq_num, sender_addr):
    if random.random() < 0.9:  # 10% probability of corruption
        conn.sendto(f"ACK{seq_num}".encode(), sender_addr)
    else:
        print("\t\tAck lost artificially from receiver side")

def main():

    # TODO: Add duplicate package handling

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

        if seq_num == expected_seq_num and checksum == received_checksum:
            send_packet_unreliable(receiver_socket, seq_num, sender_addr)
            print(f"Received and delivered: {message}\nSending ACK{seq_num}")
            expected_seq_num = 1 - expected_seq_num  # Toggle the expected sequence number
        elif seq_num == 1 - expected_seq_num and checksum == received_checksum:
            print(f"Duplicate or out of sequence packet received...")
            print(f"Packet received {seq_num}... Expected seq_no = {expected_seq_num}")
            send_packet_unreliable(receiver_socket, seq_num, sender_addr)

        if message.lower() == 'exit':
            break

    receiver_socket.close()

if __name__ == "__main__":
    main()

