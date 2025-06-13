import socket
import threading

HOST = '127.0.0.1'  # The server's IP address (localhost)
PORT = 50002      # The port used by the server



def sending(socket):
    while True:
        msg = input("You[Client]: ")
        socket.sendall(msg.encode())


# Create a socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))         # Connect to the server
    
    send_thread = threading.Thread(target=sending, args=(s,))
    send_thread.start()

    while True:
        #recieving
        data = s.recv(1024)
        if not data:
                break
        print(f"\nServer: {data.decode()}")


