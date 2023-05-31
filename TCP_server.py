from socket import *
import sys
import time

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Read from the socket
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Bind the socket to server address and server port
serverSocket.bind((serverName, serverPort))

# Listen for incoming connections
serverSocket.listen(1)

# Set a timeout value
serverSocket.settimeout(120)

# Keep track of connection IDs
connectionIDs = {}

# function for handling hello messages
def handle_hello_message(message, clientAddress, connectionIDs, connectionSocket):
    # Extract the connectionID from the message
    connectionID = message[1]

    if connectionID not in connectionIDs:
        # Add the connectionID to the dictionary
        connectionIDs[connectionID] = time.time()
        # Send the OK message to the client
        connectionSocket.send(("OK " + connectionID + " " + clientAddress[0] + " " + str(clientAddress[1])).encode())
        return
    else:
        # Send the RESET message to the client
        connectionSocket.send(("RESET " + connectionID).encode())
        return

print("The TCP server is ready to receive")

while True:
    try:
        # Accept incoming connection
        (connectionSocket, clientAddress) = serverSocket.accept()
        message = connectionSocket.recv(2048).decode().split()

        # Delete all connection IDs older than 30 seconds
        for key in list(connectionIDs.keys()):
            if time.time() - connectionIDs[key] > 30:
                del connectionIDs[key]

        # Extract the connectionID from the message
        handle_hello_message(message, clientAddress, connectionIDs, connectionSocket)  

        # Close the connection
        connectionSocket.close()
    except timeout:# If the server times out, clears the connectionID list and closes the socket
        connectionIDs.clear()
        break

# Close the socket
serverSocket.close()
