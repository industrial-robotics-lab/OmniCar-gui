#!/usr/bin/env python3
from socket import * 

server_address = ("127.0.0.1", 9999)
buff_size = 1024 # 1Kb

with socket(AF_INET, SOCK_DGRAM) as client_socket:
    while True:
        msg = input("Input to send: ").encode() # input str to bytes
        msg_len = client_socket.sendto(msg, server_address)
        print(f"Sent {msg} to {server_address}")

        # Waiting to receive
        data = client_socket.recv(buff_size)
        print(f"Received {data} back from server")