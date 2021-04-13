import sys
from PyQt5.QtWidgets import QApplication
from gui import OmniCarGUI

def fetchTouchpadPos(value):
    print(f"Touchpad: {value}")

def fetchSliderPos(value):
    print(f"Slider: {value}")

app = QApplication(sys.argv)

gui = OmniCarGUI(app, fetchTouchpadPos, fetchSliderPos)
gui.show()

sys.exit(app.exec_())