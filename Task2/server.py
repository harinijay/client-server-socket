import socket
import sys
import threading

clients = {}    # to store and manage active clients
topics = {}     # to store subscribers for each topic/subject

def manage_client(client_socket, client_address):   # to handle a specific client
    print(f"New client connected from {client_address}")
    
    clients[client_address] = client_socket
    
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        
        if data == "terminate":
            break
        else:
            print(f"Received from client {client_address}: {data}")
            handle_message(client_address, data)
    
    del clients[client_address]
    
    print(f"Client {client_address} disconnected")
    client_socket.close()

def handle_message(publisher_address, message):     # publish message for interested subscribers
    topic, _, content = message.partition(':')
    
    if topic not in topics:
        return
    
    for subscriber_socket in topics[topic]:
        if subscriber_socket != clients[publisher_address]:
            subscriber_socket.send(content.encode())

def start_server(port):     # start server 
    server_socket = socket.socket()
    server_socket.bind(('localhost', port))
    server_socket.listen()
    
    print(f"Server started and listening on port {port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        
        client_thread = threading.Thread(target=manage_client, args=(client_socket, client_address))
        client_thread.start()       # start threading for each client

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("FORMAT: python server.py PORT")
        sys.exit(1)

    port = int(sys.argv[1])
    start_server(port)
