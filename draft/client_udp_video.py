#!/usr/bin/env python3
import cv2, socket, base64, numpy as np

server_address = ("127.0.0.1", 9999)
buff_size = 65536 # max buffer size

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buff_size)
init_msg = b"Init video transmission from server by this message"
client_socket.sendto(init_msg, server_address)
while True:
    msg = client_socket.recv(buff_size)
    data = base64.b64decode(msg, ' /')
    npdata = np.fromstring(data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1) # 1 means return image as is
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break