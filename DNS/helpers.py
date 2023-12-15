import socket

LOCAL_HOST = "localhost"
LOCAL_DNS_SERVER_PORT = 8053
ROOT_SERVER_PORT = 9001
TLD_SERVER_PORT = 9002
AUTHORITATIVE_SERVER_PORT = 9003
BUFFER_SIZE = 65535
# Note:
# We could add the buffer size variable, one for sending and one for receiving,
# I have only used one to keep it simple. And its size is based on the max size
# of the receiving buffer.


def customPrint(name, value):
    print()
    print(name + ":")
    print(value)
    print(type(value))
    print()


def getInputForNextServer(listOfMessages):
    cleanList = []
    for message in listOfMessages:
        message = message.strip()
        message = message.replace("'", "")
        cleanList.append(message)
    ipAddressOfTld = str
    cleanList.reverse()
    ipAddressOfTld = cleanList[0]
    return ipAddressOfTld


def displayMessages(listOfMessages):
    for message in listOfMessages:
        message = message.strip()
        message = message.replace("'", "")
        print(message)
    print()


def actAsTemporaryClient(message, connectingPort, nameServer):
    tempClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    queryMessage = message.encode()
    nameServer = nameServer.encode()
    connectingAddress = (LOCAL_HOST, connectingPort)
    tempClientSocket.sendto(nameServer, connectingAddress)
    tempClientSocket.sendto(queryMessage, connectingAddress)
    serverMessage, serverAddress = tempClientSocket.recvfrom(BUFFER_SIZE)
    serverMessage = serverMessage.decode()
    print()
    print(f"Message from {serverAddress}:")
    listOfMessages = serverMessage.strip('[]').split(',')
    tempClientSocket.close()
    return listOfMessages


def getInput(givenInput, numberOfWords):
    result = splitInput(givenInput)
    result.reverse()
    returningString = ""
    for i in range(numberOfWords):
        returningString = result[i] + "." + returningString
    return returningString


def splitInput(userInput):
    splitDomainName = userInput.split('.')
    return splitDomainName
