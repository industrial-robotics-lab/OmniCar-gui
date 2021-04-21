#!/usr/bin/env python3
from socket import * 

server_address = ("127.0.0.1", 9999)
buff_size = 1024 # 1Kb

with socket(AF_INET, SOCK_DGRAM) as server_socket:
    print(f"Binding to {server_address}")
    server_socket.bind(server_address)
    while True:
        data, client_address = server_socket.recvfrom(buff_size)
        print(f"Received {data} from {client_address}")
        if len(data) > 0:
            msg_len = server_socket.sendto(data, client_address)
            print(f"Sent {data} back to {client_address}")