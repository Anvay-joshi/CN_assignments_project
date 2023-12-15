import socket
import random

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def send_packet_unreliable(conn, seq_num):
    if random.random() < 0.9:  # 10% probability of corruption
        conn.send(f"ACK{seq_num}".encode())
    else:
        print("\t\tAck lost actificially from reciever side")

def main():

    # TODO Add duplicate package handling

    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(("localhost", 2000))  # Replace with the actual receiver IP and port
    receiver_socket.listen(1)

    print("Receiver is ready to receive messages...")

    conn, addr = receiver_socket.accept()

    expected_seq_num = 0  # Initialize the expected sequence number

    while True:
        print("\n")
        packet = conn.recv(1024).decode()
        seq_num, message, received_checksum = packet.split('|')
        seq_num = int(seq_num)
        received_checksum = int(received_checksum)

        # Calculate the checksum for the received message
        checksum = calculate_checksum(message.encode())

        if seq_num == expected_seq_num and checksum == received_checksum:
            #conn.send(f"ACK{seq_num}".encode())
            send_packet_unreliable(conn, seq_num)
            print(f"Received and delivered: {message}\nSending ACK{seq_num}")
            expected_seq_num = 1 - expected_seq_num  # Toggle the expected sequence number
        elif seq_num == 1 - expected_seq_num and checksum == received_checksum:
            print(f"Duplicate or out of sequence packet received...")
            print(f"packet received {seq_num}... Expected seq_no = {expected_seq_num}")
            send_packet_unreliable(conn, seq_num)

        if message.lower() == 'exit':
            break

    receiver_socket.close()

if __name__ == "__main__":
    main()

