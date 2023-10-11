import socket
import time
import sys

# If a server address is provided, use it. Otherwise, default to 'localhost'.
if len(sys.argv) > 1:
    SERVER = sys.argv[1]
else:
    SERVER = 'localhost'

PORT = 16828  # 10000 + 6828 Quang's student ID


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER, PORT))
    except:
        print("[*] Error connecting to Server.")

    t1 = time.time()  # time of sending
    try:
        client.send(str(t1).encode())
    except:
        print("[*] Error sending data to server.")

    try:
        data = client.recv(2048).decode().split()
    except:
        print("[*] Error getting T2 and T3 from Server.")

    t4 = time.time() # Time of receiving
    t2, t3 = float(data[0]), float(data[1])

    RTT = t4 - t1 - int(t3 - t2)  # Request delay + Response delay
    OFFSET = (t2 - t1 + t3 - t4) / 2 # Clock offset assuming symmetrical delay

    #We will use the time when the client receives the response from the server (t4)
    REMOTE_TIME = t4 + OFFSET 
    LOCAL_TIME = t4

    print(f"REMOTE_TIME {int(REMOTE_TIME*1000)}")
    print(f"LOCAL_TIME {int(LOCAL_TIME*1000)}")
    print(f"RTT_ESTIMATE {int(RTT*1000)}")

    client.close()


if __name__ == "__main__":
    main()
