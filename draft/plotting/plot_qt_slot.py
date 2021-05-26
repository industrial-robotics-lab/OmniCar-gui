import sys
import random
from PyQt5 import QtCore, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()

        self.setMinimumSize(QtCore.QSize(1200,800))
        self.setWindowTitle('My Graphic Window')

        self.list_x_y = ListXY()
        self.plotview = Plot()
        self.setCentralWidget(self.plotview)
        self.list_x_y.listChanged.connect(self.plotview.update_data)

        timer = QtCore.QTimer(self, interval=100)
        timer.timeout.connect(self.list_x_y.createdata)
        timer.start()

class Plot(QtWidgets.QWidget):
    def __init__(self):
        super(Plot, self).__init__()
        self.initializewidget()

    def initializewidget(self):
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        self.figure = plt.figure(figsize=(15,5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self._ax = self.figure.add_subplot(111)
        self._ax.set_title('Random Plot')
        self._line = self._ax.plot([], [], 'b.-')[0]

    @QtCore.pyqtSlot(list, list)
    def update_data(self, x, y):
        self._line.set_data(x, y)
        self._ax.set_xlim(min(x), max(x))
        self._ax.set_ylim(min(y), max(y))
        self.canvas.draw()

class ListXY(QtCore.QObject):
    listChanged = QtCore.pyqtSignal(list, list)

    def createdata(self):
        X, Y = list(range(100)), []
        for y in range(0,100):
            Y.append(random.randint(0, 100)) 
        self.listChanged.emit(X, Y)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    im = Mainwindow()
    im.show()
    sys.exit(app.exec_())