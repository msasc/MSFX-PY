import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QGuiApplication
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QGridLayout, QApplication

from msfx.lib.qt.canvas import QCanvas

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt drawing tutorial")

        self.canvas = QCanvas()
        self.canvas.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        layout = QGridLayout()
        layout.addWidget(self.canvas, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.setCentralWidget(self.canvas)

        self.canvas.paintCanvas.connect(self.paintCanvas)

    def paintCanvas(self, event):
        width = self.canvas.width()
        height = self.canvas.height()

        factor = 0.98

        x = int(width * (1 - factor) / 2)
        y = int(height * (1 - factor) / 2)
        w = int(width * factor)
        h = int(height * factor)

        # w = min(w, h)
        # h = min(w, h)

        painter: QPainter = self.canvas.startPaint()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor('black'), 1))
        painter.drawEllipse(x, y, w, h)
        self.canvas.endPaint()

if __name__ == "__main__":
    app = QApplication([])
    # noinspection PyArgumentList
    screen = QGuiApplication.primaryScreen()

    wnd = Window()
    wnd.show()

    sys.exit(app.exec())
