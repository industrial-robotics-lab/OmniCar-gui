#!/usr/bin/env python3
from socket import * 

server_address = ("127.0.0.1", 9999)
buff_size = 1024 # 1Kb

with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"Listening at {server_address}")
    client_socket, client_address = server_socket.accept()
    while True:
        data = client_socket.recv(buff_size)
        if len(data) > 0:
            print(f"Received {data} from {client_address}")
            client_socket.sendall(data)
            print(f"Sent {data} back to {client_address}")