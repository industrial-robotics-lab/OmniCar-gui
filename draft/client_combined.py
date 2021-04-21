#!/usr/bin/env python3
import cv2, socket, base64, numpy as np
from threading import Thread

tcp_server_address = ("127.0.0.1", 10001)
udp_server_address = ("127.0.0.1", 10002)
tcp_buff_size = 1024
udp_buff_size = 65536 # max buffer size

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, udp_buff_size)

def rx_tcp():
    print(f"Connecting TCP client to {tcp_server_address}")
    tcp_client_socket.connect(tcp_server_address)
    while True:
        msg = input("Input to send: ").encode() # input str to bytes
        tcp_client_socket.sendall(msg)
        print(f"Sent {msg} to {tcp_server_address}")

        # Waiting to receive
        data = tcp_client_socket.recv(tcp_buff_size)
        print(f"Received {data} back from TCP server")

def rx_udp():
    init_msg = b"Init video transmission from server by this message"
    udp_client_socket.sendto(init_msg, udp_server_address)
    while True:
        msg = udp_client_socket.recv(udp_buff_size)
        data = base64.b64decode(msg, ' /')
        npdata = np.fromstring(data, dtype=np.uint8)
        frame = cv2.imdecode(npdata, 1) # 1 means return image as is
        cv2.imshow("RECEIVING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            udp_client_socket.close()
            break

# ----------------------- main loop -------------------------
tcp_thread = Thread(target=rx_tcp)
udp_thread = Thread(target=rx_udp)

tcp_thread.start()
udp_thread.start()

tcp_thread.join()
udp_thread.join()