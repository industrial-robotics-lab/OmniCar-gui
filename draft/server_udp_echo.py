#!/usr/bin/env python3
from socket import * 

sock = socket(AF_INET, SOCK_DGRAM)
server_address = ('localhost', 10000)
print(f"starting up on {server_address[0]} port {server_address[1]}")
sock.bind(server_address)

while True:
    print("\nwaiting to receive message")
    data, address = sock.recvfrom(4096)

    print(f"received {len(data)} bytes from {address}")
    print(data)

    if data:
        send = sock.sendto(data, address)
        print(f"send {send} bytes back to {address}")