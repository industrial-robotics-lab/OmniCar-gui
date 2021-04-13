import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QBrush, QPixmap, QVector2D

class Knob(QGraphicsEllipseItem):
    def __init__(self, x, y, d, maxRadius, app, fetchPosition):
        super().__init__(0, 0, d, d)
        self.app = app
        self.fetchPosition = fetchPosition
        self.outPos = QPointF() # ------------------------------------- out
        self.maxRadius = maxRadius
        self.basePos = QVector2D(x, y)
        self.vecFromBase = QVector2D(x, y)
        self.setPos(self.basePos.toPointF())
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(1)))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        self.app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        self.app.instance().setOverrideCursor(Qt.ArrowCursor)
        # app.instance().restoreOverrideCursor()
    
    def mousePressEvent(self, event):
        self.app.instance().setOverrideCursor(Qt.ClosedHandCursor)

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
        self.fetchPosition(self.outPos)

    def mouseReleaseEvent(self, event):
        self.app.instance().setOverrideCursor(Qt.OpenHandCursor)
        self.setPos(self.basePos.toPointF())
        self.outPos = self.pos()
        self.fetchPosition(self.outPos)


class LimitCircle(QGraphicsEllipseItem):
    def __init__(self, x, y, d):
        super().__init__(0, 0, d, d)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(0)))


class TurnSlider(QSlider):
    def __init__(self, maxValue, fetchPosition):
        super().__init__(Qt.Horizontal)
        self.valueChanged[int].connect(fetchPosition)
        self.setRange(-maxValue, maxValue)
        self.setValue(0)
 
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setValue(0)


class Touchpad(QGraphicsView):
    def __init__(self, app, fetchPosition):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 500, 500)

        self.knob = Knob(225, 225, 50, 200, app, fetchPosition)
        self.scene.addItem(self.knob)
        self.limitCircle = LimitCircle(50, 50, 400)
        self.scene.addItem(self.limitCircle)

class OmniCarGUI(QWidget):
    def __init__(self, app, fetchTouchpadPos, fetchSliderPos):
        super().__init__()

        touchpad = Touchpad(app, fetchTouchpadPos)
        slider = TurnSlider(100, fetchSliderPos)
        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap("pencils.jpg").scaled(500, 500, Qt.AspectRatioMode(1)))

        vLayout = QVBoxLayout()
        vLayout.addWidget(touchpad)
        vLayout.addWidget(slider)

        layout = QHBoxLayout()
        layout.addLayout(vLayout)
        layout.addWidget(imageLabel)
        self.setLayout(layout)

        self.setWindowTitle("OmniCar GUI")