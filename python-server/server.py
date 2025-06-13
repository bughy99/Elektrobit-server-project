import socket
import threading
import sys

HOST = '127.0.0.1'  # Localhost (only accessible from your computer)
PORT = 50002        # Port to listen on (choose >1023)



def recieving(conn):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"\nClient: {data.decode()}")
        except:
            break


conn = None

# Create a TCP/IP socket
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))    # Bind to host and port
        s.listen()              # Start listening for connections
        print(f"Server listening on {HOST}:{PORT}")

        conn, addr = s.accept()  # Accept an incoming connection
        with conn:
            print(f"Connected by {addr}")


            recv_tread = threading.Thread(target=recieving, args=(conn,))
            #recieving part
            recv_tread.start()


            while True:
                
                msg = input("You[Server]: ")
                conn.sendall(msg.encode()) 

except KeyboardInterrupt:
    print("\n🔌 Server interrupted with Ctrl+C. Shutting down gracefully.")
    try:
        conn.close()
    except:
        pass
    sys.exit(0)