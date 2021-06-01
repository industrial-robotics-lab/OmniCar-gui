from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from OmniCarWidgets import Touchpad, TurnSlider, Map
from OmniCarCommunication import TcpControlThread, UdpVideoThread, TcpMapThread



class OmniCarGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1800, 600)

        # ip = "192.168.0.119"
        ip = "127.0.0.1"
        tcp_tx_port = 10001
        udp_rx_port = 10002
        tcp_rx_port = 10003

        videoThread = UdpVideoThread(self, (ip, udp_rx_port))
        videoThread.changePixmap.connect(self.setImage)
        videoThread.start()

        tcpControlThread = TcpControlThread(self, (ip, tcp_tx_port))
        tcpControlThread.start()

        self.map = Map()

        tcpMapThread = TcpMapThread(self, (ip, tcp_rx_port))
        tcpMapThread.mapPointSignal.connect(self.map.add_point_to_map)
        tcpMapThread.start()

        self.touchpad = Touchpad()
        self.touchpad.changePos.connect(tcpControlThread.updateLin)
        self.slider = TurnSlider()
        self.slider.valueChanged[int].connect(tcpControlThread.updateAng)
        self.imageLabel = QLabel(self)

        vLayout = QVBoxLayout()
        vLayout.addWidget(self.touchpad)
        vLayout.addWidget(self.slider)

        layout = QHBoxLayout()
        layout.addLayout(vLayout)
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.map)
        self.setLayout(layout)

        self.setWindowTitle("OmniCar GUI")

    @pyqtSlot(QImage)
    def setImage(self, img):
        self.imageLabel.setPixmap(QPixmap.fromImage(img).scaled(500, 500, Qt.KeepAspectRatio))