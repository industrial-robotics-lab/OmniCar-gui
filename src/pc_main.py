#!/usr/bin/env python3
# Transmit car control + Receive video
from gui import OmniCarGUI
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
gui = OmniCarGUI()
gui.show()

sys.exit(app.exec_())