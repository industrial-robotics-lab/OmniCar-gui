from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QPointF, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QBrush, QPixmap, QVector2D, QImage
import cv2

class Knob(QGraphicsEllipseItem):
    def __init__(self, x, y, d, maxRadius, fetchPosition):
        super().__init__(0, 0, d, d)
        self.app = QApplication.instance()
        self.fetchPosition = fetchPosition
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
        self.fetchPosition(self.outPos)

    def mouseReleaseEvent(self, event):
        self.app.setOverrideCursor(Qt.OpenHandCursor)
        self.setPos(self.basePos.toPointF())
        self.outPos = self.pos()
        self.fetchPosition(self.outPos)


class LimitCircle(QGraphicsEllipseItem):
    def __init__(self, x, y, d):
        super().__init__(0, 0, d, d)
        self.setPos(x, y)
        self.setBrush(QBrush(QColor(0, 0, 0), Qt.BrushStyle(0)))


class TurnSlider(QSlider):
    def __init__(self, updateSliderPos, maxValue):
        super().__init__(Qt.Horizontal)
        self.valueChanged[int].connect(updateSliderPos)
        self.setRange(-maxValue, maxValue)
        self.setValue(0)
 
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.setValue(0)


class GraphicalView(QGraphicsView):
    def __init__(self, updateKnobPos):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(0, 0, 500, 500)

        self.knob = Knob(225, 225, 50, 200, updateKnobPos)
        self.scene.addItem(self.knob)
        self.limitCircle = LimitCircle(50, 50, 400)
        self.scene.addItem(self.limitCircle)

class VideoThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                self.changePixmap.emit(convertToQtFormat)

class OmniCarGUI(QWidget):
    def __init__(self, updateKnobPos, updateSliderPos):
        super().__init__()
        self.resize(1100, 600)

        touchpad = GraphicalView(updateKnobPos)
        slider = TurnSlider(updateSliderPos, 100)
        self.imageLabel = QLabel(self)
        videoThread = VideoThread(self)
        videoThread.changePixmap.connect(self.updateImage)
        videoThread.start()

        vLayout = QVBoxLayout()
        vLayout.addWidget(touchpad)
        vLayout.addWidget(slider)

        layout = QHBoxLayout()
        layout.addLayout(vLayout)
        layout.addWidget(self.imageLabel)
        self.setLayout(layout)

        self.setWindowTitle("OmniCar GUI")

    @pyqtSlot(QImage)
    def updateImage(self, img):
        self.imageLabel.setPixmap(QPixmap.fromImage(img).scaled(500, 500, Qt.KeepAspectRatio))