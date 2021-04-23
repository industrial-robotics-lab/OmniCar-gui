#!/usr/bin/env python3
# Receive car control + Transmit video
import cv2, imutils, socket, base64
from threading import Thread

tcp_server_address = ("127.0.0.1", 10001)
udp_server_address = ("127.0.0.1", 10002)
tcp_buff_size = 1024
udp_buff_size = 65536 # max buffer size
control_vec = [0,0,0]

tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, udp_buff_size)

def rx_tcp():
    global control_vec
    print(f"Binding TCP server to {tcp_server_address}")
    tcp_server_socket.bind(tcp_server_address)
    tcp_server_socket.listen(1)
    client_socket, client_address = tcp_server_socket.accept()
    while True:
        data = client_socket.recv(tcp_buff_size)
        if len(data) == 3:
            control_vec = list(data)
            # print(f"Received {control_vec} from {client_address}")

def tx_udp():
    global control_vec
    print(f"Binding UDP server to {udp_server_address}")
    udp_server_socket.bind(udp_server_address)
    vid = cv2.VideoCapture(0)
    while True:
        init_msg, client_address = udp_server_socket.recvfrom(udp_buff_size) # receive init message
        print(f"Received init msg from {client_address}, starting video transmission...")
        WIDTH=400
        while vid.isOpened():
            _, frame = vid.read()
            frame = imutils.resize(frame, width=WIDTH) # if you want to reduce frame size
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80]) # compress image
            msg = base64.b64encode(buffer)
            # print(f"Encoding: frame({frame.shape[0]*frame.shape[1]*frame.shape[2]}) -> encoded({len(buffer)}) -> base64({len(msg)})")
            udp_server_socket.sendto(msg, client_address)
            cv2.putText(frame, str(control_vec), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("TRANSMITTING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                udp_server_socket.close()
                break

# ----------------------- main loop -------------------------
tcp_thread = Thread(target=rx_tcp)
udp_thread = Thread(target=tx_udp)

tcp_thread.start()
udp_thread.start()

tcp_thread.join()
udp_thread.join()