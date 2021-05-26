#!/usr/bin/env python3
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import numpy as np
import random
import sys

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Matplotlib live plot in PyQt - example 2")
        self.frm = QtWidgets.QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: #eeeeec; }")
        self.lyt = QtWidgets.QVBoxLayout()
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)

        self.myFig = MyCanvas(x_range=[-2, 2], y_range=[-2, 2], interval=20)
        self.lyt.addWidget(self.myFig)

        self.show()

class MyCanvas(FigureCanvas, anim.FuncAnimation):
    def __init__(self, x_range, y_range, interval: int) -> None:
        FigureCanvas.__init__(self, mpl_fig.Figure())
        self.x_range = x_range
        self.y_range = y_range
        self.x = []
        self.y = []

        self.ax = self.figure.subplots()
        self.ax.set_xlim(xmin=x_range[0], xmax=x_range[1])
        self.ax.set_ylim(ymin=y_range[0], ymax=y_range[1])
        self.line, = self.ax.plot([], [])

        anim.FuncAnimation.__init__(self, self.figure, self.update_canvas, interval=interval, blit=True)
        return

    def update_canvas(self, i) -> None:
        self.x.append(random.uniform(self.x_range[0], self.x_range[1]))
        self.y.append(random.uniform(self.y_range[0], self.y_range[1]))
        self.line.set_data(self.x, self.y)
        return self.line,


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = MyApp()
    qapp.exec_()
