from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import ctypes


class Loading(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setup_ui()

    def setup_ui(self):
        self.movie = QMovie('assets\\load.gif')
        gu = ctypes.windll.user32
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setGeometry(gu.GetSystemMetrics(0) / 2 - 300 / 2, gu.GetSystemMetrics(1) / 2 - 300 / 2, 300, 300)
        self.setGeometry(
            QtCore.QRect(gu.GetSystemMetrics(0) / 2 - 300 / 2, gu.GetSystemMetrics(1) / 2 - 300 / 2, 300, 300))

        self.lbl = QLabel()
        self.setStyleSheet("QLabel\n"
                           "{\n"
                           "     background-color: #D7CCC8;\n"
                           "}\n"
                           )
        self.lbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.lbl.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.lbl)
        self.setLayout(main_layout)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.lbl.setMovie(self.movie)
        self.movie.start()
        self.movie.loopCount()

    def start_dialog(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()

    def stop_dialog(self):
        self.hide()

# app = QApplication(sys.argv)
# w = Loading()
# w.start_dialog()
# app.exec_()
