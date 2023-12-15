import socket

def calculate_checksum(data):
    checksum = 0

    for byte in data:
        checksum ^= byte

    return checksum

def main():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Use SOCK_DGRAM for UDP
    receiver_socket.bind(("localhost", 2000))

    print("Receiver is ready to receive messages...")

    while True:
        print("\n")
        packet, sender_addr = receiver_socket.recvfrom(1024)  # Receive packet as UDP datagram
        packet = packet.decode()

        message, received_checksum = packet.split('|')
        received_checksum = int(received_checksum)

        checksum = calculate_checksum(message.encode())

        if checksum == received_checksum:
            receiver_socket.sendto(b"ACK", sender_addr)  # Send ACK back to the sender
            print(f"Received and delivered: {message}\nsending ACK")
        else:
            receiver_socket.sendto(b"NAK", sender_addr)  # Send NAK if the message is corrupted
            print("Message corrupted. Requesting sender to resend...")

        if message.lower() == 'exit':
            break

    receiver_socket.close()

if __name__ == "__main__":
    main()

