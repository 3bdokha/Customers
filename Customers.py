from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import os
import sys
from Setup_UI.setup_ui import MainForm

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_EnableHighDpiScaling)
if __name__ == '__main__':
    w = MainForm()
    w.showMaximized()
    sys.exit(app.exec_())
