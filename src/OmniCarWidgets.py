from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QSlider, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QPointF, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QBrush, QVector2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
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
        x = rescale(x, -200, 200, 0, 255)
        y = rescale(y, -200, 200, 0, 255)
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


class TurnSlider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setRange(0, 255)
        self.setValue(127)
 
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setValue(127)


class Map(QWidget):

    def __init__(self, limit):
        super(Map, self).__init__()

        self.theta_list = [0]
        self.x_list = [0]
        self.y_list = [0]
        
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.figure = plt.figure(figsize=(6,5))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self._ax = self.figure.add_subplot(111)
        self._ax.set_title('Wheel odometry')
        self._line = self._ax.plot([], [], 'k')[0]

        self._ax.set_xlim(-limit, limit)
        self._ax.set_ylim(-limit, limit)

    @pyqtSlot(float, float, float)
    def add_point_to_map(self, theta, x, y):
        if theta != self.theta_list[-1] or x != self.x_list[-1] or y != self.y_list[-1]:
            self.theta_list.append(theta)
            self.x_list.append(x)
            self.y_list.append(y)
            # print(f"Got new point: [{theta}, {x}, {y}]; traj size: {len(self.x_list)}")
            self._line.set_data(self.x_list, self.y_list)
            self.canvas.draw()