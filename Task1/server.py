import socket
import sys

def start_server(port):
    server_socket = socket.socket()
    server_socket.bind(('localhost', port))
    server_socket.listen()
    
    print(f"Server started and listening on port {port}")
    
    client_socket, client_address = server_socket.accept()
    print(f"Client connected from {client_address}")
    
    while True:
        data = client_socket.recv(1024).decode()
        if data == "terminate":
            break
        print(f"Received from client: {data}")
    
    print("Client disconnected")
    
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("FORMAT: python server.py PORT")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
