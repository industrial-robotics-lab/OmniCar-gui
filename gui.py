import sys
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QBrush, QImage, QPixmap, QVector2D

class Knob(QGraphicsEllipseItem):
    def __init__(self, x, y, d, maxRadius, fetchPosition):
        super().__init__(0, 0, d, d)
        self.fetchPosition = fetchPosition
        self.outPos = QPointF() # ------------------------------------- out
        self.maxRadius = maxRadius
        self.basePos = QVector2D(x, y)
        self.vecFromBase = QVector2D(x, y)
        self.setPos(self.basePos.toPointF())
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(1)))
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().setOverrideCursor(Qt.ArrowCursor)
        # app.instance().restoreOverrideCursor()
    
    def mousePressEvent(self, event):
        app.instance().setOverrideCursor(Qt.ClosedHandCursor)

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
        app.instance().setOverrideCursor(Qt.OpenHandCursor)
        self.setPos(self.basePos.toPointF())
        self.outPos = self.pos()
        self.fetchPosition(self.outPos)


class TurnButton(QGraphicsEllipseItem):
    def __init__(self, x, y, d):
        super().__init__(x, y, d, d)
        self.isActive = False # --------------------------------------- out
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(1)))
        self.setAcceptHoverEvents(True)
    
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.PointingHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()
    
    def mousePressEvent(self, event):
        self.isActive = True

    def mouseReleaseEvent(self, event):
        self.isActive = False


class LimitCircle(QGraphicsEllipseItem):
    def __init__(self, x, y, d):
        super().__init__(0, 0, d, d)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(0)))


class TurnSlider(QSlider):
    def __init__(self, maxValue):
        super().__init__(Qt.Horizontal)
        self.valueChanged[int].connect(self.onChange)
        self.setRange(-maxValue, maxValue)
        self.setValue(0)
    
    def onChange(self, value):
        print(f"Slider value = {value}")
 
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setValue(0)


class GraphicalView(QGraphicsView):
    def __init__(self, fetchPosition):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 500, 500)

        self.knob = Knob(225, 225, 50, 200, fetchPosition)
        self.scene.addItem(self.knob)
        self.limitCircle = LimitCircle(50, 50, 400)
        self.scene.addItem(self.limitCircle)
        # self.turnLeftBtn = TurnButton(50, 50, 50)
        # self.scene.addItem(self.turnLeftBtn)
        # self.turnRightBtn = TurnButton(400, 50, 50)
        # self.scene.addItem(self.turnRightBtn)

class OmniCarGUI(QWidget):
    def __init__(self):
        super().__init__()

        touchpad = GraphicalView(self.fetchPosition)
        slider = TurnSlider(100)
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

    def fetchPosition(self, outPos):
        pass

knobPos = [0, 0]
def updateKnobPos(outPos):
    knobPos[0] = outPos.x()
    knobPos[1] = outPos.y()
    print(f"Fetching pos: {knobPos}")

app = QApplication(sys.argv)

main = OmniCarGUI()
main.show()

sys.exit(app.exec_())