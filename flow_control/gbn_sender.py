import socket
import random

WINDOW_SIZE = 4
TOTAL_PACKETS = 20
TIMEOUT = 3

def corrupt_message(message):
    if random.random() < 0.1:  # 10% probability of corruption
        index = random.randint(0, len(message) - 1)
        message = message[:index] + bytes([message[index] ^ 1]) + message[index + 1:]
    return message

def send_packet_unreliable(sender_socket, receiver_addr, message):
    if random.random() < 0.9:  # 10% probability of corruption
        sender_socket.sendto(message.encode(), receiver_addr)

def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

def main():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_addr = ('localhost', 2000)  # Replace with actual receiver IP and port

    base_seq_num = 0
    next_seq_num = 0
    buffer = [None] * WINDOW_SIZE
    #packets_sent = 0
    last_ack = -1

    while base_seq_num < TOTAL_PACKETS:
        while next_seq_num < base_seq_num + WINDOW_SIZE and next_seq_num < TOTAL_PACKETS:
            message = f"Message {next_seq_num}"
            print(message)
            buffer[next_seq_num % WINDOW_SIZE] = message

            packet = f"{message}".encode()  # Include the sequence number

            send_packet_unreliable(sender_socket, receiver_addr, message)
            #sender_socket.sendto(message.encode(), receiver_addr)

            print(f"Sent message {next_seq_num}")
            next_seq_num += 1
            #packets_sent += 1

        try:
            sender_socket.settimeout(TIMEOUT)
            ack, _ = sender_socket.recvfrom(1024)
            ack = int(ack.decode())
            print(f"Received ACK {ack}")
            print(f"Expected ACK {last_ack + 1}")
            #if base_seq_num <= ack < next_seq_num:
            if ack == last_ack + 1:
                #base_seq_num = ack + 1
                base_seq_num += 1
                print(f"Advancing base to {base_seq_num}")
                last_ack = ack
            else:
                print(f"Ack out of sequence... resending window")
                base_seq_num = last_ack + 1

        except socket.timeout:
            print("Timeout. Resending...")
            next_seq = base_seq_num
            while next_seq < next_seq_num:
                message = buffer[next_seq % WINDOW_SIZE]

                packet = f"{message}".encode()
                #send_packet_unreliable(sender_socket, packet)
               # sender_socket.sendto(message.encode(), receiver_addr)
                send_packet_unreliable(sender_socket, receiver_addr, message)

                print(f"Resent message {next_seq}")
                next_seq += 1


    message = f"Message -1"
    sender_socket.sendto(message.encode(), receiver_addr)

    sender_socket.close()

if __name__ == "__main__":
    main()

