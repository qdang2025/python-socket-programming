from socket import *
import sys
import time

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Read from the socket
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Bind the socket to server address and server port
serverSocket.bind((serverName, serverPort))

# Set a timeout value
serverSocket.settimeout(120)

# Keep track of connection IDs
connectionIDs = {}

#function for handling hello messages
def handle_hello_message(message, clientAddress, connectionIDs, serverSocket):
    connectionID = message[1]
    if connectionID not in connectionIDs:
        connectionIDs[connectionID] = time.time()
        serverSocket.sendto(("OK " + connectionID + " " + clientAddress[0] + " " + str(clientAddress[1])).encode(), clientAddress)
        return
    else:
        serverSocket.sendto(("RESET " + connectionID).encode(), clientAddress)
        return

print("The UDP server is ready to receive")

while True:
    try:
        (message, clientAddress) = serverSocket.recvfrom(2048)
        message = message.decode().split()
        # Delete all connection IDs older than 30 seconds
        for key in list(connectionIDs.keys()):
            if time.time() - connectionIDs[key] > 30:
                del connectionIDs[key]
        # Extract the connectionID from the message
        handle_hello_message(message, clientAddress, connectionIDs, serverSocket)
    except timeout:
        # If there is a timeout, clear the dictionary and break
        connectionIDs.clear()
        break

serverSocket.close()

