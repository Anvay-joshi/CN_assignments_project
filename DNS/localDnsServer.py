import socket
import dns
import dns.resolver
from helpers import LOCAL_HOST, LOCAL_DNS_SERVER_PORT, BUFFER_SIZE
from helpers import ROOT_SERVER_PORT
from helpers import TLD_SERVER_PORT
from helpers import AUTHORITATIVE_SERVER_PORT
from helpers import splitInput
from helpers import actAsTemporaryClient
from helpers import displayMessages
from helpers import getInputForNextServer
from helpers import customPrint
from helpers import getInput

cache = {}


def fetchFromCache(searchKey):
    ipAddress = cache.get(searchKey)
    print(f"\"{searchKey}\" found in cache")
    print(f"IP Address of \"{searchKey}\" is \"{ipAddress}\"")
    return ipAddress


def generalServerHandler(userInput, nameServer, connectedPort, message):
    result = actAsTemporaryClient(userInput, connectedPort, nameServer)
    print(message + ":")
    displayMessages(result)
    ipAddress = getInputForNextServer(result)
    print("Returned IP Address :", ipAddress)
    return ipAddress


def localDnsServer():
    localDnsServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # try:
    localDnsServerSocket.bind((LOCAL_HOST, LOCAL_DNS_SERVER_PORT))
    #localDnsServerSocket.bind(("localhost", 2000))
    print(
        f"localDNS is up and running and I am listening at Port:{LOCAL_DNS_SERVER_PORT}")
    while True:
        clientMessage, clientAddress = localDnsServerSocket.recvfrom(
            BUFFER_SIZE)
        userInput = clientMessage.decode()
        print(f"Talking to the Client at the Address:{clientAddress}")
        print(f"Client Message:{userInput}")
        message = f"Hang in there client, I will get the IP Address of the \"{userInput}\""
        message = message.encode()
        localDnsServerSocket.sendto(message, clientAddress)
        defaultResolver = dns.resolver.get_default_resolver()
        rootNameServer = defaultResolver.nameservers[0]
        splitResult = splitInput(userInput)
        splitResult.reverse()
        rootInput, tldInput, *_ = splitResult
        tldInput = tldInput + "." + rootInput
        authoritativeInput = getInput(userInput, len(splitResult))
        authoritativeInput = authoritativeInput[:-1]
        customPrint("rootInput", rootInput)
        customPrint("tldInput", tldInput)
        customPrint("_", _)
        customPrint("authoritativeInput", authoritativeInput)
        if bool(cache) and rootInput in cache:
            tldNameServer = fetchFromCache(rootInput)
        else:
            rootMessage = "Root Result"
            tldNameServer = generalServerHandler(
                userInput, rootNameServer, ROOT_SERVER_PORT, rootMessage)
        cache[rootInput] = tldNameServer
        tldMessage = "TLD Result"
        authoritativeServer = generalServerHandler(
            userInput, tldNameServer, TLD_SERVER_PORT, tldMessage)
        cache[tldInput] = authoritativeServer
        authoritativeMessage = "Authoritative Result"
        finalIpAddress = generalServerHandler(
            userInput, authoritativeServer, AUTHORITATIVE_SERVER_PORT, authoritativeMessage)
        cache[authoritativeInput] = finalIpAddress
        customPrint("cache", cache)
        print()
        print(f"Final IP Address : {finalIpAddress}")
        print()
        serverMessage = finalIpAddress.encode()
        localDnsServerSocket.sendto(serverMessage, clientAddress)
    # except KeyboardInterrupt:
    #     print("\nStopping the server")
    #     print("........")
    #     print("........")
    #     print("You Stopped the server")
    #     exit()
    # except:
    #     print("Something went wrong")
    #     exit()


localDnsServer()
