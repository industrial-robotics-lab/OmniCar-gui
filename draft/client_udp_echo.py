#!/usr/bin/env python3
from socket import * 

sock = socket(AF_INET, SOCK_DGRAM)

server_address = ('localhost', 10000)
message = b"This is our message. It will be sent all at once"

try:
    print('sending {!r}'.format(message))
    sent = sock.sendto(message, server_address)

    print("Waiting to receive")
    data, server = sock.recvfrom(4096)
    print('received {!r}'.format(data))

finally:
    print("closing socket")
    sock.close()