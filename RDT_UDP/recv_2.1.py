import socket
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
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(("localhost", 2000))

    print("Receiver is ready to receive messages...")

    expected_seq_num = 0

    ack = "ACK"
    nak = "NAK"

    while True:
        print("\n")
        packet, sender_addr = receiver_socket.recvfrom(1024)
        packet = packet.decode()
        seq_num, message, received_checksum = packet.split('|')
        seq_num = int(seq_num)
        received_checksum = int(received_checksum)

        checksum = calculate_checksum(message.encode())

        i = 0
        while not (checksum == received_checksum):
            if i == 5:
                break

            nak_corrupted = corrupt_message(nak.encode())
            receiver_socket.sendto(nak_corrupted, sender_addr)

            packet, sender_addr = receiver_socket.recvfrom(1024)
            packet = packet.decode()
            seq_num, message, received_checksum = packet.split('|')
            seq_num = int(seq_num)
            received_checksum = int(received_checksum)

            checksum = calculate_checksum(message.encode())

            if checksum != received_checksum:
                print(f"Packet seq no {seq_num} is corrupted...\t sending NAK")

            i += 1

        ack_corrupted = corrupt_message(ack.encode())
        receiver_socket.sendto(ack_corrupted, sender_addr)

        if seq_num != expected_seq_num:
            print(f"expected seq_no {expected_seq_num}...   discarding duplicate packet")
        else:
            print(f"Received and delivered: {message} seq_no{seq_num}\nSending ACK")
            expected_seq_num = 1 - expected_seq_num

        if message.lower() == 'exit':
            break

    receiver_socket.close()

if __name__ == "__main__":
    main()

