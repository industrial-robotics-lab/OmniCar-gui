#!/usr/bin/env python3
import cv2, imutils, socket
import numpy as np
import time
import base64

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
# socket_address = ('127.0.0.1', 9999)
socket_address = ('192.168.0.119', 9999)
server_socket.bind(socket_address)
print(f"Listening at: {socket_address}")

vid = cv2.VideoCapture(0)

while True:
    msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
    print(f"GOT connection from {client_addr}")
    WIDTH=400
    while vid.isOpened():
        _, frame = vid.read()
        frame = imutils.resize(frame, width=WIDTH)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = base64.b64encode(buffer)
        print(f"Encoding: frame({frame.shape[0]*frame.shape[1]*frame.shape[2]}) -> encoded({len(buffer)}) -> base64({len(message)})")
        server_socket.sendto(message, client_addr)
        cv2.imshow("TRANSMITTING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break