import socket
import dns
import dns.resolver
import dns.query
import dns.name
import dns.message
import warnings
from helpers import LOCAL_HOST, ROOT_SERVER_PORT, BUFFER_SIZE
from helpers import splitInput
from helpers import getInput
from helpers import customPrint
from helpers import displayMessages


def findOutTld(userInput, localNameServer):
    returnMessage = []
    defaultResolver = dns.resolver.get_default_resolver()
    converToDomainName = dns.name.from_text(userInput)
    numberOfWords = 1
    rootInput = getInput(userInput, numberOfWords)
    customPrint("Customized rootInput", rootInput)
    message = f"I dont know the address of \"{userInput}\" but I know the address of \"{rootInput}\""
    returnMessage.append(message)
    returnMessage.append(
        f"Looking up \"{rootInput}\" on \"{localNameServer}\"")
    query = dns.message.make_query(rootInput, dns.rdatatype.NS)
    response = dns.query.udp(query, localNameServer)
    responseCode = response.rcode()
    if responseCode != dns.rcode.NOERROR:
        if responseCode == dns.rcode.NXDOMAIN:
            returnMessage.append(f"\"{rootInput}\" does not exist.")
            returnMessage.append("Please enter a legible domain")
            return returnMessage
        else:
            returnMessage.append("Please enter a legible domain.")
            return returnMessage
    resourceRecordSet = None
    if len(response.authority) > 0:
        resourceRecordSet = response.authority[0]
    else:
        resourceRecordSet = response.answer[0]
    resourceRecord = resourceRecordSet[0]
    if resourceRecord.rdtype == dns.rdatatype.SOA:
        returnMessage.append(
            f"Same server is TLD Server for \"{rootInput}\"")
    else:
        tldServerName = resourceRecord.target
        returnMessage.append(
            f"\"{tldServerName}\" is TLD Server for \"{rootInput}\"")
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        ipAddressofTld = defaultResolver.query(
            tldServerName).rrset[0].to_text()
        returnMessage.append(
            f"IP Address of \"{tldServerName}\" is \"{ipAddressofTld}\"")
        returnMessage.append(str(tldServerName))
        returnMessage.append(ipAddressofTld)
    return returnMessage


def rootDnsServer():
    rootDnsServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        rootDnsServerSocket.bind((LOCAL_HOST, ROOT_SERVER_PORT))
        print(f"Root Server is up and running at port:{ROOT_SERVER_PORT}")
        while True:
            localNameServer, _ = rootDnsServerSocket.recvfrom(BUFFER_SIZE)
            localNameServer = localNameServer.decode()
            clientMessage, clientAddress = rootDnsServerSocket.recvfrom(
                BUFFER_SIZE)
            userInput = clientMessage.decode()
            print(f"Talking to Client at Address:{clientAddress}")
            print(f"Client Message:{userInput}")
            result = findOutTld(userInput, localNameServer)
            displayMessages(result)
            serverMessage = str(result).encode()
            rootDnsServerSocket.sendto(serverMessage, clientAddress)
    except KeyboardInterrupt:
        print("\nStopping the server")
        print("........")
        print("........")
        print("You Stopped the server")
        exit()
    except:
        print("Something went wrong")
        exit()


rootDnsServer()
