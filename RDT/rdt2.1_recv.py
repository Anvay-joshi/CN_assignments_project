import socket
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
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(("localhost", 2000))  # Replace with actual receiver IP and port
    receiver_socket.listen(1)

    print("Receiver is ready to receive messages...")

    conn, addr = receiver_socket.accept()

    expected_seq_num = 0  # Initialize the expected sequence number

    ack = "ACK"
    nak = "NAK"


    while True:
        print("\n")
        packet = conn.recv(1024).decode()
        seq_num, message, received_checksum = packet.split('|')
        seq_num = int(seq_num)
        received_checksum = int(received_checksum)

        # Calculate the checksum for the received message
        checksum = calculate_checksum(message.encode())
        #print(message)

        i = 0
        while not(checksum == received_checksum):
            if i == 5:
                break

            nak_corrupted = corrupt_message(nak.encode())
            conn.send(nak_corrupted)
            #conn.send(nak.encode())

            packet = conn.recv(1024).decode()
            seq_num, message, received_checksum = packet.split('|')
            seq_num = int(seq_num)
            print(f"received seq_no {seq_num}")
            received_checksum = int(received_checksum)

            # Calculate the checksum for the received message
            checksum = calculate_checksum(message.encode())
            #print(message)


            if(checksum != received_checksum):
                print(f"Packet seq no {seq_num} is corrupted...\t sending NAK")

            i += 1

        if message.lower() == 'exit':
            break

        ack_corrupted = corrupt_message(ack.encode())
        conn.send(ack_corrupted)
        #conn.send(ack.encode())
        if(seq_num != expected_seq_num):
            print(f"expected seq_no {expected_seq_num}...   discarding duplicate packet")
        else:
            print(f"Received and delivered: {message} seq_no{seq_num}\nSending ACK")
            expected_seq_num = 1 - expected_seq_num  # Toggle the expected sequence number


    receiver_socket.close()

if __name__ == "__main__":
    main()

