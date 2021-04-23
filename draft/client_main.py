#!/usr/bin/env python3
# Transmit car control + Receive video
from gui import OmniCarGUI
from PyQt5.QtWidgets import QApplication
import sys
import cv2, imutils, socket, base64
from threading import Thread
import numpy as np


app = QApplication(sys.argv)
gui = OmniCarGUI()
gui.show()

sys.exit(app.exec_())