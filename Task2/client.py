import socket
import sys
import threading

def handle_received_data(client_socket):    # print data sent by the server
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print(data)

def start_client(server_ip, port, category, topic):    # start the client
    client_socket = socket.socket()
    client_socket.connect((server_ip, port))
    
    print(f"Connected to server {server_ip} on {port}")

    client_socket.send(f"{category}:{topic}".encode())
    
    if category == "SUBSCRIBER":        # filter subscribers from the clients
        receive_thread = threading.Thread(target=handle_received_data, args=(client_socket,))
        receive_thread.start()
    
    while True:
        message = input("Enter a message (type 'terminate' to exit): ")
        client_socket.send(f"{topic}:{message}".encode())
        if message == "terminate":
            break
    
    print("Disconnected from server")
    
    client_socket.close()

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("FORMAT: python client.py SERVER_IP PORT CATEGORY TOPIC")
        sys.exit(1)

    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    category = sys.argv[3]
    topic = sys.argv[4]
    start_client(server_ip, port, category, topic)
