from sys import *
from helpers import LOCAL_HOST, LOCAL_DNS_SERVER_PORT, BUFFER_SIZE
import re
import socket
import helpers


def connectClientToLocalDnsServer(message):
    originalClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    originalClientMessage = message.encode()
    connectingAddress = ((LOCAL_HOST, LOCAL_DNS_SERVER_PORT))
    originalClientSocket.sendto(originalClientMessage, connectingAddress)
    serverMessage, serverAddress = originalClientSocket.recvfrom(BUFFER_SIZE)
    serverMessage = serverMessage.decode()
    print(f"Talking to the localDnsServer at the Address: {serverAddress}")
    print(f"Message from {serverAddress}:")
    print(f"{serverMessage}")
    result, _ = originalClientSocket.recvfrom(BUFFER_SIZE)
    result = result.decode()
    print(f"Resultant IP Address received from the localDnsServer: {result}")
    originalClientSocket.close()


def isValid(userInput):
    regex = r"([a-z]+\.[a-z]+)+"
    result = re.findall(regex, userInput)
    if len(result) > 0:
        return True
    else:
        return False


while True:
    print()
    print("Please Enter the domain name or \"break\" to exit: ")
    example = "subdomain.domain.com or domain.com"
    print(f"Example : {example}")
    try:
        userInput = input()
        userInput = userInput.lower()
        if userInput == "break":
            print("\n...Exiting Program")
            break
        result = isValid(userInput)
        if result:
            connectClientToLocalDnsServer(userInput)
        else:
            print()
            print(
                f"Please enter a domain name as shown in the example : {example}")
            print()
    except KeyboardInterrupt:
        print("\n...Exiting Program")
        exit()
