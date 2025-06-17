import socket
import threading
import sys
import os

HOST = '127.0.0.1'  # Localhost (only accessible from your computer)
PORT = int(os.environ.get("PORT"))

client_count = 0
client_count_lock = threading.Lock()
#stop 2 threads from accesing the same value at the same time

connections = {}
shutdown_event = threading.Event()



def handle_client(conn, addr):
    global client_count

    with client_count_lock:
        client_count += 1
        # Save updated client count to shell export file
        with open("client_env.sh", "w") as f:
            f.write(f"export CLIENT_NUM={client_count}\n")
        print(f"New client connected: {addr} — Total: {client_count}")
    
    connections[conn] = addr 

    thread_O = threading.Thread(target=Server_recieve, args=(conn, addr))
    thread_O.start()
    

def Server_write():
    while not shutdown_event.is_set():
        msg = input("You [Server]: ")
        for conn, addr in connections.items():
            conn.sendall(msg.encode())

def Server_recieve(conn, addr):
    while not shutdown_event.is_set():

            data = conn.recv(1024)
            if data:
                print(f"\nClient [{addr}]: {data.decode()}")


conn = None
addr = None


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as linking_socket:
        linking_socket.bind((HOST, PORT))    # Bind to host and port
        linking_socket.listen()              # Start listening for connections
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = linking_socket.accept()
        thread_I = threading.Thread(target=Server_write)
        thread_I.start()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        connections[conn] = addr


        while not shutdown_event.is_set():
            #add to a dict the new connection
            conn, addr = linking_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

except KeyboardInterrupt:
    print("\n🔌 Server interrupted with Ctrl+C. Shutting down gracefully.")
    shutdown_event.set()
    try:
        for conn_s in connections.items():
            conn_s.close()
    except:
        pass
    sys.exit(0)