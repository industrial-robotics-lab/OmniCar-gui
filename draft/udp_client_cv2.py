#!/usr/bin/env python3
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
# server_address = ('127.0.0.1', 9999)
server_address = ('192.168.0.119', 9999)
init_msg = b"Hello"

client_socket.sendto(init_msg, server_address)

while True:
    packet, _ = client_socket.recvfrom(BUFF_SIZE)
    data = base64.b64decode(packet, ' /')
    npdata = np.fromstring(data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1)
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break