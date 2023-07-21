import socket
import sys
import threading

clients = {}    # to store and manage active clients

def manage_client(client_socket, client_address):   # to handle a specific client

    print(f"New client connected from {client_address}")
    
    data = client_socket.recv(1024).decode()
    category, _, topic = data.partition(':')
    
    clients[client_address] = {'socket':client_socket,'type':category,'topic':topic}
    
    while True:
        data = client_socket.recv(1024).decode()
        topic, _, message = data.partition(':')  # we need to partition here again it comes like "Topic:Message"

        if not message:
            break
        
        if message == "terminate":
            break
        else:
            print(f"Received from client {client_address}: {data}")
            handle_message(client_socket,data)
    
    del clients[client_address]
    
    print(f"Client {client_address} disconnected")
    client_socket.close()

def handle_message(sender_socket,content):     # publish message for interested subscribers
    topic, _, message = content.partition(':')
    
    for subscriber_socket in clients:
        if clients[subscriber_socket]['type'] == 'SUBSCRIBER' and clients[subscriber_socket]['topic'] == topic and clients[subscriber_socket]['socket'] != sender_socket:   # even for a subscriber, the message is not sent to the sender
            clients[subscriber_socket]['socket'].send(message.encode())

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
