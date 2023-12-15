import socket

def calculate_checksum(data):
    #checksum = hashlib.md5(data).hexdigest()
    checksum = 0

    for byte in data:
        checksum ^= byte

    return checksum

def main():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind(("localhost", 2000)) 
    receiver_socket.listen(1)

    print("Receiver is ready to receive messages...")

    conn, addr = receiver_socket.accept()

    while True:
        packet = conn.recv(1024).decode()
        message, received_checksum = packet.split('|')
        received_checksum = int(received_checksum)

        checksum = calculate_checksum(message.encode())
        if checksum == received_checksum:
            conn.send("ACK".encode())
            print(f"Received and delivered: {message}\nsending ACK")
        else:
            conn.send("NAK".encode())
            print("Message corrupted. Requesting sender to resend...")

        if(message.lower() == 'exit'):
            break

    receiver_socket.close()

if __name__ == "__main__":
    main()

