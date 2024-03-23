import sys
import typing

from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class QCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

    def paintEvent(self, event):
        width = self.width()
        height = self.height()

        factor = 0.98

        x = int(width * (1 - factor) / 2)
        y = int(height * (1 - factor) / 2)
        w = int(width * factor)
        h = int(height * factor)

        w = min(w, h)
        h = min(w, h)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor('black'), 1))
        painter.drawEllipse(x, y, w, h)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt drawing tutorial")

        canvas = QCanvas()
        canvas.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        layout = QGridLayout()
        layout.addWidget(canvas, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.setCentralWidget(canvas)

if __name__ == "__main__":
    app = QApplication([])
    screen = QGuiApplication.primaryScreen()

    wnd = Window()
    wnd.show()

    sys.exit(app.exec())
