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
    hi = input("Keyword was not approriate, please put HELLO:")


message = hi + " " + connectionID


# Read the message from the server
for i in range(3):
    try:
        # Create a socket
        clientSocket = socket(AF_INET, SOCK_STREAM)
       
        # Set a timeout
        clientSocket.settimeout(15)
       
        # Connect to the server
        clientSocket.connect((serverName, serverPort))
       
        # Send the message to the server
        clientSocket.send(message.encode())
        
        # Receive the message from the server
        svrMessage = clientSocket.recv(2048).decode().split()
        
        # Check if the message is OK or RESET, and print the appropriate message
        if svrMessage[0] == "OK":
            print("Connection established {} {} {} @ {}\n".format(svrMessage[1],svrMessage[2], svrMessage[3], datetime.now()))
            break
        elif svrMessage[0] == "RESET":
            # Check if it is the third time, if so, break the loop
            if i == 2:
                print("Connection Failure on {}\n".format(datetime.now()))
                break
            else:
                # If not, print the error message and ask for a new ID
                print("Connection Error {} @ {}\n".format(svrMessage[1], datetime.now()))
                connectionID = input("Please give a new ID:")
                message = hi + " " + connectionID        
    
    except (timeout, ConnectionRefusedError): # If the server times out, exit immediately
        print("Connection Failure on {}\n".format(datetime.now()))
        break

# Close the socket
clientSocket.close()