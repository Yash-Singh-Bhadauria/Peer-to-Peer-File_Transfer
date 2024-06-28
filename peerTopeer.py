import socket
import os

def send_file_list(sock):
    files = os.listdir()
    file_list = "\n".join(files)
    sock.send(file_list.encode())

def get_file_list(sock):
    file_list = sock.recv(1024).decode()
    print("HERE IS THE LIST OF THE FILES YOU CAN REQUEST :")
    print(file_list)



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12346))
    server_socket.listen(1)

    print("WAITING FOR THE RECEIVER...")

    client_socket, client_address = server_socket.accept()
    print(f"CONNECTION FROM {client_address} ESTABLISHED.")   

    send_file_list(client_socket)
    get_file_list(client_socket)

    wht = client_socket.recv(1024).decode("utf-8") 
    while True: 
        if(wht == "1"):
            file_name = client_socket.recv(1024).decode()
            with open(file_name, "rb") as f:
                file_data = f.read()
            client_socket.send(file_data)
            print(f"FILE {file_name} SENT SUCCESSFULLY.")
            wht = client_socket.recv(1024).decode("utf-8")
            # break
        elif (wht == "0"):
            c = input("DO YOU WANT TO REQUEST A FILE : ") 
            client_socket.send(c.encode("utf-8"))
            if(c == "1"):
                file_name = input("ENTER THE FILE NAME YOU WANT TO RECEIVE : ")
                client_socket.send(file_name.encode())
                file_data = client_socket.recv(1024)
                with open(file_name, "wb") as f:
                    f.write(file_data)
                print(f"FILE {file_name} RECEIVED SUCCESSFULLY.")
            else:
                wht = client_socket.recv(1024).decode("utf-8")
        else:
            print("NO FURTHER REQUESTS FROM THE RECIEVER SIDE. HENCE SHUTTING DOWN THE CONNECTION..")
            server_socket.close()
            break

def start_client():
    server_ip = input("ENTER THE SENDERS IP ADDRESS : ")  # Get the server IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 12346))  # Connect using the server IP

    get_file_list(client_socket)
    send_file_list(client_socket)
    
    wht  =  input("DO YOU WANT TO REQUEST A FILE : ") 
    client_socket.send(wht.encode("utf-8"))
    while True:    
        if(wht == "1"):
            file_name = input("ENTER THE FILE NAME YOU WANT TO RECEIVE : ")
            client_socket.send(file_name.encode())
            file_data = client_socket.recv(1024)
            with open(file_name, "wb") as f:
                f.write(file_data)
            print(f"FILE {file_name} RECEIVED SUCCESSFULLY.")
            wht  =  input("DO YOU WANT TO REQUEST A FILE : ") 
            client_socket.send(wht.encode("utf-8"))
        elif(wht == "0"):
            c = client_socket.recv(1024).decode("utf-8")
            if(c == "1"):
                file_name = client_socket.recv(1024).decode()
                with open(file_name, "rb") as f:
                    file_data = f.read()
                client_socket.send(file_data)
                print(f"FILE {file_name} SENT SUCCESSFULLY.")
                # break
            else:
                wht  =  input("DO YOU WANT TO REQUEST A FILE : ") 
                client_socket.send(wht.encode())
        else:
            print("NO FURTHER REQUESTS... TERMINATING THE CONNECTION")
            client_socket.send("2".encode("utf-8"))
            client_socket.close()
            break

if __name__ == "__main__":
    print("HERE IS THE MENU YOU CAN EXECUTE ::\nNO FILE REQUEST CODE :- 0\nFILE REQUEST CODE :- 1\nEXIT CODE :- 2")
    c1 = int(input("ARE YOU TRYING TO SEND A FILE OR RECEIVE A FILE.\nENTER 0 FOR SENDING AND 1 FOR RECEIVING : "))
    if c1 == 0:
        start_server()
    else:
        start_client()