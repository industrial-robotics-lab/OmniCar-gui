import socket, cv2, pickle, struct

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.connect(("google.com", 80))
# host_ip = server_socket.getsockname()[0]
# print(f"Host ip: {host_ip}")
port = 9999
socket_address = ("192.168.0.119", port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print(f"Listening at: {socket_address}")

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print(f"Got connection from: {addr}")
    if client_socket:
        vid = cv2.VideoCapture(0)
        while(vid.isOpened()):
            ret, frame = vid.read()
            frame = cv2.resize(frame, (int(frame.shape[1]*0.5), int(frame.shape[0]*0.5)))
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow("Transmitting video", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
