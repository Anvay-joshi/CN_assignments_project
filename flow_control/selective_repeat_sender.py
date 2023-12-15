import socket
import random
import time

WINDOW_SIZE = 4
TOTAL_PACKETS = 20
TIMEOUT = 3

def timer_expired(epoch):
    if (epoch + TIMEOUT <= time.time()):
        return True
    else:
        return False

def shift_window_left(window, buffer):
    for i in range (1, WINDOW_SIZE):
        window[i-1] = window[i]
        buffer[i-1] = buffer[i]

# Function to send a packet unreliably to the receiver
def send_packet_unreliable(sender_socket, receiver_addr, message):
    packet = f"{message}".encode()
    if random.random() <= 0.9:  # 10% probability of corruption
        sender_socket.sendto(packet, receiver_addr)
    else:
        print(f"\t packet lost at sender side")

# Main function for the sender
def main():
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_addr = ('localhost', 2000)  # Replace with actual receiver IP and port

    base_seq_num = 0
    next_seq_num = 4
    buffer = [None] * WINDOW_SIZE
    ack_received = [False] * TOTAL_PACKETS
    packet_sent = [False] * TOTAL_PACKETS
    packet_timer = [None] * TOTAL_PACKETS
    last_ack = -1

    window = [0, 1, 2 ,3]

    while False in ack_received:
        print("\n")
        
        for i in range (0, WINDOW_SIZE):
            if(window[i] < TOTAL_PACKETS and ack_received[window[i]] == False and packet_sent[window[i]] == False):
                message = f"Message {window[i]}"
                buffer[i] = message
                send_packet_unreliable(sender_socket, receiver_addr, message)
                print(f"Sent message {window[i]}")
                packet_sent[window[i]] = True
                packet_timer[window[i]] = time.time()

        try:
            ack, _ = sender_socket.recvfrom(1024)
            seq_num = int(ack.decode())
            ack_received[seq_num] = True
            print(f"Received ACK for message {seq_num}")

            if seq_num == last_ack + 1:
                shift_window_left(window, buffer)
                window[WINDOW_SIZE - 1] = next_seq_num
                buffer[WINDOW_SIZE - 1] = f"Message {next_seq_num}"
                next_seq_num += 1
                base_seq_num += 1
                print(f"advancing base to {base_seq_num}")
                print(f"new window is {window}\n New buffer is {buffer}")
                last_ack = seq_num


        except:
            for i in range (0, WINDOW_SIZE):
                if(packet_timer[window[i]] and timer_expired(packet_timer[window[i]])):
                    packet_sent[window[i]] = False
                    print(f"resending packet {window[i]}")
                    send_packet_unreliable(sender_socket, receiver_addr, buffer[i])



    sender_socket.close()

if __name__ == "__main__":
    main()

