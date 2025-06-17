import socket
import threading
import os
import sys

HOST = '127.0.0.1'  # The server's IP address (localhost)
PORT = int(os.environ.get("PORT"))

shutdown_event = threading.Event()

def sending(socket):
    while not shutdown_event.is_set():
        msg = input("You[Client]: ")
        socket.sendall(msg.encode())

try:
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))         # Connect to the server
        

        send_thread = threading.Thread(target=sending, args=(s,))
        send_thread.start()

        while not shutdown_event.is_set():
            #recieving
            data = s.recv(1024)
            if not data:
                    break
            print(f"\nServer: {data.decode()}")

except KeyboardInterrupt:
    print("\n🔌 Client interrupted with Ctrl+C. Shutting down gracefully.")
    shutdown_event.set()
    try:
            s.close()
    except:
        pass
    sys.exit(0)
