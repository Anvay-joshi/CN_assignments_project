import socket
import random

# Function to corrupt the message with a 30% probability
def corrupt_message(message):
    if random.random() < 0.3:  # 30% probability of corruption
        index = random.randint(0, len(message) - 1)
        message = message[:index] + bytes([message[index] ^ 1]) + message[index + 1:]
        print("\t\tack corrupted artificially")
    return message

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():

# TODO: add duplicate package management

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
        if(message.lower() == 'exit'):
            print("tearing down")
            receiver_socket.close()
            exit()
        seq_num = int(seq_num)
        received_checksum = int(received_checksum)

        # Calculate the checksum for the received message
        checksum = calculate_checksum(message.encode())
        print(message)

        i = 0

        while not (checksum == received_checksum):

            if i == 5:
                break

            ack_corrupted = corrupt_message(f"ACK{1-expected_seq_num}".encode())
            conn.send(ack_corrupted)
            print(f"Message corrupted... sending ACK{1-expected_seq_num}")

            packet = conn.recv(1024).decode()
            seq_num, message, received_checksum = packet.split('|')
            seq_num = int(seq_num)
            received_checksum = int(received_checksum)

            # Calculate the checksum for the received message
            checksum = calculate_checksum(message.encode())

            i += 1

        ack_corrupted = corrupt_message(f"ACK{1-expected_seq_num}".encode())
        conn.send(ack_corrupted)
        #conn.send(ack.encode())
        if(seq_num != expected_seq_num):
            print(f"expected seq_no {expected_seq_num}... received seq {seq_num}..   discarding duplicate packet")
        else:
            print(f"Received and delivered: {message} seq_no{seq_num}\nSending ACK{seq_num}")
            expected_seq_num = 1 - expected_seq_num  # Toggle the expected sequence number
            print(f"          next expected packet = {expected_seq_num}")

        #conn.send(f"ACK{seq_num}".encode())

    receiver_socket.close()

if __name__ == "__main__":
    main()

