from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage
import time, struct
import socket, numpy as np, cv2


class TcpControlThread(QThread):
    control_vec = [127,127,127]

    def __init__(self, parent, address):
        QThread.__init__(self, parent)
        self.address = address

    def run(self):
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting control tx TCP client to {self.address}")
        tcp_client_socket.connect(self.address)
        prev_control_vec = [0,0,0]
        while True:
            if self.control_vec != prev_control_vec: # check if these values already were sent
                msg = struct.pack('BBB', self.control_vec[0], self.control_vec[1], self.control_vec[2])
                tcp_client_socket.send(msg)
                # print(f"Sent {*self.control_vec,}")
                prev_control_vec = self.control_vec.copy()
            time.sleep(0.05)
    
    @pyqtSlot(int, int)
    def updateLin(self, x, y):
        # y is UP on touchpad, but Car forward direction is x
        self.control_vec[1] = y
        self.control_vec[2] = x if x==127 else 255-x # flip axis
    
    @pyqtSlot(int)
    def updateAng(self, value):
        self.control_vec[0] = value if value==127 else 255-value # flip axis


class UdpVideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, parent, address):
        QThread.__init__(self, parent)
        self.address = address

    def run(self):
        udp_buff_size = 65536 # max buffer size
        udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        init_msg = b"Init video transmission from server by this message"
        udp_client_socket.sendto(init_msg, self.address)
        print(f"Receiving UDP video from {self.address}")
        while True:
            msg = udp_client_socket.recv(udp_buff_size)
            npdata = np.fromstring(msg, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1) # 1 means return image as is
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            self.changePixmap.emit(convertToQtFormat)


class TcpMapThread(QThread):
    mapPointSignal = pyqtSignal(float, float, float)
    point = [0, 0, 0]

    def __init__(self, parent, address):
        QThread.__init__(self, parent)
        self.address = address

    def run(self):
        tcp_buff_size = 64
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting map rx TCP client to {self.address}")
        tcp_client_socket.connect(self.address)
        while True:
            bytesReceived = tcp_client_socket.recv(tcp_buff_size)
            if len(bytesReceived) == 12:
                self.point = struct.unpack('fff', bytesReceived)
                # print(f"Got map point: [{self.point[0]}, {self.point[1]}, {self.point[2]}]")
                self.mapPointSignal.emit(*self.point)

