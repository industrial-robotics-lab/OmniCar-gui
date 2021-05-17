#!/usr/bin/env python3
from socket import * 

server_address = ("127.0.0.1", 9999)
buff_size = 1024 # 1Kb

with socket(AF_INET, SOCK_STREAM) as client_socket:
    print(f"Connecting to {server_address}")
    client_socket.connect(server_address)
    while True:
        msg = input("Input to send: ").encode() # input str to bytes
        client_socket.sendall(msg)
        print(f"Sent {msg} to {server_address}")

        # Waiting to receive
        data = client_socket.recv(buff_size)
        print(f"Received {data} back from server")