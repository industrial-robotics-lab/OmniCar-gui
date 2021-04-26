from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPointF, QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QColor, QBrush, QPixmap, QVector2D, QImage
import socket, base64, numpy as np, cv2
from utils import rescale

class Knob(QGraphicsEllipseItem):

    def __init__(self, x, y, d, maxRadius, updatePos):
        super().__init__(0, 0, d, d)
        self.updatePos = updatePos
        self.app = QApplication.instance()
        self.outPos = QPointF() # ------------------------------------- out
        self.maxRadius = maxRadius
        self.basePos = QVector2D(x, y)
        self.vecFromBase = QVector2D(x, y)
        self.setPos(self.basePos.toPointF())
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(1)))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.app.setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        self.app.setOverrideCursor(Qt.ArrowCursor)
        # app.instance().restoreOverrideCursor()
    
    def mousePressEvent(self, event):
        self.app.setOverrideCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        orig_cursor_pos = event.lastScenePos()
        updated_cursor_pos = event.scenePos()
        orig_pos = self.scenePos()
        cursor_x = updated_cursor_pos.x() - orig_cursor_pos.x() + orig_pos.x()
        cursor_y = updated_cursor_pos.y() - orig_cursor_pos.y() + orig_pos.y()
        self.vecFromBase.setX(cursor_x)
        self.vecFromBase.setY(cursor_y)
        self.vecFromBase -= self.basePos
        if self.vecFromBase.length() >= self.maxRadius:
            self.vecFromBase.normalize()
            self.vecFromBase *= self.maxRadius
        self.outPos = (self.basePos + self.vecFromBase).toPointF()
        self.setPos(self.outPos)
        x = self.vecFromBase.x()
        y = -self.vecFromBase.y()
        x = rescale(x, -200, 200, 0, 256)
        y = rescale(y, -200, 200, 0, 256)
        self.updatePos(x, y)

    def mouseReleaseEvent(self, event):
        self.app.setOverrideCursor(Qt.OpenHandCursor)
        self.setPos(self.basePos.toPointF())
        self.outPos = self.pos()
        self.updatePos(127, 127) # middle for 0-256


class LimitCircle(QGraphicsEllipseItem):
    def __init__(self, x, y, d):
        super().__init__(0, 0, d, d)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(0)))


class TurnSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setRange(0, 255)
        self.setValue(127)
 
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setValue(127)


class Touchpad(QGraphicsView):
    changePos = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 500, 500)

        self.knob = Knob(225, 225, 50, 200, self.updatePos)
        self.scene.addItem(self.knob)
        self.limitCircle = LimitCircle(50, 50, 400)
        self.scene.addItem(self.limitCircle)
    
    def updatePos(self, x, y):
        self.changePos.emit(x, y)


class UdpVideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        udp_server_address = ("192.168.0.119", 10002)
        # udp_server_address = ("127.0.0.1", 10002)
        udp_buff_size = 65536 # max buffer size
        udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, udp_buff_size)

        init_msg = b"Init video transmission from server by this message"
        udp_client_socket.sendto(init_msg, udp_server_address)
        while True:
            msg = udp_client_socket.recv(udp_buff_size)
            data = base64.b64decode(msg, ' /')
            npdata = np.fromstring(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1) # 1 means return image as is
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            self.changePixmap.emit(convertToQtFormat)


class TcpThread(QThread):
    control_vec = [0,0,0]

    def run(self):
        tcp_server_address = ("192.168.0.119", 10001)
        # tcp_server_address = ("127.0.0.1", 10001)
        # tcp_buff_size = 1024
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Connecting TCP client to {tcp_server_address}")
        tcp_client_socket.connect(tcp_server_address)
        while True:
            msg = bytes(self.control_vec) # input str to bytes
            # print(f"Sending {len(msg)} bytes via TCP")
            tcp_client_socket.sendall(msg)
    
    @pyqtSlot(int, int)
    def updateLin(self, x, y):
        self.control_vec[0] = x
        self.control_vec[1] = y
    
    @pyqtSlot(int)
    def updateAng(self, value):
        self.control_vec[2] = value


class OmniCarGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1100, 600)

        videoThread = UdpVideoThread(self)
        videoThread.changePixmap.connect(self.setImage)
        videoThread.start()

        tcpThread = TcpThread(self)
        tcpThread.start()

        self.touchpad = Touchpad()
        self.touchpad.changePos.connect(tcpThread.updateLin)
        self.slider = TurnSlider()
        self.slider.valueChanged[int].connect(tcpThread.updateAng)
        self.imageLabel = QLabel(self)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.touchpad)
        vLayout.addWidget(self.slider)

        layout = QHBoxLayout()
        layout.addLayout(vLayout)
        layout.addWidget(self.imageLabel)
        self.setLayout(layout)

        self.setWindowTitle("OmniCar GUI")

    @pyqtSlot(QImage)
    def setImage(self, img):
        self.imageLabel.setPixmap(QPixmap.fromImage(img).scaled(500, 500, Qt.KeepAspectRatio))