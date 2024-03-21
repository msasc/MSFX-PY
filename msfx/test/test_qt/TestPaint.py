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
        print(f"Width: {width} Height: {height} Parent width: {self.parent().width()}")

        x = int((width - (width * 3 / 4)) / 2)
        y = int((height - (height * 3 / 4)) / 2)
        w = int(width - (width / 4))
        h = int(height - (height / 4))

        # w = min(w, h)
        # h = min(w, h)

        buffered = False

        if buffered:
            image = QImage(QSize(width, height), QImage.Format.Format_RGBA64_Premultiplied)

            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor('black'), 1))

            painter.fillRect(QRectF(0, 0, width, height), QColor("white"))
            painter.drawEllipse(QRectF(x, y, w, h))

            painter = QPainter(self)
            painter.drawImage(QRectF(0, 0, width, height), image)

        else:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(QColor('black'), 1))
            painter.drawEllipse(x, y, w, h)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt drawing tutorial")

        self.__canvas = QCanvas(self)
        layout = QVBoxLayout()
        layout.addWidget(self.__canvas)
        self.setLayout(layout)

        self.__label = QLabel()
        self.__label.setText("Hello my friend")
        # self.__label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(self.__label)


if __name__ == "__main__":
    app = QApplication([])
    screen = QGuiApplication.primaryScreen()

    wnd = Window()
    wnd.show()

    sys.exit(app.exec())
