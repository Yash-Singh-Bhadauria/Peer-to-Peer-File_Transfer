import socket
import os

server_ip = None
server_socket = None
client_socket = None

def send_file_list(client_socket):
    files = os.listdir()
    file_list = "\n".join(files)
    client_socket.send(file_list.encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12346))
    server_socket.listen(1)

    print("Server is listening...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} established.")

        request = client_socket.recv(1024).decode()
        if request == "LIST":
            send_file_list(client_socket)
        elif request:
            send_file(client_socket, request)
        

def send_file(client_socket, file_name):
    try:
        with open(file_name, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.send(data)
                data = file