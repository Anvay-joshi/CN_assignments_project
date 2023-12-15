import socket
import random

WINDOW_SIZE = 4
TOTAL_PACKETS = 20

def send_packet_unreliable(receiver_socket, sender_addr, ack):
    if random.random() <= 0.9:  # 10% probability of loss
        receiver_socket.sendto(str(ack).encode(), sender_addr)
    else:
        print(f"\t packet lost at receiver side")

def main():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(("localhost", 2000))  # Replace with the actual receiver IP and port

    print("Receiver is ready to receive messages...")

    packets_received = [False] * TOTAL_PACKETS
    ack = 0  # Initialize the expected ACK number
    seq_num = 0

    while False in packets_received:
        print("\n")
        message, sender_addr = receiver_socket.recvfrom(1024)
        print(f"Received message: {message.decode().split()[1]}")
        seq_num = int(message.decode().split()[1])

        if packets_received[seq_num] == True:
            print(f"\tPacket {seq_num} is duplicate")
        packets_received[seq_num] = True

        ack = seq_num
        send_packet_unreliable(receiver_socket, sender_addr, ack)
        print(f"sending ACK {ack}")

if __name__ == "__main__":
    main()

