from socket import *
import sys
from datetime import datetime

# Read from the command line using sys.argv
hi = sys.argv[1]
serverName = sys.argv[2]
serverPort = int(sys.argv[3])
connectionID = sys.argv[4]

#Check if the message is HELLO
while hi != "HELLO":
    hi = input("Message was not approriate, please put HELLO:")

message = hi + " " + connectionID


for i in range(3):
    try:
        # Create a socket
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        
        # Set a timeout
        clientSocket.settimeout(15)
        
        # Send the message to the server
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # Receive the message from the server
        (svrMessage, serverAddress) = clientSocket.recvfrom(2048)
        svrMessage = svrMessage.decode().split()

        # Check if the message is OK or RESET, and print the appropriate message
        if svrMessage[0] == "OK":
            print("Connection established {} {} {} @ {}\n".format(svrMessage[1],svrMessage[2], svrMessage[3], datetime.now()))
            break
        elif svrMessage[0] == "RESET":
            if i == 2: # Check if it is the third time, if so, break the loop
                print("Connection Failure on {}\n".format(datetime.now()))
                break
            else: # If not, print the error message and ask for a new ID
                print("Connection Error {} @ {}\n".format(svrMessage[1], datetime.now()))
                connectionID = input("Please give a new ID:")
                message = hi + " " + connectionID
    except (timeout, ConnectionResetError): # If the server times out or the server hasn't started
        if i == 2:
            print("Connection Failure on {}\n".format(datetime.now()))
            break
        #Retry if the server times out
        print("Connection Error {} @ {}\n".format(connectionID, datetime.now()))
        connectionID = input("Please give a new ID:")
        message = hi + " " + connectionID

# Close the socket
clientSocket.close()
    

