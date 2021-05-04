#!/usr/bin/env python3
import cv2, imutils, socket, base64

server_address = ("127.0.0.1", 9999)
# buff_size = 65536 # max buffer size

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buff_size)
rcv_buf = server_socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF)
snd_buf = server_socket.getsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF)
print(f"Receive buf = {rcv_buf}; Send buf = {snd_buf}")
print(f"Binding to {server_address}")
server_socket.bind(server_address)
vid = cv2.VideoCapture(0)
while True:
    init_msg, client_address = server_socket.recvfrom(1024) # receive init message
    print(f"Received init msg from {client_address}, starting video transmission...")
    WIDTH=400
    while vid.isOpened():
        _, frame = vid.read()
        # frame = imutils.resize(frame, width=WIDTH) # if you want to reduce frame size
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80]) # compress image
        # _, buffer = cv2.imencode('.jpg', frame) # compress image
        # msg = base64.b64encode(buffer)
        msg = buffer
        print(f"Msg len =  {len(msg)}")
        print(f"Encoding: frame({frame.shape[0]*frame.shape[1]*frame.shape[2]}) -> encoded({len(buffer)}) -> base64({len(msg)})")
        server_socket.sendto(msg, client_address)
        cv2.imshow("TRANSMITTING VIDEO", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break