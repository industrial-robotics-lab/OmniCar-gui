from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
import time, struct
import socket, numpy as np, cv2

class UdpVideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        udp_server_address = ("192.168.0.119", 10002)
        # udp_server_address = ("127.0.0.1", 10002)
        udp_buff_size = 65536 # max buffer size
        udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        init_msg = b"Init video transmission from server by this message"
        udp_client_socket.sendto(init_msg, udp_server_address)
        while True:
            msg = udp_client_socket.recv(udp_buff_size)
            npdata = np.fromstring(msg, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1) # 1 means return image as is
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            self.changePixmap.emit(convertToQtFormat)


class TcpControlThread(QThread):
    control_vec = [127,127,127]

    def run(self):
        tcp_server_address = ("192.168.0.119", 10001)
        # tcp_server_address = ("127.0.0.1", 10001)
        # tcp_buff_size = 1024
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting control tx TCP client to {tcp_server_address}")
        tcp_client_socket.connect(tcp_server_address)
        while True:
            # msg = bytes(self.control_vec) # input str to bytes
            msg = struct.pack('BBB', self.control_vec[0], self.control_vec[1], self.control_vec[2])
            # print(f"Sending {len(msg)} bytes via TCP")
            tcp_client_socket.send(msg)
            time.sleep(0.01)
            # print(f"Sent {self.control_vec}")
    
    @pyqtSlot(int, int)
    def updateLin(self, x, y):
        # y is UP on touchpad, but Car forward direction is x
        self.control_vec[1] = y
        self.control_vec[2] = 255-x # flip axis
    
    @pyqtSlot(int)
    def updateAng(self, value):
        self.control_vec[0] = 255-value # flip axis


class TcpMapThread(QThread):
    point = pyqtSignal(float, float, float)

    def run(self):
        tcp_server_address = ("192.168.0.119", 10003)
        # tcp_server_address = ("127.0.0.1", 10003)
        tcp_buff_size = 1024
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting map rx TCP client to {tcp_server_address}")
        tcp_client_socket.connect(tcp_server_address)
        while True:
            bytesReceived = tcp_client_socket.recv(tcp_buff_size)
            if len(bytesReceived) == 12:
                struct.unpack('fff', self.point)