#!/usr/bin/env python3
# Transmit wheel controls + Receive video
from gui import OmniCarGUI
from PyQt5.QtWidgets import QApplication
import sys

knobPos = [0, 0]
sliderPos = 0

def updateKnobPos(outPos):
    global knobPos
    knobPos[0] = outPos.x()
    knobPos[1] = outPos.y()

def updateSliderPos(outPos):
    global sliderPos
    sliderPos = outPos

app = QApplication(sys.argv)
main = OmniCarGUI(updateKnobPos, updateSliderPos)
main.show()

sys.exit(app.exec_())