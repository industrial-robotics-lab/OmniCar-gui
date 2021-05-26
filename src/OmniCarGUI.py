from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage
from OmniCarWidgets import Touchpad, TurnSlider, Map
from OmniCarCommunication import TcpControlThread, UdpVideoThread, TcpMapThread



class OmniCarGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1100, 600)

        videoThread = UdpVideoThread(self)
        videoThread.changePixmap.connect(self.setImage)
        videoThread.start()

        tcpControlThread = TcpControlThread(self)
        tcpControlThread.start()

        self.map = Map()

        tcpMapThread = TcpMapThread(self)
        tcpMapThread.point.connect(self.map.add_point_to_map)
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
        self.setLayout(layout)

        self.setWindowTitle("OmniCar GUI")

    @pyqtSlot(QImage)
    def setImage(self, img):
        self.imageLabel.setPixmap(QPixmap.fromImage(img).scaled(500, 500, Qt.KeepAspectRatio))