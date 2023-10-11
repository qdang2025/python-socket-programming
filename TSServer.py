import socket
import time
import threading

PORT = 16828 # 10000 + 6828 Quang's student ID
BACKLOG = 5

def handle_client(client_socket):
	try: 
		data = client_socket.recv(2048).decode()
	except: # if data is empty or client disconnected
		print("[*] Error getting client time.")

	t2 = time.time() #Time of receving

	#time.sleep(5) #For multithreading demonstration purposes
    #Graders, you can modify this sleep time to see the effect of multithreading

	t3 = time.time() #Time of sending

	try:
		client_socket.send(f"{t2} {t3}".encode())
	except:
		print("[*] Error sending data back to client.")
		
	client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', PORT))
    server.listen(BACKLOG) 
    print(f"[*] Listening on port {PORT}")

    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()
